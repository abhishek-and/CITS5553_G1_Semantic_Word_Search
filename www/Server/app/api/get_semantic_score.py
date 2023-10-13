from fastapi import APIRouter
from pydantic import BaseModel

from app.lib.bert_model import process_csv_and_get_scores


router = APIRouter()


class QueryData(BaseModel):
    reference_number: str
    query: str


class WordsAndScores(BaseModel):
    words: list[str]
    semantic_scores: list[float]


@router.post("/api/getSemanticScores", response_model=WordsAndScores)
def get_semantic_scores(data: QueryData):
    words_list, semantic_scores = process_csv_and_get_scores(
        data.reference_number, data.query
    )
    return {"words": words_list, "semantic_scores": semantic_scores}
