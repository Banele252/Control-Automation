from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv(override=True)

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_HOST_POOL = os.getenv("SUPABASE_HOST_POOL")
SUPABASE_DB_USER = os.getenv("SUPABASE_DB_USER")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA")
SUPBASE_PROJECT_ID= os.getenv("SUPBASE_PROJECT_ID")
SUPABASE_HOST=os.getenv("SUPABASE_HOST")

#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPBASE_PROJECT_ID}.supabase.co:5432/postgres'

url = URL.create(
    drivername="postgresql+psycopg2",
    username=SUPABASE_DB_USER,
    password=SUPABASE_DB_PASSWORD,
    host=SUPABASE_HOST_POOL,
    port=5432,
    database="postgres"
)

engine = create_engine(url, connect_args={"sslmode":"require"})

SessionLocal =  sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()