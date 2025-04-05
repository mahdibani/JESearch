from pydantic import BaseModel, Field
from typing import List

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search term to find Junior Enterprises")
    search_type: str = Field(..., description="Search type: 'name', 'country', or 'services'")

class JuniorEnterprise(BaseModel):
    name: str = Field(..., description="Name of the Junior Enterprise")
    country: str = Field(..., description="Country of the Junior Enterprise")
    services: List[str] = Field(..., description="List of services offered by the Junior Enterprise")
    website: str = Field(None, description="Website URL of the Junior Enterprise")
    description: str = Field(None, description="Description of the Junior Enterprise")

class SearchResult(BaseModel):
    total_results: int = Field(..., description="Total number of Junior Enterprises found")
    enterprises: List[JuniorEnterprise] = Field(..., description="List of Junior Enterprises found")
