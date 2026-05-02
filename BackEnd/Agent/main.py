#import all necessary libraries and modules

import os
from dotenv import load_dotenv
from agents import Agent, Runner,trace, function_tool
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import asyncio
import httpx
from typing import Any
from agent_config import system_prompt 
from pydantic import BaseModel,Field
from typing import Optional, List, Dict 
import requests
from fastapi import FastAPI, HTTPException, Depends
from starlette import status

#import json
load_dotenv(override=True)


app = FastAPI()


#import all necessary keys


# Load the necessary keys
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_HOST_POOL = os.getenv("SUPABASE_HOST_POOL")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA")


# Connecting to the database using the raw table information 



# Structured output for the summary agent.

class ControlSummary(BaseModel):
    index_number: int =Field(description='Generate a random integer between 1 and 1000')
    analysis_date: str = Field(description='Date of the analysis (The current date)')
    control_summary: str= Field(description='Sentences that describe exceptions, including the exception count, value, similarity and abnomarlity')
    issue_resolution_status: Optional[str] = Field(description='Write "Pending" for this field')
    feedback_receiving_date: Optional[str] = Field(description='Write "Pending" for this field')
    outcome: Optional[str] = Field(description='Write "Pending" for this field')
    day: Optional[str] = Field(description='Write "Pending" for this field')



#anthropic client and openai compatible model 

anthropic_client = AsyncOpenAI(
    api_key= os.getenv(key='ANTHROPIC_API_KEY'),
    base_url='https://api.anthropic.com/v1',
)

anthropic_model = OpenAIChatCompletionsModel(
                    model="claude-haiku-4-5-20251001",
                    openai_client=anthropic_client,
                    )
openai_model = "gpt-4o-mini"



ALL_ENDPOINTS = ["/data/exception", "/data/logic", "/data/dictionary"] #this needs to be  shared using an API.
BASE_URL = "https://controldev-apfxc7h7etf4breb.southafricanorth-01.azurewebsites.net"

async def _fetch_one(client: httpx.AsyncClient, endpoint: str) -> tuple[str, Any]:
    BASE_URL = "https://controldev-apfxc7h7etf4breb.southafricanorth-01.azurewebsites.net" #Later the API should be passed using environment variables (easier change from dev to test or prod environment)
    key = endpoint.split("/")[-1]
    try:
        response = await client.get(BASE_URL + endpoint)
        if response.status_code == 200:
            return key, response.json()
    except httpx.RequestError:
        pass
    return key, None

@function_tool
async def fetch_controlweb_data(endpoints: list[str] | None = None) -> dict[str, Any]:
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



# Rewriting agents definition
Rewrite_data = Agent(name="AI assistant",
                      instructions=system_prompt.receipent_agent_prompt,
                      tools=[fetch_controlweb_data],
                      model= openai_model,
                      )

# Convert the rewriting agent to a tool

rewrite_tool = Rewrite_data.as_tool(tool_name="rewrite_tool", tool_description="an AI assistant that rewrites JSON files into easily processable output for downstream agents")

# Define the reviewing agent

fraud_analyst = Agent(name="Fraud analyst",
                      instructions=system_prompt.processing_agent_prompt,
                      tools=[rewrite_tool],
                      model=anthropic_model,
                      output_type=ControlSummary
                      )


# Define the message to sent an agent.

message = f"Call the rewrite_tool tool to extract the information to review, provide the tool with following list of Endpoints: {ALL_ENDPOINTS}"


# Define the agent function
async def review_agent(fraud_analyst, message):
    with trace("Multi-agent outcome for reviewing data v2"):
        result = await Runner.run(fraud_analyst,message)
    return result
    

# call the agent
#result = asyncio.run(review_agent(fraud_analyst=fraud_analyst, message=message))



# convert the pydantic model output to a python dictionary

#output_results: ControlSummary = result.final_output
#output_dictionary = output_results.model_dump()


# Call the summary API endpoint for ingesting the results 
#end_point = "/insert/control_summary" #This has to be passed using an API

#URL = BASE_URL+end_point
#response = requests.post(url=URL,json=[output_dictionary]) # Remember the data ingestion point expects an array.
#print(response.status_code)


@app.post("/summary-agent", status_code=status.HTTP_201_CREATED)
async def create_summary(input_endpoints:List[Dict], destination_endpoint:str):

    endpoint_list = [list(dict_item.values())[0] for dict_item in input_endpoints] # I need to optimise this later on.


    message = f"Call the rewrite_tool tool to extract the information to review, provide the tool with following list of Endpoints: {endpoint_list}"
    result = await review_agent(fraud_analyst=fraud_analyst, message=message)

    output_results: ControlSummary = result.final_output
    output_dictionary = output_results.model_dump()

    URL = BASE_URL+ destination_endpoint

    # It best practice to mix sync and async code
    #try: 
    #    requests.post(url=URL,json=[output_dictionary])
    #    return {"status":"success"}
    #except Exception as e:
    #    raise HTTPException(status_code=400, detail=str(e))
    
     # implementing the async version
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=URL, json=[output_dictionary])
            return{"status":"success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



