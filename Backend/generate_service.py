import uvicorn, nest_asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
import json
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
    api_key="*********", 
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
        prompt = f"""Create a formal collaboration email from INceptum JE to {request.je_name} based on these recommendations: {request.recommendations}
        
        Include these details:
        - INceptum JE services: {MY_JUNIOR['services']}
        - {request.je_name} services: {request.je_services}
        - Keep it professional but friendly
        - Use proper business email format
        - Include our website: https://inceptumje.tn/
        - Signature: INceptum JE Team"""

        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert in writing professional business emails for Junior Enterprises."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {"message": completion.choices[0].message.content.strip()}
    
    except Exception as e:
        logging.error(f"Message generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate message")
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8066)
