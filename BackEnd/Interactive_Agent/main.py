# import all necessary libraries and modules
import os
from dotenv import load_dotenv
from agents import Agent, Runner,trace, function_tool
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import requests
import asyncio
import httpx
from typing import Any
import os 

#override default environment variables with .env file
load_dotenv(override=True)

#Planning to use OPEN AI agent SDK, therefore we need to create an anthropic client that is compatible with the openai agent sdk. 
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

