from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os

# Load agents knowledge base from JSON file
def load_agents_knowledge():
    file_path = os.path.join(os.path.dirname(__file__), 'agentdb.json')
    with open(file_path, 'r') as f:
        return json.load(f)

AGENTS_KNOWLEDGE = load_agents_knowledge()

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Warning: Failed to initialize Gemini API: {str(e)}")
    model = None

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent knowledge base
class TaskRequest(BaseModel):
    description: str
    language: str = ""
    complexity: str = "medium"

class AgentRecommendation(BaseModel):
    id: str
    name: str
    score: float
    explanation: str

@app.get("/")
async def root():
    return {"message": "AI Coding Agent Recommendation System"}

async def analyze_task_with_gemini(task_description: str, language: str, complexity: str) -> dict:
    """Analyze the task using Gemini API to determine the best agent fit."""
    if not model:
        return {}
        
    prompt = f"""Analyze the following coding task and determine the most suitable type of AI coding assistant.
    
    Task: {task_description}
    Language: {language if language else 'Not specified'}
    Complexity: {complexity}
    
    Consider the following aspects of the task:
    1. Required technical skills and programming languages
    2. Complexity level and scope
    3. Whether it's a new project, debugging, refactoring, or learning
    4. Need for IDE integration, collaboration features, or cloud capabilities
    
    Return a JSON object with the following structure:
    {{
        "required_skills": ["list", "of", "relevant", "skills"],
        "task_type": "e.g., web_development, data_analysis, learning, debugging, etc.",
        "recommended_features": ["list", "of", "important", "features"]
    }}
    """
    
    try:
        response = await model.generate_content_async(prompt)
        # Extract JSON from the response
        import json
        import re
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {}
    except Exception as e:
        print(f"Error analyzing task with Gemini: {str(e)}")
        return {}

def calculate_agent_score(agent: Dict[str, Any], task: TaskRequest, gemini_analysis: dict) -> float:
    """Calculate a score for how well an agent matches the task requirements."""
    score = 0.0
    
    # Base score for language support
    if task.language and task.language.lower() in [lang.lower() for lang in agent["languages"]]:
        score += 3.0
    
    # Complexity bonus
    complexity_bonus = {
        "low": 0.5,
        "medium": 1.0,
        "high": 1.5
    }.get(task.complexity.lower(), 1.0)
    score += 2.0 * complexity_bonus
    
    # Gemini analysis scoring
    if gemini_analysis:
        # Check if agent's strengths match required features
        required_features = gemini_analysis.get("recommended_features", [])
        agent_strengths = [s.lower() for s in agent["strengths"]]
        
        for feature in required_features:
            if any(word in feature.lower() for word in agent_strengths):
                score += 1.5
        
        # Check if agent is good for the task type
        task_type = gemini_analysis.get("task_type", "").lower()
        best_for = [bf.lower() for bf in agent["best_for"]]
        
        if any(bf in task_type for bf in best_for):
            score += 2.0
    
    # Add some randomness to avoid ties
    import random
    score += random.uniform(0, 0.5)
    
    return round(score, 2)

def generate_explanation(agent: Dict[str, Any], task: TaskRequest, gemini_analysis: dict = None) -> str:
    """Generate a human-readable explanation for the recommendation."""
    reasons = []
    
    # Language support
    if task.language and task.language.lower() in [lang.lower() for lang in agent["languages"]]:
        reasons.append(f"supports {task.language}")
    
    # Task type matching
    if gemini_analysis and gemini_analysis.get("task_type"):
        task_type = gemini_analysis["task_type"].replace("_", " ")
        reasons.append(f"ideal for {task_type} tasks")
    else:
        reasons.append(f"excels at {', '.join(agent['best_for'])}")
    
    # Complexity handling
    if task.complexity == "high":
        reasons.append("excels at complex tasks")
    
    # Specific strengths
    if gemini_analysis and gemini_analysis.get("recommended_features"):
        matched_features = []
        agent_strengths = [s.lower() for s in agent["strengths"]]
        
        for feature in gemini_analysis["recommended_features"]:
            if any(word in feature.lower() for word in agent_strengths):
                matched_features.append(feature)
        
        if matched_features:
            reasons.append(f"offers {', '.join(matched_features[:2])}")
    
    # Fallback if no specific reasons
    if not reasons:
        reasons.append("is a well-rounded coding assistant")
    
    return f"Recommended because it {', '.join(reasons)}."

@app.post("/recommend", response_model=List[AgentRecommendation])
async def recommend_agents(task: TaskRequest):
    """Get recommendations for the best coding agents for a given task."""
    # Analyze task with Gemini
    gemini_analysis = await analyze_task_with_gemini(
        task.description,
        task.language,
        task.complexity
    )
    print(gemini_analysis,"gemini_analysis")
    
    # Calculate scores for all agents
    scored_agents = []

    for agent in AGENTS_KNOWLEDGE:
        score = calculate_agent_score(agent, task, gemini_analysis)
        explanation = generate_explanation(agent, task, gemini_analysis)
        
        scored_agents.append({
            **agent,
            "score": score,
            "explanation": explanation,
            "analysis": gemini_analysis if score > 0 else None  # Include analysis for top agents
        })
    
    # Sort by score (descending) and get top 3
    top_agents = sorted(scored_agents, key=lambda x: x["score"], reverse=True)[:3]
    
    # Format response
    recommendations = []
    for agent in top_agents:
        recommendations.append({
            "id": agent["id"],
            "name": agent["name"],
            "score": agent["score"],
            "explanation": agent["explanation"],
            "analysis": agent.get("analysis")
        })
    
    return recommendations
