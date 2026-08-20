# src/knowledge_base_chroma.py - Optimized with ChromaDB persistence

import os
import sys
import warnings
import pickle
import hashlib
from typing import List, Dict, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

from src.config import (
    DATA_FOLDER,
    CHAPTER_TOPICS,
    CHAPTER_NAMES,
    get_grade_from_file,
    USE_CHROMA,
    CHROMA_PATH
)
from src.utils import load_pdf_text, chunk_text

# Suppress warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    try:
        import chromadb
        from chromadb.config import Settings
        HAS_CHROMA = True
        print("   ✅ ChromaDB imported")
    except ImportError:
        HAS_CHROMA = False
        print("⚠️ ChromaDB not installed")


class KnowledgeBase:
    """Knowledge Base with optimized ChromaDB persistence"""

    def __init__(self, folder: str = DATA_FOLDER, use_chroma: bool = USE_CHROMA):
        self.folder = folder
        self.use_chroma = use_chroma and HAS_CHROMA
        self.chunks: List[str] = []
        self.metadata: List[Dict] = []
        self._loaded_files: List[str] = []
        self.grade_index = {"Class 8": [], "Class 9": [], "Class 10": []}
        self.file_hashes = {}

        # TF-IDF for search
        self.vectorizer = None
        self.tfidf_matrix = None

        # ChromaDB client
        self.client = None
        self.collection = None
        
        # Cache file for faster loading
        self.cache_file = os.path.join(CHROMA_PATH, "knowledge_cache.pkl")

        # Initialize ChromaDB
        if self.use_chroma:
            print("📚 Initializing ChromaDB with persistence...")
            self._init_chroma()
            if self._collection_exists():
                # Load from ChromaDB (FAST)
                self._load_from_chroma()
            else:
                # First time - build from PDFs (SLOW - only once)
                print("📚 First time setup - building index from PDFs...")
                print("⏳ This may take a few minutes on first run...")
                self._build_from_pdfs()
                self._save_to_chroma()
                print("✅ Index built and saved to ChromaDB!")
        else:
            print("📚 Loading from PDFs (no ChromaDB)...")
            self._build_from_pdfs()

        # Build TF-IDF for search
        self._build_tfidf()
        self._build_grade_index()

        print(f"✅ Loaded {len(self.chunks)} chunks")
        print(f"   Class 8: {len(self.grade_index['Class 8'])} chunks")
        print(f"   Class 9: {len(self.grade_index['Class 9'])} chunks")
        print(f"   Class 10: {len(self.grade_index['Class 10'])} chunks")

    def _init_chroma(self):
        """Initialize ChromaDB with persistence"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(CHROMA_PATH, exist_ok=True)
            
            self.client = chromadb.PersistentClient(
                path=CHROMA_PATH,
                settings=Settings(
                    anonymized_telemetry=False,
                    is_persistent=True,
                    allow_reset=False
                )
            )
            print(f"   ✅ ChromaDB initialized at {CHROMA_PATH}")
        except Exception as e:
            print(f"⚠️ ChromaDB init failed: {e}")
            self.use_chroma = False

    def _collection_exists(self) -> bool:
        """Check if collection exists and has data"""
        try:
            collections = self.client.list_collections()
            if "ncert_science" in [c.name for c in collections]:
                collection = self.client.get_collection("ncert_science")
                # Check if it has documents
                count = collection.count()
                return count > 0
            return False
        except Exception:
            return False

    def _get_file_hash(self, filepath: str) -> str:
        """Get hash of file to detect changes"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""

    def _get_files_hash(self) -> str:
        """Get combined hash of all PDFs to detect changes"""
        pdf_files = [f for f in os.listdir(self.folder) if f.endswith('.pdf')]
        hashes = []
        for pdf_file in sorted(pdf_files):
            filepath = os.path.join(self.folder, pdf_file)
            hashes.append(self._get_file_hash(filepath))
        return hashlib.md5(''.join(hashes).encode()).hexdigest()

    def _load_from_chroma(self):
        """Load from ChromaDB - FAST"""
        try:
            print("📚 Loading from ChromaDB (fast)...")
            self.collection = self.client.get_collection("ncert_science")

            # Get all data
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
                
                # Update file tracking
                if hasattr(self, '_loaded_files'):
                    loaded_files = set()
                    for meta in self.metadata:
                        if meta.get('file'):
                            loaded_files.add(meta['file'])
                    self._loaded_files = list(loaded_files)
            else:
                print("   ⚠️ ChromaDB is empty, rebuilding...")
                self._build_from_pdfs()
                self._save_to_chroma()

        except Exception as e:
            print(f"⚠️ ChromaDB load failed: {e}, rebuilding...")
            self._build_from_pdfs()
            self._save_to_chroma()

    def _build_from_pdfs(self):
        """Load from PDFs - SLOW (only on first run or when files change)"""
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
        """Save to ChromaDB - FAST retrieval later"""
        if not self.use_chroma or not self.client:
            return

        try:
            # Delete existing collection if exists
            try:
                self.client.delete_collection("ncert_science")
            except:
                pass

            print("💾 Saving to ChromaDB for fast loading...")
            self.collection = self.client.create_collection(
                name="ncert_science",
                embedding_function=None
            )

            # Batch save for efficiency
            batch_size = 1000
            total_batches = (len(self.chunks) + batch_size - 1) // batch_size

            for i in range(0, len(self.chunks), batch_size):
                end = min(i + batch_size, len(self.chunks))
                ids = [f"chunk_{j}" for j in range(i, end)]
                documents = self.chunks[i:end]
                metadatas = []
                
                for meta in self.metadata[i:end]:
                    metadatas.append({
                        'file': meta.get('file', ''),
                        'chapter': meta.get('chapter', ''),
                        'grade': meta.get('grade', ''),
                        'topics': ','.join(meta.get('topics', []))
                    })

                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                print(f"  ✓ Saved batch {i // batch_size + 1}/{total_batches}")

            print(f"✅ Saved {len(self.chunks)} chunks to ChromaDB!")
            
            # Save file hash for change detection
            hash_file = os.path.join(CHROMA_PATH, "files_hash.txt")
            with open(hash_file, 'w') as f:
                f.write(self._get_files_hash())

        except Exception as e:
            print(f"⚠️ ChromaDB save failed: {e}")
            self.use_chroma = False

    def _build_tfidf(self):
        """Build TF-IDF for search - optimized"""
        if not self.chunks:
            return

        try:
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=10000,  # Reduced for speed
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
        """Search using TF-IDF - optimized"""
        if not self.chunks or self.tfidf_matrix is None:
            return []

        # Fast filtering
        candidate_indices = None
        if grade and grade in self.grade_index:
            candidate_indices = set(self.grade_index[grade])

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

        # Vectorized search (fast)
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