import nest_asyncio
import uvicorn
import json
import logging
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="**************",
)
logging.basicConfig(level=logging.INFO)

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/junior_entreprise")
async def junior_check():
    """Simple junior check endpoint."""
    return {"status": "running"}

def get_junior_enterprises_info(query: str):
    """Queries the Llama API to get information about Junior Enterprises based on the user's query."""
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",  
            messages=[{
                    "role": "system",
                    "content": (
                        "You are a knowledgeable assistant.Output JSON only that specializes in providing detailed information about Junior Enterprises"
                        "worldwide. When the user asks for information about a specific Junior Enterprise, you should return the following details in a structured format:\n"
                        "{\n"
                        '  "name": "<name of the Junior Enterprise>",\n'
                        '  "country": "<country where the Junior Enterprise is based>",\n'
                        '  "services": "<description of services provided by the Junior Enterprise>",\n'
                        '  "description": "<brief description of the Junior Enterprise>",\n'
                        '  "website": "<official website URL of the Junior Enterprise>",\n'
                        '  "facebook": "<link to the Facebook page of the Junior Enterprise>",\n'
                        '  "instagram": "<link to the Instagram profile of the Junior Enterprise>",\n'
                        '  "linkedin": "<link to the LinkedIn profile of the Junior Enterprise>",\n'
                        '  "email": "<contact email of the Junior Enterprise>"\n'
                        "}\n"
                        "Your response should be a clean JSON object, with all fields included. If any of the fields are not available, return 'N/A' for those fields. "
                        "Make sure the data returned is accurate and formatted correctly. Only return valid JSON and nothing else. Ensure you respond only with the requested information, no extra commentary."
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        
        response_content = completion.choices[0].message.content
        logging.info(f"🔍 Raw Llama API Response: {response_content}")
        try:
            ai_response = json.loads(response_content)
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON Parsing Error: {e}")
            raise HTTPException(status_code=500, detail="Error in parsing the response from Llama.")

        return ai_response

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing the request.")

@app.post("/search_junior_enterprises", response_model=SearchResult)
async def search_junior_enterprises(request: SearchRequest):
    """Search for Junior Enterprises using Llama API based on the user's query."""
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query is required.")

    try:
        junior_enterprise_info = get_junior_enterprises_info(query)
        if not isinstance(junior_enterprise_info, list):
            raise HTTPException(status_code=500, detail="Invalid format returned from Llama.")
        enterprises = []
        for item in junior_enterprise_info:
            enterprise = JuniorEnterprise(
                name=item.get('name', 'N/A'),
                country=item.get('country', 'N/A'),
                services=item.get('services', 'N/A'),
                website=item.get('website', 'N/A'),
                facebook=item.get('facebook', 'N/A'),
                instagram=item.get('instagram', 'N/A'),
                linkedin=item.get('linkedin', 'N/A'),
                email=item.get('email', 'N/A'),
                description=item.get('description', 'N/A')
            )
            enterprises.append(enterprise)

        return SearchResult(total_results=len(enterprises), enterprises=enterprises)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing the request.")

# Run FastAPI inside Jupyter or as a standalone script
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)
