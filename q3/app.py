from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import google.generativeai as genai
import os
from datetime import datetime
import re
from typing import List, Dict, Any

app = FastAPI(title="Adaptive Prompt Optimizer", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Debug routes
@app.get("/debug")
async def debug():
    """Debug endpoint to check if API is working"""
    return {"status": "ok", "message": "API is working correctly"}

@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    """Test page to verify template rendering"""
    return templates.TemplateResponse(
        name="test.html", 
        context={"request": request, "tools": optimizer.supported_tools}
    )

# Import configuration
from config import Config

# Configure Gemini AI
genai.configure(api_key=Config.GEMINI_API_KEY)

print(f"Gemini API configured with key: {'*' * (len(Config.GEMINI_API_KEY) - 4) + Config.GEMINI_API_KEY[-4:] if Config.GEMINI_API_KEY != 'your-api-key-here' else 'NOT SET'}")

# Pydantic models
class OptimizeRequest(BaseModel):
    prompt: str
    tool: str

class OptimizeResponse(BaseModel):
    original_prompt: str
    optimized_prompt: str
    tool: str
    analysis: Dict[str, Any]
    optimizations_made: List[str]
    timestamp: str

class ToolInfo(BaseModel):
    name: str
    strengths: List[str]
    best_practices: List[str]

class PromptOptimizer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.supported_tools = {
            'copilot': {
                'name': 'GitHub Copilot',
                'strengths': ['Code completion', 'Function generation', 'Bug fixes'],
                'best_practices': [
                    'Use descriptive function names',
                    'Add type hints and docstrings',
                    'Be specific about desired functionality',
                    'Include context about the codebase'
                ]
            },
            'cursor': {
                'name': 'Cursor AI',
                'strengths': ['Code editing', 'Refactoring', 'Multi-file operations'],
                'best_practices': [
                    'Describe the current state and desired outcome',
                    'Be explicit about file locations',
                    'Use clear, actionable language',
                    'Mention specific technologies/frameworks'
                ]
            },
            'replit': {
                'name': 'Replit AI',
                'strengths': ['Full-stack development', 'Interactive coding', 'Deployment'],
                'best_practices': [
                    'Specify the programming language',
                    'Mention deployment requirements',
                    'Include package/dependency needs',
                    'Be clear about the project structure'
                ]
            },
            'codewhisperer': {
                'name': 'Amazon CodeWhisperer',
                'strengths': ['AWS integration', 'Security-focused code', 'Enterprise patterns'],
                'best_practices': [
                    'Mention AWS services if relevant',
                    'Include security considerations',
                    'Specify cloud architecture patterns',
                    'Use enterprise-grade terminology'
                ]
            },
            'tabnine': {
                'name': 'Tabnine',
                'strengths': ['Code completion', 'Pattern recognition', 'Team consistency'],
                'best_practices': [
                    'Use consistent naming conventions',
                    'Provide context about team coding style',
                    'Be specific about patterns to follow',
                    'Include relevant imports/dependencies'
                ]
            },
            'cody': {
                'name': 'Sourcegraph Cody',
                'strengths': ['Code search', 'Large codebase navigation', 'Code understanding'],
                'best_practices': [
                    'Reference specific files or functions',
                    'Use precise technical terminology',
                    'Include context about codebase structure',
                    'Mention related code patterns'
                ]
            },
            'claude': {
                'name': 'Claude (Anthropic)',
                'strengths': ['Code analysis', 'Architecture design', 'Complex reasoning'],
                'best_practices': [
                    'Provide comprehensive context',
                    'Ask for step-by-step explanations',
                    'Include architectural constraints',
                    'Request code review and suggestions'
                ]
            }
        }

    def analyze_prompt_intent(self, prompt):
        """Analyze the intent and complexity of the input prompt"""
        analysis_prompt = f"""
        Analyze this coding prompt and categorize it:
        
        Prompt: "{prompt}"
        
        Please provide a JSON response with:
        1. primary_intent: What is the main goal? (e.g., "code_generation", "debugging", "refactoring", "explanation", "optimization")
        2. complexity_level: Rate 1-5 (1=simple, 5=very complex)
        3. key_requirements: List of specific requirements mentioned
        4. missing_context: What additional context would be helpful
        5. technical_domains: Programming languages, frameworks, or technologies mentioned
        
        Return only valid JSON.
        """
        
        try:
            response = self.model.generate_content(analysis_prompt)
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback analysis
                return {
                    "primary_intent": "code_generation",
                    "complexity_level": 3,
                    "key_requirements": ["Basic functionality"],
                    "missing_context": ["Specific requirements"],
                    "technical_domains": ["General programming"]
                }
        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                "primary_intent": "code_generation",
                "complexity_level": 3,
                "key_requirements": ["Basic functionality"],
                "missing_context": ["Specific requirements"],
                "technical_domains": ["General programming"]
            }

    def optimize_for_tool(self, prompt, tool_id, analysis):
        """Generate optimized prompt for specific tool"""
        if tool_id not in self.supported_tools:
            return prompt, []

        tool_info = self.supported_tools[tool_id]
        
        optimization_prompt = f"""
        Optimize this coding prompt for {tool_info['name']}:
        
        Original Prompt: "{prompt}"
        
        Tool Strengths: {', '.join(tool_info['strengths'])}
        Best Practices: {', '.join(tool_info['best_practices'])}
        
        Intent Analysis: {json.dumps(analysis, indent=2)}
        
        Create an optimized version that:
        1. Leverages the tool's strengths
        2. Follows the tool's best practices
        3. Addresses missing context from the analysis
        4. Is more specific and actionable
        
        Provide:
        1. optimized_prompt: The improved prompt
        2. optimizations_made: List of specific changes and why they help
        
        Return as JSON only.
        """
        
        try:
            response = self.model.generate_content(optimization_prompt)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get('optimized_prompt', prompt), result.get('optimizations_made', [])
            else:
                return prompt, ["Unable to generate optimizations"]
        except Exception as e:
            print(f"Optimization error: {e}")
            return prompt, [f"Error during optimization: {str(e)}"]

# Initialize the optimizer
try:
    optimizer = PromptOptimizer()
    print("✓ PromptOptimizer initialized successfully")
except Exception as e:
    print(f"✗ Error initializing PromptOptimizer: {e}")
    # Create a fallback optimizer with minimal functionality
    class FallbackOptimizer:
        def __init__(self):
            self.supported_tools = {
                'copilot': {'name': 'GitHub Copilot', 'strengths': ['Testing'], 'best_practices': ['Testing']}
            }
        def analyze_prompt_intent(self, prompt):
            return {"primary_intent": "testing", "complexity_level": 1, "key_requirements": ["test"], 
                   "missing_context": ["test"], "technical_domains": ["test"]}
        def optimize_for_tool(self, prompt, tool_id, analysis):
            return f"Optimized: {prompt}", ["Test optimization"]
    
    optimizer = FallbackOptimizer()
    print("✓ Fallback optimizer initialized")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Make sure to pass the request object as required by Jinja2Templates
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request, "tools": optimizer.supported_tools}
    )

@app.post("/api/optimize", response_model=OptimizeResponse)
async def optimize_prompt(request: OptimizeRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    if request.tool not in optimizer.supported_tools:
        raise HTTPException(status_code=400, detail="Invalid tool selected")
    
    # Analyze the prompt
    analysis = optimizer.analyze_prompt_intent(request.prompt)
    
    # Optimize for the specific tool
    optimized_prompt, optimizations = optimizer.optimize_for_tool(
        request.prompt, request.tool, analysis
    )
    
    return OptimizeResponse(
        original_prompt=request.prompt,
        optimized_prompt=optimized_prompt,
        tool=optimizer.supported_tools[request.tool]['name'],
        analysis=analysis,
        optimizations_made=optimizations,
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/tools")
async def get_tools():
    return optimizer.supported_tools

if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration
    if not Config.validate_config():
        print("Configuration validation failed. Please check your settings.")
        exit(1)
    
    print(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    print(f"Server will run on http://{Config.HOST}:{8080}")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host=Config.HOST, port=8080, reload=Config.DEBUG) 