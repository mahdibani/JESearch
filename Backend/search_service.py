import nest_asyncio
import uvicorn
import json
import logging
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

nest_asyncio.apply()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="*****",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search term to find Junior Enterprises")

class JuniorEnterprise(BaseModel):
    name: str = Field(..., description="Name of the Junior Enterprise")
    country: str = Field(..., description="Country of the Junior Enterprise")
    services: str = Field(..., description="Services provided by the Junior Enterprise")
    website: str = Field(None, description="Website URL of the Junior Enterprise")
    facebook: str = Field(None, description="Facebook URL of the Junior Enterprise")
    instagram: str = Field(None, description="Instagram URL of the Junior Enterprise")
    linkedin: str = Field(None, description="LinkedIn URL of the Junior Enterprise")
    email: str = Field(None, description="Email of the Junior Enterprise")
    description: str = Field(None, description="Description of the Junior Enterprise")

class SearchResult(BaseModel):
    total_results: int = Field(..., description="Total number of Junior Enterprises found")
    enterprises: list = Field(..., description="List of Junior Enterprises found")

@app.get("/junior_entreprise")
async def junior_check():
    return {"status": "running"}

def get_junior_enterprises_info(query: str):
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[{
                "role": "system",
                "content": """... (keep your system message here) ..."""
            }, {
                "role": "user",
                "content": query
            }]
        )

        response_content = completion.choices[0].message.content
        logging.info(f"🔍 Raw Llama API Response: {response_content}")

        try:
            return json.loads(response_content)
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON Parsing Error: {e}")
            raise HTTPException(status_code=500, detail="Error parsing response from Llama.")

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing request.")

@app.post("/search_junior_enterprises", response_model=SearchResult)
async def search_junior_enterprises(request: SearchRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is required.")

    try:
        junior_enterprise_info = get_junior_enterprises_info(query)
        if not isinstance(junior_enterprise_info, list):
            raise HTTPException(status_code=500, detail="Invalid format from Llama.")

        enterprises = []
        for item in junior_enterprise_info:
            enterprise = JuniorEnterprise(**{k: item.get(k, 'N/A') for k in JuniorEnterprise.__fields__})
            enterprises.append(enterprise)

        return SearchResult(total_results=len(enterprises), enterprises=enterprises)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing request.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)
