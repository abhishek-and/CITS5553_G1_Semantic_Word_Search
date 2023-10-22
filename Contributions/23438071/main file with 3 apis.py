from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model1 import extract_keywords_from_query

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

class filterJSON(BaseModel):
    query: str
    date_type: str
    start_date: str
    end_date: str
    cost_range_type: str
    start_range: int
    end_range: int
    unspsc_code: list[int]
    region: str

class documentJSON(BaseModel):
    documentName: str
    documentID: str
    similarityScore: str

class documentsJSON(BaseModel):
    documents: list[documentJSON]

@app.post("/api/getFilters")
def get_filters(query: queryJSON):
    extracted_data = extract_keywords_from_query(query.query)
    return extracted_data

@app.post("/api/getDocuments")
def get_documents(filters: filterJSON):
    document = documentJSON(
        documentName=filters.query, documentID="123456", similarityScore="0.98"
    )
    return documentsJSON(documents=[document, document])

word_match_example = {
    "abc": "def",
    "ghi": "jkl",
    "mno": "pqr",
}

@app.get("/api/getMatchingWords")
def get_matching_words():
    return word_match_example
