import sys
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)
logger = logging.getLogger(__name__)
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# --- Path setup ---
# Add project root to the Python path to resolve module imports
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Get the absolute path to the directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

from app.ai_service import get_math_solution, get_math_hint
from app.parser import LLMResponseParser

app = FastAPI()

# --- Templates and Static Files ---
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

parser = LLMResponseParser()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "MathTutor AI"})

@app.post("/solve", response_class=JSONResponse)
async def solve_problem(
    problem_text: str = Form(None),
    problem_image: UploadFile = File(None)
):
    if not problem_text and not problem_image:
        raise HTTPException(
            status_code=400,
            detail="Either problem_text or problem_image must be provided"
        )

    image_data = None
    if problem_image:
        image_data = await problem_image.read()

    try:
        llm_response = await get_math_solution(problem_text=problem_text, image_data=image_data)
        if llm_response is None:
            raise HTTPException(status_code=500, detail="Failed to get a response from the AI tutor.")
        
        # Parse the LLM response
        parsed_solution = parser.parse_solution(llm_response)
        
        return JSONResponse(content=parsed_solution) # Return the parsed solution
    except ValueError as ve:
        # This will catch errors from the parser as well
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.post("/hint", response_class=JSONResponse)
async def get_hint(
    problem_text: str = Form(None),
    problem_image: UploadFile = File(None)
):
    if not problem_text and not problem_image:
        raise HTTPException(
            status_code=400,
            detail="Either problem_text or problem_image must be provided"
        )

    image_data = None
    if problem_image:
        image_data = await problem_image.read()

    try:
        hint_response = await get_math_hint(problem_text=problem_text, image_data=image_data)
        if hint_response is None:
            raise HTTPException(status_code=500, detail="Failed to get a hint from the AI tutor.")
        
        # Parse the hint response
        parsed_hint = parser.parse_hint(hint_response)
        
        return JSONResponse(content=parsed_hint)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

