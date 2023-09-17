from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

class filterJSON(BaseModel):
    query: str
    start_date: str
    end_date: str

class documentsJSON(BaseModel):
    documentName: str
    documentID: str
    similarityScore: str

@app.get("/api/getFilters")
def get_filters(user_query: str):
    return filterJSON(
        query=user_query,
        start_date="01-01-2023",
        end_date="31-12-2023"
    )

@app.post("/api/getDocuments")
def get_documents(filters: filterJSON):
    return documentsJSON(
        documentName="TestDocument",
        documentID="123456",
        similarityScore="0.98"
    )