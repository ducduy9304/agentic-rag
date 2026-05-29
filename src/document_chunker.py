"""
This file cuts markdown documents into small pieces (chunks) for a RAG system.

We use a "parent-child" idea:
  - PARENT chunks are big. They have enough text for the LLM to read and
    understand the context.
  - CHILD chunks are small. They are good for search, because a small piece
    of text matches a user's question more clearly.

How it works at search time:
  1. The user asks a question.
  2. We search the CHILD chunks to find the best match.
  3. We return the PARENT of that child to the LLM.

This way we get good search (from children) AND good context (from parents).
"""

import glob
import os
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import config


class DocumentChunker:
    def __init__(self):
        # This splitter cuts the document at every heading (#, ##, ###).
        # We keep the heading text inside the chunk (strip_headers=False)
        # because the title helps the model understand what the chunk is about.
        self.__parent_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=config.HEADERS_TO_SPLIT_ON,
            strip_headers=False
        )

        # This splitter cuts text into small pieces by character count.
        # We use a small overlap so a sentence is not cut in half.
        self.__child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHILD_CHUNK_SIZE,
            chunk_overlap=config.CHILD_CHUNK_OVERLAP
        )

        # A section can be very short or very long. We will use these two
        # numbers later to fix that:
        #   - if a chunk is smaller than min_parent_size, it is too small
        #   - if a chunk is bigger than max_parent_size, it is too big
        self.__min_parent_size = config.MIN_PARENT_SIZE
        self.__max_parent_size = config.MAX_PARENT_SIZE

    def create_chunks(self, path_dir=config.MARKDOWN_DIR):
        # Read every .md file in the folder, chunk each one, and put all
        # the results together into two big lists.
        all_parent_chunks, all_child_chunks = [], []

        for doc_path_str in sorted(glob.glob(os.path.join(path_dir, "*.md"))):
            doc_path = Path(doc_path_str)
            parent_chunks, child_chunks = self.create_chunks_single(doc_path)
            all_parent_chunks.extend(parent_chunks)
            all_child_chunks.extend(child_chunks)

        return all_parent_chunks, all_child_chunks

    def create_chunks_single(self, md_path):
        # This function chunks ONE markdown file.
        doc_path = Path(md_path)

        # Step 1: Read the file and split it at every heading.
        # After this step, the chunk sizes are not balanced yet.
        with open(doc_path, 'r', encoding='utf-8') as f:
            parent_chunks = self.__parent_splitter.split_text(f.read())

        # Step 2: Fix the chunk sizes in three passes.
        #   - merge: join small chunks together
        #   - split: cut big chunks into smaller pieces
        #   - clean: handle any small pieces that are still left
        merged_parents = self.__merge_small_parents(parent_chunks)
        split_parents = self.__split_large_parents(merged_parents)
        cleaned_parents = self.__clean_small_chunks(split_parents)

        # Step 3: Give each parent an ID and make child chunks from it.
        all_parent_chunks, all_child_chunks = [], []
        self.__create_child_chunks(all_parent_chunks, all_child_chunks, cleaned_parents, doc_path)
        return all_parent_chunks, all_child_chunks


    def __merge_small_parents(self, chunks):
        # Why we need this:
        #   A short section (for example "## Note\nSee below.") is too small
        #   to be useful. The LLM cannot learn much from it.
        #
        # What we do:
        #   Go through the chunks in order. Keep adding small chunks together
        #   until the total size is big enough. Then save that as one parent
        #   and start again with the next chunk.
        #
        # About metadata:
        #   When we join two chunks, we also need to join their heading info.
        #   If both chunks have the same heading level (for example two "H2"),
        #   we connect them with "->" so we can still see the original titles.

        if not chunks:
            return []

        merged, current = [], None
        for chunk in chunks:
            if current is None:
                # Start a new group with this chunk.
                current = chunk
            else:
                # Add this chunk's text and heading info to the current group.
                current.page_content += "\n\n" + chunk.page_content
                for k, v in chunk.metadata.items():
                    if k in current.metadata:
                        current.metadata[k] = f"{current.metadata[k]} -> {v}"
                    else:
                        current.metadata[k] = v

            # The group is big enough now. Save it and start a new one.
            if len(current.page_content) >= self.__min_parent_size:
                merged.append(current)
                current = None

        # Last case:
        #   We finished the loop, but the current group is still too small.
        #   We don't want to lose it, so we add it to the last saved parent.
        #   If there is no saved parent yet, we just keep it as it is.
        if current:
            if merged:
                merged[-1].page_content += "\n\n" + current.page_content
                for k, v in current.metadata.items():
                    if k in merged[-1].metadata:
                        merged[-1].metadata[k] = f"{merged[-1].metadata[k]} -> {v}"
                    else:
                        merged[-1].metadata[k] = v
            else:
                merged.append(current)

        return merged


    def __split_large_parents(self, chunks):
        # Why we need this:
        #   Some sections are very long (for example one full chapter).
        #   The embedding model works better on shorter text, so we should
        #   not keep these huge chunks.
        #
        # What we do:
        #   If a chunk is bigger than max_parent_size, cut it into smaller
        #   pieces. If it is already small enough, keep it as is.

        split_chunks = []

        for chunk in chunks:
            if len(chunk.page_content) <= self.__max_parent_size:
                split_chunks.append(chunk)
            else:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size = self.__max_parent_size,
                    chunk_overlap = config.CHILD_CHUNK_OVERLAP
                )
                sub_chunks = splitter.split_documents([chunk])
                split_chunks.extend(sub_chunks)

        return split_chunks

    def __clean_small_chunks(self, chunks):
        # Why we need this:
        #   When we cut a big chunk in the step before, the last piece is
        #   often very small (for example: 4000 chars + 300 chars left over).
        #   That tiny 300-char piece is too small to be a good parent.
        #
        # What we do:
        #   Check every chunk again. If a chunk is still too small, join it
        #   with another chunk. There are three cases:
        #     1. We already have a parent before this one -> join it there.
        #     2. There is no parent before, but there is a chunk after ->
        #        add the small text to the front of the next chunk.
        #     3. It is the last chunk and there is nothing after -> just
        #        keep it.

        cleaned = []

        for i, chunk in enumerate(chunks):
            if len(chunk.page_content) < self.__min_parent_size:
                if cleaned:
                    # Case 1: add to the last parent we kept.
                    cleaned[-1].page_content += "\n\n" + chunk.page_content
                    for k, v in chunk.metadata.items():
                        if k in cleaned[-1].metadata:
                            cleaned[-1].metadata[k] = f"{cleaned[-1].metadata[k]} -> {v}"
                        else:
                            cleaned[-1].metadata[k] = v
                elif i < len(chunks) - 1:
                    # Case 2: no parent before yet, so move the text to the
                    # next chunk. The loop will handle it next time.
                    chunks[i+1].page_content = chunk.page_content + "\n\n" + chunks[i+1].page_content
                    for k,v in chunk.metadata.items():
                        if k in chunks[i + 1].metadata:
                            chunks[i+1].metadata[k] = f"{v} -> {chunks[i+1].metadata[k]}"
                        else:
                            chunks[i+1].metadata[k] = v
                else:
                    # Case 3: last chunk, nothing to join with. Keep it.
                    cleaned.append(chunk)
            else:
                cleaned.append(chunk)

        return cleaned

    def __create_child_chunks(self, all_parent_chunks, all_child_chunks, parent_chunks, doc_path):
        # Last step:
        #   For each parent, we do two things:
        #     1. Give it an ID like "myfile_parent_3". We need this ID later
        #        so we can find the parent when a child is matched in search.
        #     2. Cut the parent into smaller child chunks for the vector DB.
        #
        # Note: when we call split_documents, the children copy the parent's
        # metadata. This means every child also has the parent_id inside it.
        # That is how the search system can link a child back to its parent.

        for i, p_chunk in enumerate(parent_chunks):
            parent_id = f"{doc_path.stem}_parent_{i}"
            # Save the original file name and the parent ID into metadata.
            # The markdown files come from PDFs, so we save the source as .pdf.
            p_chunk.metadata.update({"source": str(doc_path.stem)+".pdf", "parent_id": parent_id})

            all_parent_chunks.append((parent_id, p_chunk))
            all_child_chunks.extend(self.__child_splitter.split_documents([p_chunk]))
