# Testing : Connecting to supabase and retrieving data from the database using FastAPI


# Import the required libraries 

from fastapi import FastAPI
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Provide a brief description of the task

"""


This is a wrapper Fast API to call supabase API and retrieve the stored in that database.


"""
load_dotenv()
#Load the necessary keys

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

print(SUPABASE_KEY)

# Create a client with supabase

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



app = FastAPI()

@app.get("/data")
async def get_data():
    try:
        response = supabase.table('test_data').select("*").execute()
    except:
        response = {'details':"Error"}
    return response
