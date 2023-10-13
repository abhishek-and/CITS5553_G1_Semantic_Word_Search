from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import get_filters, get_documents, get_semantic_score

# from app.api import get_documents


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

app.include_router(get_filters.router)
app.include_router(get_documents.router)
app.include_router(get_semantic_score.router)
