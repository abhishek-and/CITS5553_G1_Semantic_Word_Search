from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer

router = APIRouter()

# Initialize KeyBERT model
kb_model = KeyBERT()

class QueryJSON(BaseModel):
    query: str

class FilterOutput(BaseModel):
    query: str
    keywords: List[str]
    filters: Dict[str, Optional[str]]

@router.post("/api/getFilters", response_model=FilterOutput)
async def get_filters(query: QueryJSON):
    if not query.query:
        raise HTTPException(status_code=400, detail="Query is empty")

    # Extract keywords using KeyBERT
    vectorizer = CountVectorizer().build_analyzer()
    keywords = kb_model.extract_keywords(query.query, vectorizer=vectorizer, top_n=5)

    # Extract filters from query
    filters = extract_filters(query.query)

    return FilterOutput(
        query=query.query,
        keywords=[keyword for keyword, _ in keywords],
        filters=filters
    )

def extract_filters(query: str) -> Dict[str, Optional[str]]:
    # Implement your logic here to analyze the query and extract filters
    # This is a placeholder implementation.
    # You should replace it with your own logic to analyze the query and extract relevant information.
    filters = {}
    if "from:" in query:
        filters["startDate"] = query.split("from:")[1].split()[0]
    if "to:" in query:
        filters["endDate"] = query.split("to:")[1].split()[0]
    # Add more conditions as required
    return filters

# You can then run the server using uvicorn
