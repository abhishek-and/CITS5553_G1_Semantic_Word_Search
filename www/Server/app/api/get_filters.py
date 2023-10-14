from fastapi import APIRouter
from pydantic import BaseModel
from app.lib.keyphrase_transformer import extract_info

router = APIRouter()


class queryJSON(BaseModel):
    query: str


class FilterOutput(BaseModel):
    query: str
    startDate: str | None = None
    endDate: str | None = None
    Range: list[int] | None = None
    typeOfWork: str | None = None
    UNSPSCcode: list[int] | None = None


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
