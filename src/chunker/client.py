from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from src.core.settings import ChunkSettings


class ChunkerClient:
    def __init__(self, settings: ChunkSettings):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")],
            strip_headers=False,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def split_text(self, text: str, metadata: dict | None = None) -> List[Document]:
        documents = self.markdown_splitter.split_text(text)
        for document in documents:
            document.metadata.update(metadata or {})
        return self.text_splitter.split_documents(documents)

    def chunk_file(self, path: Path) -> List[Document]:
        with open(path, "r") as file:
            text = file.read()
        return self.split_text(text, {"source": str(path)})