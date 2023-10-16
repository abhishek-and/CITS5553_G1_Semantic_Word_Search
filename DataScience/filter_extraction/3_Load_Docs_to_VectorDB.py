from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pandas as pd

from rich.progress import track

from lib.dataframe_loader import DataFrameLoader

# Load file
FILE_DIR = "/Users/jithfernandez/Documents/Uni Notes/Semester 3/CITS5553 Capstone Project/CITS5553_G1_Semantic_Word_Search/Dataset/Contracts_Dataset_With_Extract.csv"
df = pd.read_csv(FILE_DIR, index_col=False)

# Transform NAs to empty string
df = df.fillna("")

# Transform date to timestamp
df["Tender Closing Date Timestamp"] = pd.to_datetime(
    df["Tender Closing Date"], format="%Y-%m-%d %H:%M:%S"
)
df["Tender Closing Date Timestamp"] = df["Tender Closing Date Timestamp"].apply(
    lambda x: int(x.strftime("%Y%m%d%H%M%S"))
)

# Load data frame into a list of documents
loader = DataFrameLoader(df, page_content_columns=["Description", "Tenders Content"])
data = loader.load()


def chunk_docs(
    docs: list[Document], max_chunk_size: int, overlap: int = -1
) -> list[Document]:
    """
    Chunk documents into smaller documents
    :param docs: Documents
    :param metadatas: Documents metadata
    :param max_chunk_size:
    :param overlap: - if -1 then overlap is 10% of max_chunk_size
    :return:
    """
    _overlap = overlap
    if _overlap == -1:
        _overlap = int(max_chunk_size * 0.1)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size, chunk_overlap=_overlap, add_start_index=True
    )
    _out_docs = text_splitter.split_documents(docs)
    return _out_docs


# Load documents into vector database
docs = chunk_docs(data, 512)
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2", model_kwargs={"device": "mps"}
)


# sqlite db has a limit to the number of rows it can store at once
def split_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]


split_docs_chunked = split_list(docs, 41000)

for split_docs_chunk in track(split_docs_chunked, description="Loading..."):
    vectordb = Chroma.from_documents(
        documents=split_docs_chunk,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_metadata={"hnsw:space": "cosine"},
    )
    vectordb.persist()
