# Testing : Connecting to supabase and retrieving data from the database using FastAPI


# Import the required libraries.

from fastapi import FastAPI, HTTPException, Depends
import os
from dotenv import load_dotenv
import psycopg2
from pydantic import BaseModel
from typing import List, Dict, Annotated
from sqlalchemy.orm import Session
from starlette import status
from supabase_databases import SessionLocal
from supabase_mapping import get_orm_model # this is used to get details of the ORL model

# Provide a brief description of the task

"""


This is a wrapper Fast API to call supabase API and retrieve the stored in that database.


"""
app = FastAPI()

def get_db(): # Creates a DB session 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

load_dotenv(override=True)
#Load the necessary keys

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_HOST_POOL = os.getenv("SUPABASE_HOST_POOL")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA")



def connection_instant():
    conn = psycopg2.connect(
    port=5432,
    database="postgres",
    user=SUPABASE_DB_USER,
    sslmode="require",
    host=SUPABASE_HOST_POOL,
    password=SUPABASE_DB_PASSWORD)
    return conn


####
#get data from  synthetic_data, control_dictionary, control_logic, 
# control_exception
@app.get("/data/{table}",status_code=status.HTTP_200_OK) #table can be synthetic_data, control_dictionary, control_logic, control_exception
def get_data(db:db_dependency ,table:str):
    try:
        return db.query(get_orm_model(table)).all()
    except Exception as e:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=str(e))

#push data from synthetic_data, control_dictionary, control_logic

####
#get data from  synthetic_data, control_dictionary, control_logic, 
# control_exception
'''
@app.get("/data/{table}",status_code=status.HTTP_200_OK) #table can be synthetic_data, control_dictionary, control_logic, control_exception
async def get_data(table:str):
    try:
        conn=connection_instant() #creates a database instant.
        cursor = conn.cursor() #enables to execute queries.
        query = f"""
                 SELECT * FROM %s.%s
                ;""",(SUPABASE_SCHEMA,table)
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        response = data
        cursor.close()
        conn.close()
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))'''

#push data from synthetic_data, control_dictionary, control_logic


@app.post("/insert/{table}", status_code=status.HTTP_201_CREATED) #very important: extracting column dynamically requires
#the order to be the same from the source to the target input.
def insert_many(table: str, rows: List[Dict]):
    if not rows:
        return {"error": "No records provided"}

    try:
        conn = connection_instant()
        cursor = conn.cursor()

        # Extract column names dynamically
        columns = rows[0].keys()
        col_names = ", ".join(columns)

        # Build placeholder string: (%s, %s, %s)
        placeholder = "(" + ", ".join(["%s"] * len(columns)) + ")"

        # Convert list[dict] → list[tuples]
        values = [tuple(row[col] for col in columns) for row in rows]

        # AI - Build SQL
        # Banele- The values section contains placeholders that equals to the number
        # of records that will be inserted to the table. 
        # e.g., insert into a (b,c) values (%s, %s)* x ..[x can be any integer, let say 2]
        # insert into a (b,c) values (%s, %s)* 2,  insert into a (b,c) values (%s, %s), (%s,%s)
        query = f"""
            INSERT INTO {SUPABASE_SCHEMA}.{table} ({col_names})
            VALUES {",".join([placeholder] * len(values))}
        """

        # AI-Flatten all value tuples for psycopg2
        # Banele - takes a list of tuple, iterates through the list and
        # iterates through the each tuple extracting elements. 
        # Therefore, flatten is converting the List[tuples] to a list
        flat_values = [item for tup in values for item in tup]

        cursor.execute(query, flat_values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "inserted": len(rows)}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


