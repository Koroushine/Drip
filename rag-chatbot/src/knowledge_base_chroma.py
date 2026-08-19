# src/knowledge_base_chroma.py

# ============================================================
# FIX: Import chromadb with a patch to avoid onnxruntime
# ============================================================

import sys
import os
import warnings
from typing import List, Dict, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import (
    DATA_FOLDER,
    CHAPTER_TOPICS,
    CHAPTER_NAMES,
    get_grade_from_file,
    USE_CHROMA,
    CHROMA_PATH
)
from src.utils import load_pdf_text, chunk_text

# ============================================================
# Suppress the onnxruntime import error
# ============================================================

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    try:
        import chromadb
        from chromadb.config import Settings

        HAS_CHROMA = True
        print("   ✅ ChromaDB imported successfully")
    except ImportError:
        HAS_CHROMA = False
        print("⚠️ ChromaDB not installed. Install with: pip install chromadb")
    except Exception as e:
        HAS_CHROMA = False
        print(f"⚠️ ChromaDB import error: {e}")
        print("   Continuing without ChromaDB...")


class KnowledgeBase:
    """
    Knowledge Base with ChromaDB for persistent storage (no embeddings)
    Uses TF-IDF for search, ChromaDB just stores the data
    """

    def __init__(self, folder: str = DATA_FOLDER, use_chroma: bool = USE_CHROMA):
        self.folder = folder
        self.use_chroma = use_chroma and HAS_CHROMA
        self.chunks: List[str] = []
        self.metadata: List[Dict] = []
        self._loaded_files: List[str] = []
        self.grade_index = {"Class 8": [], "Class 9": [], "Class 10": []}

        # TF-IDF for search
        self.vectorizer = None
        self.tfidf_matrix = None

        # ChromaDB client
        self.client = None
        self.collection = None

        if self.use_chroma:
            print("📚 Initializing ChromaDB (storage only)...")
            self._init_chroma()
            if self._collection_exists():
                self._load_from_chroma()
            else:
                print("📚 First time - building from PDFs...")
                self._build_from_pdfs()
                self._save_to_chroma()
        else:
            print("📚 Loading from PDFs (no ChromaDB)...")
            self._build_from_pdfs()

        # Always build TF-IDF for search
        self._build_tfidf()
        self._build_grade_index()

        print(f"✅ Loaded {len(self.chunks)} chunks")
        print(f"   Class 8: {len(self.grade_index['Class 8'])} chunks")
        print(f"   Class 9: {len(self.grade_index['Class 9'])} chunks")
        print(f"   Class 10: {len(self.grade_index['Class 10'])} chunks")

    def _init_chroma(self):
        """Initialize ChromaDB client WITHOUT embeddings"""
        try:
            # ✅ FIX: Use Settings to disable telemetry and avoid embedding issues
            self.client = chromadb.PersistentClient(
                path=CHROMA_PATH,
                settings=Settings(
                    anonymized_telemetry=False,
                    is_persistent=True,
                    allow_reset=True
                )
            )
            print(f"   ✅ ChromaDB initialized at {CHROMA_PATH}")
        except Exception as e:
            print(f"⚠️ ChromaDB init failed: {e}")
            self.use_chroma = False

    def _collection_exists(self) -> bool:
        """Check if collection already exists"""
        try:
            collections = self.client.list_collections()
            return "ncert_science" in [c.name for c in collections]
        except Exception:
            return False

    def _load_from_chroma(self):
        """Load from ChromaDB"""
        try:
            print("📚 Loading from ChromaDB...")
            self.collection = self.client.get_collection("ncert_science")

            results = self.collection.get()

            if results and results['documents']:
                for i, text in enumerate(results['documents']):
                    self.chunks.append(text)
                    meta = results['metadatas'][i] if results['metadatas'] else {}
                    self.metadata.append({
                        'file': meta.get('file', 'unknown'),
                        'chapter': meta.get('chapter', 'unknown'),
                        'grade': meta.get('grade', 'unknown'),
                        'topics': meta.get('topics', '').split(',') if meta.get('topics') else [],
                        'chunk_index': i
                    })
                print(f"   ✅ Loaded {len(self.chunks)} chunks from ChromaDB")
            else:
                print("   ⚠️ ChromaDB is empty, rebuilding from PDFs...")
                self._build_from_pdfs()
                self._save_to_chroma()

        except Exception as e:
            print(f"⚠️ ChromaDB load failed: {e}, rebuilding...")
            self._build_from_pdfs()
            self._save_to_chroma()

    def _build_from_pdfs(self):
        """Load from PDFs (slower, first time only)"""
        print("📚 Loading from PDFs...")
        self.chunks = []
        self.metadata = []

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            print(f"⚠️ Data folder '{self.folder}' created. Place NCERT PDFs here.")
            return

        pdf_files = sorted([f for f in os.listdir(self.folder) if f.endswith('.pdf')])

        if not pdf_files:
            print(f"⚠️ No PDF files found in '{self.folder}'")
            return

        for pdf_file in pdf_files:
            try:
                pdf_path = os.path.join(self.folder, pdf_file)
                text = load_pdf_text(pdf_path)

                if text and len(text) > 100:
                    chunks = chunk_text(text)
                    topics = CHAPTER_TOPICS.get(pdf_file, [])
                    chapter_name = CHAPTER_NAMES.get(pdf_file, pdf_file)
                    grade = get_grade_from_file(pdf_file)

                    for chunk in chunks:
                        self.chunks.append(chunk)
                        self.metadata.append({
                            'file': pdf_file,
                            'chapter': chapter_name,
                            'grade': grade,
                            'topics': topics,
                            'chunk_index': len(self.chunks) - 1
                        })

                    self._loaded_files.append(pdf_file)
                    print(f"  ✓ Loaded {pdf_file} ({len(chunks)} chunks) [{grade}]")

            except Exception as e:
                print(f"  ⚠️ Error loading {pdf_file}: {e}")

        print(f"✅ Loaded {len(self.chunks)} chunks from PDFs")

    def _save_to_chroma(self):
        """Save to ChromaDB"""
        if not self.use_chroma or not self.client:
            return

        try:
            print("💾 Saving to ChromaDB...")

            # ✅ FIX: Create collection WITHOUT embedding function
            self.collection = self.client.create_collection(
                name="ncert_science",
                embedding_function=None  # ← NO embeddings!
            )

            ids = [f"chunk_{i}" for i in range(len(self.chunks))]
            documents = self.chunks
            metadatas = []

            for meta in self.metadata:
                metadatas.append({
                    'file': meta.get('file', ''),
                    'chapter': meta.get('chapter', ''),
                    'grade': meta.get('grade', ''),
                    'topics': ','.join(meta.get('topics', []))
                })

            batch_size = 1000
            total_batches = (len(documents) + batch_size - 1) // batch_size

            for i in range(0, len(documents), batch_size):
                end = min(i + batch_size, len(documents))
                self.collection.add(
                    ids=ids[i:end],
                    documents=documents[i:end],
                    metadatas=metadatas[i:end]
                )
                print(f"  ✓ Saved batch {i // batch_size + 1}/{total_batches}")

            print(f"✅ Saved {len(self.chunks)} chunks to ChromaDB!")

        except Exception as e:
            print(f"⚠️ ChromaDB save failed: {e}")
            self.use_chroma = False

    def _build_tfidf(self):
        """Build TF-IDF for search"""
        if not self.chunks:
            return

        try:
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=20000,
                min_df=2,
                sublinear_tf=True
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        except Exception as e:
            print(f"⚠️ TF-IDF build failed: {e}")

    def _build_grade_index(self):
        """Build grade-specific indices"""
        self.grade_index = {"Class 8": [], "Class 9": [], "Class 10": []}
        for idx, meta in enumerate(self.metadata):
            grade = meta.get('grade', 'Unknown')
            if grade in self.grade_index:
                self.grade_index[grade].append(idx)

    def search(self, query: str, topics: List[str] = None, grade: str = None, top_k: int = 4) -> List[Dict]:
        """Search using TF-IDF"""
        if not self.chunks or self.tfidf_matrix is None:
            return []

        # Filter by grade if specified
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

    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            'total_chunks': len(self.chunks),
            'loaded_files': len(self._loaded_files),
            'grade_counts': {
                grade: len(indices)
                for grade, indices in self.grade_index.items()
            },
            'using_chroma': self.use_chroma,
            'has_tfidf': self.tfidf_matrix is not None
        }