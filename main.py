
import os
import secrets

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(
    title="PREM AI API",
    description="Personal AI Chat API",
    version="2.0.0"
)

MODEL = "gemini-3.8-flash"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class TextData(BaseModel):
    text: str


class CalculatorData(BaseModel):
    a: float
    b: float
    operation: str


@app.get("/")
def home():
    return {
        "success": True,
        "message": "Welcome to PREM AI API",
        "developer": "PREM",
        "version": "2.0.0"
    }


@app.get("/api/hello")
def hello():
    return {"message": "Hello from PREM API"}


@app.get("/api/info")
def info():
    return {
        "name": "PREM AI API",
        "status": "online",
        "version": "2.0.0"
    }


@app.post("/api/text")
def text_api(data: TextData):
    return {
        "success": True,
        "result": data.text
    }


@app.post("/api/calculate")
def calculate(data: CalculatorData):
    a, b = data.a, data.b

    if data.operation == "add":
        result = a + b
    elif data.operation == "subtract":
        result = a - b
    elif data.operation == "multiply":
        result = a * b
    elif data.operation == "divide":
        if b == 0:
            raise HTTPException(400, "Cannot divide by zero")
        result = a / b
    else:
        raise HTTPException(400, "Invalid operation")

    return {"success": True, "result": result}


@app.post("/api/chat")
def ai_chat(
    data: ChatRequest,
    x_api_key: str = Header(default="", alias="x-api-key")
):
    access_key = os.getenv("PREM_ACCESS_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not access_key or not gemini_key:
        raise HTTPException(503, "API secrets are not configured")

    if not secrets.compare_digest(x_api_key, access_key):
        raise HTTPException(401, "Invalid API access key")

    try:
        client = genai.Client(api_key=gemini_key)

        response = client.models.generate_content(
            model=MODEL,
            contents=data.message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are PREM AI, a friendly and helpful "
                    "assistant. Reply clearly and helpfully. "
                    "Reply in the language used by the user."
                ),
                temperature=0.7,
                max_output_tokens=800
            )
        )

        if not response.text:
            raise HTTPException(502, "AI returned an empty response")

        return {
            "success": True,
            "developer": "PREM",
            "reply": response.text,
            "model": MODEL
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            502,
            "Gemini request failed. Check API key, model or quota."
        )
