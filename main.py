from fastapi import FastAPI
from pydantic import BaseModel
from agent import search_agent
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Topic(BaseModel):
    topic:str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate-post")
async def generate_post(topic:Topic):
    return search_agent(topic.topic)
  