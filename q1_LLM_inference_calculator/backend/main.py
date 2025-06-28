from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List, Literal
from pydantic import BaseModel
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import math
from enum import Enum

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()
# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model configurations
class HardwareType(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    TPU = "tpu"

class ModelSize(str, Enum):
    SMALL = "7B"
    MEDIUM = "13B"
    LARGE = "GPT-4"

class DeploymentMode(str, Enum):
    CLOUD = "cloud"
    ON_PREM = "on_prem"
    EDGE = "edge"

class InferenceRequest(BaseModel):
    model_size: ModelSize
    input_tokens: int
    output_tokens: int
    batch_size: int = 1
    hardware_type: HardwareType
    deployment_mode: DeploymentMode

class InferenceMetrics(BaseModel):
    latency_seconds: float
    memory_gb: float
    cost_per_request: float
    hardware_compatibility: str

def calculate_inference_metrics(request: InferenceRequest) -> InferenceMetrics:
    """Calculate inference metrics based on model size and hardware."""
    # Base values for 7B model
    base_latency = 0.05  # seconds per token
    base_memory = 14  # GB
    base_cost = 0.00002  # $ per 1K tokens
    
    # Adjust based on model size
    size_multiplier = {
        ModelSize.SMALL: 1.0,
        ModelSize.MEDIUM: 1.8,
        ModelSize.LARGE: 10.0  # GPT-4 is significantly larger
    }[request.model_size]
    
    # Adjust based on hardware
    hardware_multiplier = {
        HardwareType.CPU: 10.0,
        HardwareType.GPU: 1.0,
        HardwareType.TPU: 0.5
    }[request.hardware_type]
    
    # Adjust based on deployment mode
    deployment_multiplier = {
        DeploymentMode.CLOUD: 1.2,  # Higher cost for cloud services
        DeploymentMode.ON_PREM: 1.0,
        DeploymentMode.EDGE: 1.5  # Higher cost for edge deployment
    }[request.deployment_mode]
    
    # Calculate metrics
    total_tokens = request.input_tokens + request.output_tokens
    latency = (
        (base_latency * size_multiplier * total_tokens) / 
        (request.batch_size * (1 / hardware_multiplier))
    )
    
    memory = base_memory * size_multiplier
    
    # Cost calculation (simplified)
    cost_per_1k = base_cost * size_multiplier * deployment_multiplier
    cost = (total_tokens / 1000) * cost_per_1k
    
    # Hardware compatibility
    if request.hardware_type == HardwareType.CPU and request.model_size != ModelSize.SMALL:
        compatibility = "Not recommended for this model size"
    else:
        compatibility = "Compatible"
    
    return InferenceMetrics(
        latency_seconds=round(latency, 4),
        memory_gb=round(memory, 2),
        cost_per_request=round(cost, 6),
        hardware_compatibility=compatibility
    )

vision_model = genai.GenerativeModel("gemini-2.0-flash")
text_model = genai.GenerativeModel("gemini-2.0-flash")

def load_image_from_url(url: str):
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except Exception as e:
        return None

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    image: Optional[UploadFile] = None,
    image_url: Optional[str] = Form(None)
):
    img = None
    if image:
        img = Image.open(BytesIO(await image.read()))
    elif image_url:
        img = load_image_from_url(image_url)

    try:
        if img:
            response = vision_model.generate_content([question, img])
        else:
            response = text_model.generate_content(question)

        return JSONResponse(content={
            "answer": response.text,
            "used_model": "gemini-2.0-flash" if img else "gemini-2.0-flash"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e)
        })

@app.post("/calculate-inference")
async def calculate_inference(request: InferenceRequest):
    """Calculate LLM inference metrics based on model and hardware parameters."""
    try:
        metrics = calculate_inference_metrics(request)
        return {
            "latency_seconds": metrics.latency_seconds,
            "memory_gb": metrics.memory_gb,
            "cost_per_request": metrics.cost_per_request,
            "hardware_compatibility": metrics.hardware_compatibility,
            "model_size": request.model_size,
            "hardware_type": request.hardware_type,
            "deployment_mode": request.deployment_mode
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
