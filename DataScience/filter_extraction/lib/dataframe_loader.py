from typing import Any, Iterator, List, Optional
from pandas import DataFrame

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class BaseDataFrameLoader(BaseLoader):
    def __init__(
        self,
        data_frame: DataFrame,
        *,
        page_content_columns: List[str],
        source_column: Optional[str] = None,  # < ADDED
        metadata_columns: Optional[List[str]] = None,  # < ADDED
    ):
        """Initialize with dataframe object.

        Args:
            data_frame: DataFrame object.
            page_content_column: Name of the column containing the page content.
              Defaults to "text".
        """
        self.data_frame = data_frame
        self.page_content_columns = page_content_columns
        self.source_column = source_column  # < ADDED
        self.metadata_columns = metadata_columns  # < ADDED

    def lazy_load(self) -> Iterator[Document]:
        """Lazy load records from dataframe."""

        for i, row in self.data_frame.iterrows():
            content = "\n".join(
                f"{str(k).strip()}: {str(v).strip()}" for k, v in row.items()
            )
            metadata = row.to_dict()
            for column_name in self.page_content_columns:
                metadata.pop(column_name)
            metadata["row"] = i
            yield Document(page_content=content, metadata=metadata)

    def load(self) -> List[Document]:
        """Load full dataframe."""
        return list(self.lazy_load())


class DataFrameLoader(BaseDataFrameLoader):
    """Load `Pandas` DataFrame."""

    def __init__(self, data_frame: Any, page_content_columns: List[str]):
        """Initialize with dataframe object.

        Args:
            data_frame: Pandas DataFrame object.
            page_content_column: Name of the column containing the page content.
              Defaults to "text".
        """
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "Unable to import pandas, please install with `pip install pandas`."
            ) from e

        if not isinstance(data_frame, pd.DataFrame):
            raise ValueError(
                f"Expected data_frame to be a pd.DataFrame, got {type(data_frame)}"
            )
        super().__init__(data_frame, page_content_columns=page_content_columns)
