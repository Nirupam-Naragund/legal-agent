from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from crewai import Agent, Task, Crew, Process, LLM
import json
import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GEMINI_API_KEY,
    temperature=0,
)

# Define the Planner Agent
planner = Agent(
    llm=llm,
    role="Legal Content Planner",
    goal="Generate an in-depth legal analysis with relevant sections, landmark judgments, and detailed reasoning for the situation: {situation}",
    backstory=(
        "You are an expert legal researcher with extensive knowledge of Indian Penal Code, "
        "Criminal Procedure Code, and landmark judicial precedents. Your task is to provide "
        "a comprehensive and structured legal analysis of the given crime scenario."
    ),
    allow_delegation=False,
    verbose=True,
    embedder={
        "provider": "google",
        "config": {
            "model": "models/text-embedding-004",
            "api_key": GEMINI_API_KEY,
        }
    }
)

# Define the Legal Analysis Task
plan = Task(
    description=(
        "1. Analyze the given situation: {situation} to identify the most relevant legal sections.\n"
        "2. Retrieve legal sections and landmark judgments associated with the situation.\n"
        "3. Provide a detailed reasoning for the relevance of each section.\n"
        "4. Include summaries and URLs for landmark judgments."
    ),
    expected_output="""
    {{
        "legalSections": [
            {{
                "sectionCode": "IPC Section [Section Code]",
                "description": "[Brief description of the legal section]",
                "relevanceScore": "[Percentage indicating importance]",
                "reasoning": "[Very Detailed explanation of why this section applies]"
            }}
        ],
        "landmarkJudgments": [
            {{
                "title": "[Full Case Title]",
                "summary": "[Detailed Summary of the judgment's main points]",
            }}
        ],
        "legalAnalysisSummary": "[Comprehensive overview of legal implications]"
    }}
    """,
    agent=planner,
    output_format="json"  # Specify JSON as a string
)

# Assemble the Crew with Memory Capabilities
my_crew = Crew(
    agents=[planner],
    tasks=[plan],
    llm=llm,
    process=Process.sequential,
    memory=True,
    embedder={
        "provider": "google",
        "config": {
            "model": "models/text-embedding-004",
            "api_key": GEMINI_API_KEY,
        }
    },
    verbose=True
)

class SituationInput(BaseModel):
    situation: str

@app.post("/analyze")
async def analyze(situation_input: SituationInput):
    inputs = {"situation": situation_input.situation}
    result = my_crew.kickoff(inputs=inputs)

    try:
        # Extract the JSON string from the raw output
        raw_output = result.raw.strip("```json\n").strip("\n```")
        result_dict = json.loads(raw_output)  # Parse the JSON string into a dictionary
    except (AttributeError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing the result: {e}")

    return result_dict

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)