from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from transformers import AutoTokenizer, AutoModel
import torch

router = APIRouter()

# Load pre-trained model tokenizer
tokenizer = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")

# Load pre-trained model
model = AutoModel.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")

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

    # Tokenize input text
    inputs = tokenizer(query.query, return_tensors="pt")

    # Get embeddings for input text
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state

    # Calculate average embedding for entire input text
    text_embedding = torch.mean(embeddings, dim=1)

    # Calculate cosine similarity between entire text and each token
    similarities = torch.nn.functional.cosine_similarity(embeddings.squeeze(), text_embedding.squeeze())

    # Get indices of top 5 tokens
    top_tokens = torch.topk(similarities, 5).indices

    # Convert token indices to words
    keywords = [tokenizer.convert_ids_to_tokens(idx.item()) for idx in top_tokens]

    # Extract filters from query
    filters = extract_filters(query.query)

    return FilterOutput(
        query=query.query,
        keywords=keywords,
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
