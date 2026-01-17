# vector_memory.py
import json
import math
from datetime import datetime

class VectorMemory:
    def __init__(self, embed_fn, path="vector_memory.json"):
        self.embed_fn = embed_fn
        self.path = path
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def add(self, text: str):
        embedding = self.embed_fn(text)
        self.data.append({
            "text": text,
            "embedding": embedding,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()

    def search(self, query: str, top_k=3):
        query_emb = self.embed_fn(query)

        scored = []
        for item in self.data:
            score = self._cosine_similarity(query_emb, item["embedding"])
            scored.append((score, item["text"]))

        scored.sort(reverse=True)
        return [text for _, text in scored[:top_k]]

    def _cosine_similarity(self, a, b):
        dot = sum(x*y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x*x for x in a))
        norm_b = math.sqrt(sum(x*x for x in b))
        return dot / (norm_a * norm_b + 1e-8)

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
