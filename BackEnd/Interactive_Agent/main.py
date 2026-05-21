# import all necessary libraries and modules
import os
from dotenv import load_dotenv
from agents import Agent, Runner,trace, function_tool
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import requests
import asyncio
import httpx
from typing import Annotated, Any
import os 
from .agent_config import system_prompt
from fastapi import APIRouter, HTTPException
from Supabase.supabase_databases import SessionLocal
from Supabase.main import fetch_table_data
from starlette import status

load_dotenv(override=True)

# Load the necessary keys
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_HOST_POOL = os.getenv("SUPABASE_HOST_POOL")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA")
SUPABASE_CONTAINER = os.getenv("SUPABASE_CONTAINER")


#override default environment variables with .env file


#Define the FastAPI application instance
router = APIRouter(
    prefix="/interactive-agent",
    tags=["interactive-agent"],
    responses={404: {"description": "Not found"}},
)




system_prompts = system_prompt(ALL_ENDPOINTS=["/data/exception", "/data/logic", "/data/dictionary", "/data/summary"])

ALL_ENDPOINTS=["/data/exception", "/data/logic", "/data/dictionary", "/data/summary"]
# Planning to use OPEN AI agent SDK, therefore we need to create an anthropic client that is compatible with the openai agent sdk. 
# This will allow us to use the same codebase for both openai and anthropic models, and easily switch between them if needed.

anthropic_client = AsyncOpenAI(
    api_key= os.getenv(key='ANTHROPIC_API_KEY'),
    base_url='https://api.anthropic.com/v1/',
)

# Create an instance of the OpenAIChatCompletionsModel using the anthropic client and Open ai model to be used for the interactive agent.

anthropic_model = OpenAIChatCompletionsModel(
            model="claude-haiku-4-5",
            openai_client=anthropic_client,
            )
openai_model = "gpt-4o-mini"

#First tool 
async def _fetch_one(client: httpx.AsyncClient, endpoint: str) -> tuple[str, Any]:
    #BASE_URL = "https://controldev-apfxc7h7etf4breb.southafricanorth-01.azurewebsites.net" #for modularity, will use docker container communication in prod.
    #BASE_URL = f"http://localhost:8000/supabase" #for modularity, will use docker container communication in prod.
    key = endpoint.split("/")[-1]
    try:
        db = SessionLocal()        
        try:
            response = await asyncio.to_thread(fetch_table_data, table=key, db=db)
            return key, response
        finally:
            db.close() 
    except httpx.RequestError:
        pass
    return key, None

@function_tool
async def fetch_control_data(endpoints: list[str] | None = None) -> dict[str, Any]:
    """
    Fetch ControlWeb data from one or more endpoints concurrently.

    Args:
        endpoints: Subset of ['/data/exception', '/data/logic', '/data/dictionary'].
                   Defaults to all three if not provided.

    Returns:
        Dict keyed by endpoint name ('exception', 'logic', 'dictionary').
        Keys for failed/non-200 requests are omitted.
    """
    targets = endpoints if endpoints is not None else ALL_ENDPOINTS
    async with httpx.AsyncClient() as client:
        tasks = [_fetch_one(client, ep) for ep in targets]
        results = await asyncio.gather(*tasks)
    return {key: data for key, data in results if data is not None}

tools = [fetch_control_data]

#create the processing agent

ai_processing = Agent(name="AI processing agent",
                      instructions=system_prompts.processing_agent_prompt,
                      tools=tools,
                      model= anthropic_model,
                      )
# testing message
#message = "How many exceptions are there?"


handoff=ai_processing

ai_assistent = Agent(name="AI assistant",
                      instructions=system_prompts.receipent_agent_prompt,
                      model= openai_model,
                      handoffs=[handoff],
                      handoff_description="Pass the rewritten instruction to the AI processing agent for execution.",
                      )


async def interactive_agents(message: str) -> str:
    """Process a user message through the interactive agent workflow.
    Args:
        message: The original user query to be processed.
    Returns:
        The final output from the AI processing agent after handling the message.
    """
    with trace("testing preprod") as t:
        rewritten_message = await Runner.run(ai_assistent,message)
        return rewritten_message.final_output


#print(asyncio.run(some_function()))

@router.get("/interactive-agent",status_code= status.HTTP_200_OK)
async def interactive_agent(message: str):
    """
    Endpoint to process a user message through the interactive agent workflow.

    Args:
        message: The original user query to be processed.

    Returns:
        The final output from the AI processing agent after handling the message.
    """
    try:
        result = await interactive_agents(message=message)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




