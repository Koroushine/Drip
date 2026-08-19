# src/knowledge_base.py - Updated for Class 8, 9, 10

import os
import re
import numpy as np
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import (
    DATA_FOLDER,
    CHAPTER_TOPICS,
    CHAPTER_NAMES,
    get_grade_from_file,
    DEFAULT_TOP_K
)
from src.utils import load_pdf_text, chunk_text


class KnowledgeBase:
    """
    Knowledge Base for NCERT Class 8, 9, 10 Science
    """

    def __init__(self, folder: str = DATA_FOLDER):
        self.folder = folder
        self.chunks: List[str] = []
        self.metadata: List[Dict] = []
        self.grade_index: Dict[str, List[int]] = {
            "Class 8": [],
            "Class 9": [],
            "Class 10": []
        }
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._loaded_files: List[str] = []

        print("📚 Loading NCERT Knowledge Base (Class 8, 9, 10)...")
        self._load_all_pdfs()
        self._build_index()
        self._build_grade_index()
        print(f"✅ Loaded {len(self.chunks)} chunks from {len(self._loaded_files)} files")
        print(f"   Class 8: {len(self.grade_index['Class 8'])} chunks")
        print(f"   Class 9: {len(self.grade_index['Class 9'])} chunks")
        print(f"   Class 10: {len(self.grade_index['Class 10'])} chunks")

    def _load_all_pdfs(self):
        """Load all PDF files from the data folder"""
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            print(f"⚠️ Data folder '{self.folder}' created. Place NCERT PDFs here.")
            return

        pdf_files = [f for f in os.listdir(self.folder) if f.endswith('.pdf')]

        if not pdf_files:
            print(f"⚠️ No PDF files found in '{self.folder}'")
            return

        # Sort by grade for better loading order
        def sort_key(f):
            if f.startswith("hecu"):
                return 0
            elif f.startswith("iesc"):
                return 1
            elif f.startswith("jesc"):
                return 2
            return 3

        pdf_files.sort(key=sort_key)

        for pdf_file in pdf_files:
            try:
                pdf_path = os.path.join(self.folder, pdf_file)
                text = load_pdf_text(pdf_path)

                if text and len(text) > 100:  # Skip empty files
                    chunks = chunk_text(text)
                    topics = CHAPTER_TOPICS.get(pdf_file, [])
                    chapter_name = CHAPTER_NAMES.get(pdf_file, pdf_file)
                    grade = get_grade_from_file(pdf_file)

                    for chunk in chunks:
                        idx = len(self.chunks)
                        self.chunks.append(chunk)
                        self.metadata.append({
                            'file': pdf_file,
                            'chapter': chapter_name,
                            'grade': grade,
                            'topics': topics,
                            'chunk_index': idx
                        })

                    self._loaded_files.append(pdf_file)
                    print(f"  ✓ Loaded {pdf_file} ({len(chunks)} chunks) [{grade}]")
                else:
                    print(f"  ⚠️ No text extracted from {pdf_file}")

            except Exception as e:
                print(f"  ⚠️ Error loading {pdf_file}: {e}")

    def _build_index(self):
        """Build TF-IDF index for searching"""
        if not self.chunks:
            print("⚠️ No chunks to index")
            return

        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=20000,
            min_df=2,
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        print(f"  ✓ Built index with {self.tfidf_matrix.shape[1]} features")

    def _build_grade_index(self):
        """Build grade-specific indices"""
        for idx, meta in enumerate(self.metadata):
            grade = meta.get('grade', 'Unknown')
            if grade in self.grade_index:
                self.grade_index[grade].append(idx)

    def search(self,
               query: str,
               topics: List[str] = None,
               grade: str = None,
               top_k: int = DEFAULT_TOP_K) -> List[Dict]:
        """
        Search for relevant chunks with grade/topic filtering

        Args:
            query: Search query
            topics: Optional list of topics to filter by
            grade: Optional grade filter ("Class 8", "Class 9", "Class 10")
            top_k: Number of results to return
        """
        if not self.chunks or self.tfidf_matrix is None:
            return []

        # Grade filtering
        candidate_indices = None
        if grade and grade in self.grade_index:
            candidate_indices = set(self.grade_index[grade])

        # Topic filtering
        if topics:
            topic_indices = set()
            for topic in topics:
                topic_lower = topic.lower()
                for idx, meta in enumerate(self.metadata):
                    meta_topics = [t.lower() for t in meta.get('topics', [])]
                    if topic_lower in meta_topics:
                        topic_indices.add(idx)

            if candidate_indices is not None:
                candidate_indices = candidate_indices.intersection(topic_indices)
            else:
                candidate_indices = topic_indices

        # Search
        q_vec = self.vectorizer.transform([query])

        if candidate_indices:
            indices = list(candidate_indices)
            if not indices:
                return []
            sim = cosine_similarity(q_vec, self.tfidf_matrix[indices]).flatten()
            top_local = np.argsort(sim)[-top_k:][::-1]

            results = []
            for local_idx in top_local:
                global_idx = indices[local_idx]
                if sim[local_idx] > 0:
                    results.append({
                        'text': self.chunks[global_idx],
                        'score': float(sim[local_idx]),
                        'metadata': self.metadata[global_idx]
                    })
            return results

        # Regular search
        sim = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        top_indices = np.argsort(sim)[-top_k:][::-1]

        return [{
            'text': self.chunks[i],
            'score': float(sim[i]),
            'metadata': self.metadata[i] if i < len(self.metadata) else {}
        } for i in top_indices if sim[i] > 0]

    def search_by_grade(self, query: str, grade: str, top_k: int = DEFAULT_TOP_K) -> List[Dict]:
        """Search within a specific grade"""
        return self.search(query, grade=grade, top_k=top_k)

    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            'total_chunks': len(self.chunks),
            'loaded_files': len(self._loaded_files),
            'total_files': len([f for f in os.listdir(self.folder) if f.endswith('.pdf')]),
            'grade_counts': {
                grade: len(indices)
                for grade, indices in self.grade_index.items()
            },
            'total_topics': len(set([t for meta in self.metadata for t in meta.get('topics', [])]))
        }