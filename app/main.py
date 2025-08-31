from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pix2text import Pix2Text
import requests
import tempfile
import os
import re
from pathlib import Path
from PIL import Image

app = FastAPI()
pix2text_engine = Pix2Text()

# ADK endpoints (assumes local ADK API server is running)
BASE_ADK_URL = "http://localhost:8000"
CREATE_ENDPOINT = f"{BASE_ADK_URL}/apps/autograder"
QUERY_ENDPOINT = f"{BASE_ADK_URL}/run"

def transform(s: str) -> str:
    
    s = re.sub(r"\n\$\$\n", r"", s)
    s = re.sub(r"\$\$\n", r"\\", s)
    s = re.sub(r"\n\$\$", r"\\", s)
    return s

def replace_color(img_path, output_path=None, tolerance=20, threshold=100):
    img = Image.open(img_path).convert("RGB")
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if abs(r - g) <= tolerance and abs(r - b) <= tolerance and abs(g - b) <= tolerance:
                gray = int(round((r + g + b) / 3))
                if gray < threshold:
                    pixels[x, y] = (0, 0, 0)
                else:
                    pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (255, 255, 255)
    if output_path:
        img.save(output_path)

@app.post("/create")
async def create_session(
    userId: str = Form(...),
    sessionId: str = Form(...),
):
    payload = {}

    try:
        create_url = f"{CREATE_ENDPOINT}/users/{userId}/sessions/{sessionId}"
        response = requests.post(create_url, json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(content={"data": result})

@app.post("/grade")
async def grade_solution(
    question: str = Form(...),
    marking_scheme: str = Form(...),
    answer_text: str = Form(...),
    userId: str = Form(...),
    sessionId: str = Form(...),
):        
    try:
        # Prepare message payload for ADK
        full_prompt = (
            f"Question: {question}\n"
            f"MarkingScheme: {marking_scheme}\n"
            f"Answer: {answer_text}"
        )

        payload = {
            "appName": "autograder",
            "userId": userId,
            "sessionId": sessionId,
            "newMessage": {
                "role": "user",
                "parts": [{"text": full_prompt}]
            }
        }

        # Send to ADK agent
        response = requests.post(QUERY_ENDPOINT, json=payload)
        response.raise_for_status()
        result = response.json()

        return JSONResponse(content={
            "grading_result": result
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/recognize")
async def recognize_text(
    image: UploadFile | None = Form(None),
):
    try:
        if image is not None:
            
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Extract the file extension from the uploaded image
            filename = image.filename
            ext = Path(filename).suffix.lower()
            
            # Sanity check for allowed extensions
            answer_text = "[Unsupported file type. ]"
            if ext not in [".png", ".jpg", ".jpeg"]:
                return JSONResponse(status_code=400, content={"error": "Unsupported file type."})

            img_type = "text_formula"
            # Save the uploaded file temporarily with correct extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_path = tmp_file.name
                content = await image.read()
                tmp_file.write(content)
            
            output_path = os.path.join(output_dir, filename)
            replace_color(tmp_path, output_path=output_path)
            
            try:
                # Convert image to text using Pix2Text or other OCR engine
                extracted_text = pix2text_engine.recognize(output_path, file_type=img_type)
                answer_text = extracted_text if extracted_text else "[No text recognized]"
            finally:
                # Clean up
                os.remove(tmp_path)
            
        else:
            # Handle case with no image
            answer_text = "[No file submitted]"

        return JSONResponse(content={
            "answer_text": transform(answer_text)
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})