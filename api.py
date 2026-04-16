import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

from agent import creer_agent, interroger_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = creer_agent()
    yield


app = FastAPI(title="Agent Financier API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str
    status: str


@app.get("/")
def root():
    return {"status": "ok", "message": "Agent Financier API"}


@app.post("/api/agent/query", response_model=QueryResponse)
def query_agent(body: QueryRequest):
    try:
        response = interroger_agent(app.state.agent, body.query)
        return {"response": response, "status": "success"}
    except Exception as e:
        return {"response": str(e), "status": "error"}
