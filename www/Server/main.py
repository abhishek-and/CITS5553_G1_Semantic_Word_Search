from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from bert_model import process_csv_and_get_scores
from keyphrase_transformer import extract_info
import json
from typing import List, Optional

from datetime import datetime

from langchain.embeddings import SentenceTransformerEmbeddings
from lib.chroma import Chroma

from datetime import datetime
from chromadb.api.types import Where

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


@dataclass
class filterJSON(BaseModel):
    query: str
    startDate: str | None = None
    endDate: str | None = None
    Range: list[int] | None = None
    typeOfWork: str | None = None
    UNSPSCcode: list[int] | None = None

    def get_filters(self) -> Where | None:
        filters = {"$and": []}
        if self.startDate:
            filters["$and"].append(
                {"Tender Closing Date Timestamp": {"$gte": format_date(self.startDate)}}
            )
        if self.endDate:
            filters["$and"].append(
                {"Tender Closing Date Timestamp": {"$lte": format_date(self.endDate)}}
            )
        if self.Range:
            filters["$and"].append(
                {
                    "Revised Contract Value": {
                        "$gte": self.Range[0],
                    }
                }
            )
            filters["$and"].append(
                {
                    "Revised Contract Value": {
                        "$lte": self.Range[1],
                    }
                }
            )
        if self.typeOfWork:
            filters["$and"].append({"Type of Work": self.typeOfWork})
        if self.UNSPSCcode:
            filters["$and"].append({"UNSPSC Code": {"$in": self.UNSPSCcode}})
        if len(filters["$and"]) == 1:
            filters = filters["$and"][0]
        elif len(filters["$and"]) == 0:
            filters = None
        return filters


class documentJSON(BaseModel):
    client_agency: str
    contract_title: str
    # description: str
    procurement_method: str
    reference_number: str
    revised_contract_value: float
    supplier_name: str
    tender_closing_date: datetime
    # tenders_content: Optional[str]
    type_of_work: str
    unspsc_code: int
    unspsc_title: str
    similarity_score: float
    sentence_piece: str


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
        UNSPSCcode=extracted_data["UNSPSCcode"],
    )


def format_date(date_string: str, date_format: str = "%Y-%m-%d") -> int:
    # date_format = "%Y-%m-%d %H:%M:%S"
    # Convert string to datetime object
    date_object = datetime.strptime(date_string, date_format)
    # Convert datetime object to "YYYYMMDDHHMMSS" format
    return int(date_object.strftime("%Y%m%d%H%M%S"))


@app.post("/api/getDocuments")
def get_documents(filters: filterJSON):
    model = "all-MiniLM-L6-v2"
    embeddings = SentenceTransformerEmbeddings(model_name=model)
    db_disk = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"},
    )

    query_embedding = embeddings.embed_query(filters.query)

    num_filtered_docs = len(db_disk.get(where=filters.get_filters())["documents"])

    k_filtered = int(num_filtered_docs * 0.95)

    matching_docs = db_disk.similarity_search_by_vector_with_relevance_scores(
        query_embedding, k=k_filtered, filter=filters.get_filters()
    )

    result_dict = {}
    for doc, score in matching_docs:
        row_id = doc.metadata["row"]
        if row_id not in result_dict:
            doc.metadata["similarity_score"] = score
            result_dict[row_id] = doc.metadata
            result_dict[row_id]["sentence_piece"] = doc.page_content
            result_dict[row_id].pop("row")
            result_dict[row_id].pop("start_index")
        else:
            if result_dict[row_id]["similarity_score"] > score:
                result_dict[row_id]["similarity_score"] = score
                result_dict[row_id]["sentence_piece"] = doc.page_content

    values_list = list(result_dict.values())

    documents = [
        documentJSON(
            client_agency=item["Client Agency"],
            contract_title=item["Contract Title"],
            procurement_method=item["Procurement Method"],
            reference_number=item["Reference Number"],
            revised_contract_value=item["Revised Contract Value"],
            supplier_name=item["Supplier Name"],
            tender_closing_date=item["Tender Closing Date"],
            type_of_work=item["Type of Work"],
            unspsc_code=item["UNSPSC Code"],
            unspsc_title=item["UNSPSC Title"],
            similarity_score=item["similarity_score"],
            sentence_piece=item["sentence_piece"],
        )
        for item in values_list
    ]

    return documentsJSON(documents=documents)


@app.post("/api/getSemanticScores", response_model=WordsAndScores)
def get_semantic_scores(data: QueryData):
    words_list, semantic_scores = process_csv_and_get_scores(
        data.reference_number, data.query
    )
    return {"words": words_list, "semantic_scores": semantic_scores}
