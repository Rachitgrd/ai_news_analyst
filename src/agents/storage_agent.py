from datetime import datetime
from src.utils.vector_store import get_vector_store, add_embeddings_to_store

class StorageAgent:
    def __init__(self):
        self.client = get_vector_store()

    def generate_collection_name(self, prefix: str = "news_embeddings"):
        date_str = datetime.now().strftime("%Y_%m_%d")
        return f"{prefix}_{date_str}"

    def store_embeddings(self, embeddings_list: list, collection_name: str = None):
        """
        Stores embeddings into ChromaDB.
        If no collection name provided, creates a date-based collection.
        """

        if not embeddings_list:
            print("[StorageAgent] No embeddings to store.")
            return None

        if collection_name is None:
            collection_name = self.generate_collection_name()

        # Try removing old collection with same name
        try:
            self.client.delete_collection(collection_name)
        except:
            pass

        try:
            collection = add_embeddings_to_store(
                self.client,
                collection_name,
                embeddings_list
            )
            print(f"[StorageAgent] Stored {len(embeddings_list)} embeddings in {collection_name}.")
            return collection_name

        except Exception as e:
            print(f"[StorageAgent] Failed to store embeddings: {e}")
            return None

    def delete_collection(self, name: str):
        try:
            self.client.delete_collection(name)
            print(f"[StorageAgent] Deleted collection {name}.")
        except:
            print(f"[StorageAgent] Unable to delete collection {name}.")
