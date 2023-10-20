from fastapi import APIRouter
from pydantic import BaseModel
from app.lib.keyphrase_transformer import extract_info

from typing import Optional

router = APIRouter()


class queryJSON(BaseModel):
    query: str


class FilterOutput(BaseModel):
    query: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    Range: Optional[list[int]] = None
    typeOfWork: Optional[str] = None
    UNSPSCcode: Optional[list[int]] = None


@router.post("/api/getFilters", response_model=FilterOutput)
def get_filters(query: queryJSON):
    extracted_data = extract_info(query.query)

    return FilterOutput(
        query=extracted_data["query"],
        startDate=extracted_data["startDate"],
        endDate=extracted_data["endDate"],
        Range=extracted_data["Range"],
        typeOfWork=extracted_data["typeOfWork"],
        UNSPSCcode=extracted_data["UNSPSCcode"],
    )
