"""
Semantic memory search using embeddings.
Inspired by AI Town's memory retrieval system.
"""
import os
from typing import List, Optional, Tuple
import numpy as np
from src.models.character import Memory


class MemorySearchEngine:
    """Search character memories using semantic similarity."""

    def __init__(self, use_embeddings: bool = True, api_key: Optional[str] = None):
        """
        Args:
            use_embeddings: Use embeddings for semantic search (requires API key)
            api_key: OpenAI API key for embeddings
        """
        self.use_embeddings = use_embeddings
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.embedding_cache = {}  # Cache embeddings to avoid re-computing

        if use_embeddings and not self.api_key:
            print("⚠️  No API key for embeddings. Using keyword fallback.")
            self.use_embeddings = False

    def search_relevant_memories(
        self,
        memories: List[Memory],
        query: str,
        top_k: int = 5
    ) -> List[Memory]:
        """
        Search memories for those most relevant to the query.

        Args:
            memories: List of memories to search
            query: What to search for (e.g., "interactions about lost things")
            top_k: How many memories to return

        Returns:
            List of most relevant memories
        """
        if not memories:
            return []

        if self.use_embeddings:
            return self._search_with_embeddings(memories, query, top_k)
        else:
            return self._search_with_keywords(memories, query, top_k)

    def _search_with_embeddings(
        self,
        memories: List[Memory],
        query: str,
        top_k: int
    ) -> List[Memory]:
        """Use embeddings for semantic similarity search."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            # Get query embedding
            query_embedding = self._get_embedding(query, client)

            # Score each memory by similarity
            scored_memories = []
            for memory in memories:
                memory_embedding = self._get_embedding(memory.content, client)
                similarity = self._cosine_similarity(query_embedding, memory_embedding)

                # Weight by importance and recency
                recency_weight = 0.3  # Recent memories get boost
                importance_weight = memory.importance / 10.0

                final_score = similarity + (recency_weight * 0.1) + (importance_weight * 0.2)
                scored_memories.append((final_score, memory))

            # Sort by score and return top k
            scored_memories.sort(reverse=True, key=lambda x: x[0])
            return [mem for score, mem in scored_memories[:top_k]]

        except Exception as e:
            print(f"Embedding search failed: {e}. Using keyword fallback.")
            return self._search_with_keywords(memories, query, top_k)

    def _get_embedding(self, text: str, client) -> List[float]:
        """Get embedding for text, with caching."""
        if text in self.embedding_cache:
            return self.embedding_cache[text]

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embedding = response.data[0].embedding
        self.embedding_cache[text] = embedding
        return embedding

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

    def _search_with_keywords(
        self,
        memories: List[Memory],
        query: str,
        top_k: int
    ) -> List[Memory]:
        """Fallback: Simple keyword matching."""
        query_words = set(query.lower().split())

        scored_memories = []
        for memory in memories:
            memory_words = set(memory.content.lower().split())

            # Count matching words
            matches = len(query_words.intersection(memory_words))

            # Weight by importance and recency
            importance_weight = memory.importance / 10.0
            recency_boost = 0.5  # Recent memories slightly preferred

            score = matches + importance_weight + recency_boost
            scored_memories.append((score, memory))

        # Sort by score and return top k
        scored_memories.sort(reverse=True, key=lambda x: x[0])
        return [mem for score, mem in scored_memories[:top_k]]

    def clear_cache(self):
        """Clear the embedding cache."""
        self.embedding_cache = {}
