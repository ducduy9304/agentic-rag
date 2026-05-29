"""
This file saves and loads the PARENT chunks on disk.

Why we need this:
  In our parent-child RAG system, the vector database only stores the small
  child chunks (for search). The big parent chunks are too long to store as
  vectors, so we keep them on disk instead.

  Each parent is saved as one JSON file. The file name is the parent_id
  (for example "myfile_parent_3.json"), so we can find any parent later
  just by knowing its ID.
"""

import re
import json
import config
from utils import clear_directory_contents
from pathlib import Path
from typing import List, Dict

class ParentStoreManager:
    __store_path: Path

    def __init__(self, store_path=config.PARENT_STORE_PATH):
        # Set the folder where all parent JSON files will live.
        # Create it now if it does not exist yet.
        self.__store_path = Path(store_path)
        self.__store_path.mkdir(parents=True, exist_ok=True)

    def save(self, parent_id: str, content: str, metadata: Dict) -> None:
        # Save ONE parent chunk as a JSON file.
        # The file is named after the parent_id, so we can load it back later.
        file_path = self.__store_path / f"{parent_id}.json"
        file_path.write_text(
            json.dump({"page_content": content, "metadata": metadata}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def save_many(self, parents: List) -> None:
        # Save many parents at once. `parents` is a list of (id, doc) pairs
        # — the same shape that DocumentChunker returns.
        for parent_id, doc in parents:
            self.save(parent_id, doc.page_content, doc.metadata)

    def load(self, parent_id: str) -> Dict:
        # Read one parent file back from disk and return it as a dict.
        # The caller can pass the id with or without the ".json" suffix —
        # we accept both to make it easy to use.
        file_path = self.__store_path / (parent_id if parent_id.lower().endswith(".json") else f"{parent_id}.json")
        return json.loads(file_path.read_text(encoding="utf-8"))

    def load_content(self, parent_id: str) -> Dict:
        # Same as load(), but reshape the result into the format that the
        # rest of the app expects: {content, parent_id, metadata}.
        data = self.load(parent_id)
        return {
            "content": data["page_content"],
            "parent_id": parent_id,
            "metadata": data["metadata"]
        }

    @staticmethod
    def __get_sort_key(id_str):
        # Parent IDs look like "myfile_parent_3". This helper pulls out the
        # number at the end ("3") so we can sort parents in the order they
        # appeared in the original document, not in alphabetical order.
        # (Alphabetical order would put "parent_10" before "parent_2".)
        match = re.search(r'_parent_(\d+)$', id_str)
        return int(match.group(1) if match else 0)

    def load_content_many(self, parent_ids: List[str]) -> List[Dict]:
        # Load many parents at once.
        # We use set() to remove duplicates (the search may return the same
        # parent more than once if two of its children match the query).
        # Then we sort by document order so the LLM reads the parents in
        # the same order they appeared in the original file.
        unique_ids = set(parent_ids)
        return [self.load_content(pid) for pid in sorted(unique_ids, key=self.__get_sort_key)]

    def clear_store(self) -> None:
        # Delete every file inside the store folder, but keep the folder
        # itself. We use this when we want to re-index everything from scratch.
        self.__store_path.mkdir(parents=True, exist_ok=True)
        clear_directory_contents(self.__store_path)
        