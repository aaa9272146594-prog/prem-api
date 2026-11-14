
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="PREM API",
    description="My Free Personal API",
    version="1.0.0"
)

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
        "message": "Welcome to PREM API",
        "developer": "PREM",
        "version": "1.0.0"
    }

@app.get("/api/hello")
def hello():
    return {"message": "Hello from PREM API"}

@app.get("/api/info")
def info():
    return {
        "name": "PREM API",
        "status": "online",
        "version": "1.0.0"
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
    op = data.operation

    if op == "add":
        result = a + b
    elif op == "subtract":
        result = a - b
    elif op == "multiply":
        result = a * b
    elif op == "divide":
        if b == 0:
            return {"success": False, "error": "Cannot divide by zero"}
        result = a / b
    else:
        return {"success": False, "error": "Invalid operation"}

    return {"success": True, "result": result}
