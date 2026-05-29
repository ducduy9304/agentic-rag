"""
This file manages the vector database (Qdrant) for our RAG system.

We use HYBRID search, which means we combine two kinds of embeddings:
  - DENSE embeddings: a normal sentence-transformer model. Good at finding
    text with similar MEANING (even if the words are different).
  - SPARSE embeddings (BM25): good at finding exact KEYWORD matches.

Using both together gives better search results than using either alone.
The vector DB only stores CHILD chunks (the small pieces). The parents
live on disk — see parent_store_manager.py.
"""

import config
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

class VectorDbMangager:
    __client: QdrantClient
    __dense_embeddings: HuggingFaceEmbeddings
    __sparse_embeddings: FastEmbedSparse

    def __init__(self):
        # Open the local Qdrant database (stored as files on disk).
        self.__client = QdrantClient(path=config.QDRANT_DB_PATH)
        # Load the two embedding models we use for hybrid search.
        self.__dense_embeddings = HuggingFaceEmbeddings(model_name=config.DENSE_MODEL)
        self.__sparse_embeddings = FastEmbedSparse(model_name=config.SPARSE_MODEL)


    def create_collection(self, collection_name):
        # A "collection" in Qdrant is like a table in a normal database.
        # We only create it if it does not exist yet (so we don't lose data).
        if not self.__client.collection_exists(collection_name):
            print(f"Creating collection: {collection_name}...")
            self.__client.create_collection(
                collection_name=collection_name,
                # We need to tell Qdrant the size (dimension) of our dense
                # vectors. We get it by embedding a small test string and
                # checking how long the result is.
                # COSINE distance is the standard way to compare meaning.
                vectors_config=qmodels.VectorParams(size=len(self.__dense_embeddings.embed_query("test")), distance=qmodels.Distance.COSINE),
                # We also tell Qdrant to store sparse (BM25) vectors next
                # to the dense ones, so hybrid search can use both.
                sparse_vectors_config={config.SPARSE_VECTOR_NAME: qmodels.SparseVectorParams()},
            )
            print(f"Collection created: {collection_name}")
        else:
            print(f"Collection already exists: {collection_name}")


    def delete_collection(self, collection_name):
        # Remove a collection completely. We use this when we want to
        # rebuild the index from scratch.
        # We wrap it in try/except so a missing collection does not crash
        # the whole pipeline.
        try:
            if self.__client.collection_exists(collection_name):
                print(f"Removing existing Qdrant collection: {collection_name}")
                self.__client.delete_collection(collection_name)
        except Exception as e:
            print(f"Warning: could not delete collection: {collection_name}: {e}")


    def get_collection(self, collection_name) -> QdrantVectorStore:
        # Return the collection wrapped as a LangChain VectorStore.
        # We set retrieval_mode=HYBRID so search uses BOTH dense and sparse
        # vectors at the same time, then combines the scores.
        try:
            return QdrantVectorStore(
                client=self.__client,
                collection_name=collection_name,
                embedding=self.__dense_embeddings,
                sparse_embedding=self.__sparse_embeddings,
                retrieval_mode=RetrievalMode.HYBRID,
                sparse_vector_name=config.SPARSE_VECTOR_NAME
            )
        except Exception as e:
            print(f"Unable to get collection {collection_name}: {e}")

