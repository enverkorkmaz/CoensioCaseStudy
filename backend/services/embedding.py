# services/embedding.py — Metni vektöre çevirir
from openai import OpenAI
from config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]:
    
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    embedding = response.data[0].embedding
    print(f"[Embedding] '{text[:50]}...' -> {len(embedding)} boyutlu vektör oluşturuldu")
    return embedding