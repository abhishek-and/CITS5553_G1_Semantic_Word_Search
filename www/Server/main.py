from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bert_model import process_csv_and_get_scores
from keyphrase_transformer import extract_info 
from typing import List
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}



class queryJSON(BaseModel):
    query: str

class QueryData(BaseModel):
    reference_number: str
    query: str

class WordsAndScores(BaseModel):
    words: list[str]
    semantic_scores: list[float]

class documentJSON(BaseModel):
    documentName: str
    documentID: str
    similarityScore: str

class filterJSON(BaseModel):
    query: str
    start_date: str
    end_date: str

class documentsJSON(BaseModel):
    documents: list[documentJSON]

class FilterOutput(BaseModel):
    query: str
    startDate: str
    endDate: str
    Range: List[int]
    typeOfWork: str
    UNSPSCcode: List[int]


@app.post("/api/getFilters", response_model=FilterOutput)
def get_filters(query: queryJSON):
    extracted_data = json.loads(extract_info(query.query))
    
    return FilterOutput(
        query=extracted_data["query"],
        startDate=extracted_data["startDate"],
        endDate=extracted_data["endDate"],
        Range=extracted_data["Range"],
        typeOfWork=extracted_data["typeOfWork"],
        UNSPSCcode=extracted_data["UNSPSCcode"]
    )

@app.post("/api/getDocuments")
def get_documents(filters: filterJSON):
    document = documentJSON(
        documentName=filters.query,
        documentID="123456",
        similarityScore="0.98"
    )
    return documentsJSON(documents=[document, document])

@app.post("/api/getSemanticScores", response_model=WordsAndScores)
def get_semantic_scores(data: QueryData):
    words_list, semantic_scores = process_csv_and_get_scores(data.reference_number, data.query)
    return {"words": words_list, "semantic_scores": semantic_scores}
