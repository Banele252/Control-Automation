# Testing: Generating synthetic data using AI, then ingesting the data to Mongo DB using Fast API. Additionally retrieving the data.

# import libraries and connect mongodb

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from starlette import status
from motor.motor_asyncio import AsyncIOMotorClient
from agents import Agent, Runner, trace
import json
from config import agent_info

load_dotenv()

app = FastAPI()

# =========================
# Configure AI Agent
# =========================



system_prompt = agent_info.system_prompt

data_generator_agent = Agent(
    name="agent_data_generator",
    instructions=system_prompt,
    model="gpt-4o-mini"
)

# ===========================
# MongoDB Connection
# ===========================

username = os.getenv("MONGO_USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.k3rfzyy.mongodb.net/{database}?retryWrites=true&w=majority"

client = AsyncIOMotorClient(mongo_uri)
db = client[database]

synthetic_collection = db["Synthetic_data"]
overview_collection = db["Dataset_Overview"]
dictionary_collection = db["Synthetic_Data"]
anomaly_collection = db["Anomaly_Key"]

# =========================
# Agent Call Function
# =========================

async def generate_synthetic_data():
    with trace("Generating synthetic data"):
        result = await Runner.run(
            data_generator_agent,
            "Telecommunication customer postpaid subscription dataset with 50 records, including 5-10% anomalies. Less than 10 fields"
        )

    return result.final_output


# =========================
# API Endpoint
# =========================

@app.post("/AI_generated_data", status_code=status.HTTP_200_OK)
async def insert_synthetic_data():

    try:
        # 1️⃣ Generate data from agent
        result = await generate_synthetic_data()

        # 2️⃣ Convert JSON string to Python dict
        data = json.loads(result)

        # 3️⃣ Extract synthetic records
        synthetic_records = data["Synthetic Data"]
        dictionary_records = data["Data Dictionary"]
        overview_records = data["Dataset Overview"]
        anomaly_records = data["Anomaly Key"]

        # 4️⃣ Insert into MongoDB
        synthetic_insert_result = await synthetic_collection.insert_many(synthetic_records)
        dictionary_insert_result = await synthetic_collection.insert_many(dictionary_records)
        overview_insert_result = await synthetic_collection.insert_many(overview_records)
        anomaly_insert_result = await synthetic_collection.insert_many(anomaly_records)

        return {"outcome":[{
                        "status": "success",
                        "records_inserted": len(synthetic_insert_result.inserted_ids)
                    },{
                    "status": "success",
                        "records_inserted": len(dictionary_insert_result.inserted_ids)
                    },
                    {
                    "status": "success",
                        "records_inserted": len(overview_insert_result.inserted_ids)
                    },
                    {
                    "status": "success",
                        "records_inserted": len(anomaly_insert_result.inserted_ids)
                    }

                 ]
                }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error encountered during processing: {str(e)}"
        )

@app.get("/get_synthetic_data", status_code=status.HTTP_200_OK)
async def get_synthetic_data():
    try:
        # Fetch all records from MongoDB
        records = []
        documents = await synthetic_collection.find().to_list()  # Adjust length as needed
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            records.append(doc)

        return {
            "status": "success",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error encountered during data retrieval: {str(e)}"
        )
    
@app.get("/get_overview", status_code=status.HTTP_200_OK)
async def get_overview():
    try:
        # Fetch all records from MongoDB
        records = []
        documents = await overview_collection.find().to_list()  # Adjust length as needed
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            records.append(doc)

        return {
            "status": "success",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error encountered during data retrieval: {str(e)}"
        )
    


@app.get("/get_dictionary", status_code=status.HTTP_200_OK)
async def get_data_dictionary():
    try:
        # Fetch all records from MongoDB
        records = []
        documents = await dictionary_collection.find().to_list()  # Adjust length as needed
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            records.append(doc)

        return {
            "status": "success",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error encountered during data retrieval: {str(e)}"
        )

@app.get("/get_anomaly", status_code=status.HTTP_200_OK)
async def get_anomaly_data():
    try:
        # Fetch all records from MongoDB
        records = []
        documents = await anomaly_collection.find().to_list()  # Adjust length as needed
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            records.append(doc)

        return {
            "status": "success",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error encountered during data retrieval: {str(e)}"
        )


