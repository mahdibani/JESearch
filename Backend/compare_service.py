import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
    api_key="********",  
)

# Define Junior Enterprise
MY_JUNIOR = {
    "name": "My Junior Enterprise",
    "services": "Web and Desktop Development, Graphic Design, Mobile Development, Community Management",
    "description": "Project Department, Foreign Affairs Department, Marketing Department, commercial development and prospecting."
}


class ComparisonRequest(BaseModel):
    services: str = Field(..., min_length=1, example="Web Development")
    description: str = Field(..., min_length=1, example="Technical services")
    name: str = Field(..., min_length=1, example="Example JE")

def compute_similarity(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return round(float(similarity[0][0]) * 100, 2)  # Convert to percentage

def get_collaboration_suggestions(name: str, services: str, description: str, score: float) -> str:
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides tailored collaboration suggestions for Junior Enterprises."},
                {"role": "user", "content": f"""Based on a similarity score of {score}%, suggest a possible collaboration opportunity between these two Junior Enterprises:
                
                INceptum JE Services: {MY_JUNIOR['services']}
                INceptum JE Description: {MY_JUNIOR['description']}
                
                {name} Services: {services}
                {name} Description: {description}

                Provide recommendations specifically mentioning both 'INceptum JE' and '{name}' in your response."""}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error fetching response from Llama 3: {str(e)}")
        return "Error generating suggestions. Please try again."
@app.post("/compare_junior_enterprise")
async def compare_junior_enterprise(request: ComparisonRequest):
    try:
        # Validate input data
        if not all([request.services.strip(), request.description.strip(), request.name.strip()]):
            raise HTTPException(
                status_code=400,
                detail="All fields must contain non-whitespace characters"
            )
            
        service_similarity = compute_similarity(request.services, MY_JUNIOR["services"])
        description_similarity = compute_similarity(request.description, MY_JUNIOR["description"])
        final_score = round((service_similarity + description_similarity) / 2, 2)
        
        recommendations = get_collaboration_suggestions(
            request.name, 
            request.services,
            request.description, 
            final_score
        )
        
        return {
            "similarity_score": final_score,
            "recommendations": recommendations,
            "jeName": request.name,  # Add these fields
            "jeServices": request.services,
            "jeDescription": request.description
        }
        
    except HTTPException as he:
        logging.error(f"Validation error: {he.detail}")
        raise he
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
# Run FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8099)
