import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="*****",
)

MY_JUNIOR = {
    "name": "My Junior Enterprise",
    "services": "Web and Desktop Development, Graphic Design, Mobile Development, Community Management",
    "description": "Project Department, Foreign Affairs Department, Marketing Department, commercial development and prospecting."
}

class MessageRequest(BaseModel):
    je_name: str = Field(..., min_length=1)
    je_services: str = Field(..., min_length=1)
    je_description: str = Field(..., min_length=1)
    recommendations: str = Field(..., min_length=1)

@app.post("/generate_collaboration_message")
async def generate_collaboration_message(request: MessageRequest):
    try:
        if not all([
            request.je_name.strip(),
            request.je_services.strip(),
            request.je_description.strip(),
            request.recommendations.strip()
        ]):
            raise HTTPException(status_code=400, detail="All fields must contain non-whitespace characters")

        prompt = f"""... (keep your email generation prompt here) ..."""
        
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert in writing professional business emails for Junior Enterprises."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {"message": completion.choices[0].message.content.strip()}
    
    except HTTPException as he:
        logging.error(f"Validation error: {he.detail}")
        raise he
    except Exception as e:
        logging.error(f"Generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate message")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8066)
