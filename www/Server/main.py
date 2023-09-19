from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    start_date: str
    end_date: str


class documentJSON(BaseModel):
    documentName: str
    documentID: str
    similarityScore: str


class documentsJSON(BaseModel):
    documents: list[documentJSON]


@app.post("/api/getFilters")
def get_filters(query: queryJSON):
    return filterJSON(query=query.query, start_date="01-01-2023", end_date="31-12-2023")


@app.post("/api/getDocuments")
def get_documents(filters: filterJSON):
    document = documentJSON(
        documentName=filters.query, documentID="123456", similarityScore="0.98"
    )
    return documentsJSON(documents=[document, document])
