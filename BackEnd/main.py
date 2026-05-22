from fastapi import FastAPI, HTTPException, Depends
from Interactive_Agent import main as interactive_main
from Summary_Agent import main as summary_main
from Supabase import main as supabase_main

app = FastAPI()


@app.get("/healthy-check")
async def healthy_check():
    return {"message": "Healthy"}

app.include_router(interactive_main.router)
app.include_router(summary_main.router)
app.include_router(supabase_main.router)