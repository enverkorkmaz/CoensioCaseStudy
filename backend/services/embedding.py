import logging
from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY, EMBEDDING_MODEL

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]:
    try:
        response = client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL
        )
        embedding = response.data[0].embedding
        logger.info(f"Embedding oluşturuldu: '{text[:50]}...' -> {len(embedding)} boyut")
        return embedding
    except OpenAIError as e:
        logger.error(f"OpenAI embedding hatası: {e}")
        raise
