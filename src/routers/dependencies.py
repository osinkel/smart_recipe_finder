from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from src.database import get_session
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


Session = Annotated[AsyncSession, Depends(get_session)]

embedding_function: HuggingFaceEmbeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)