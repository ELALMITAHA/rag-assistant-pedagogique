from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv, find_dotenv
import os

# ***** LOAD ENV *****
load_dotenv(find_dotenv())

# ***** SINGLETON MODELS *****

EMBEDDINGS = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
)

LLM = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    api_key=os.getenv("MISTRAL_API_KEY")
)

RERANKER = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)