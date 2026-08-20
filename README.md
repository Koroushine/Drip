# Drip

DRIP is a student-first learning platform for Classes 8–10, bringing together notes, definitions, formulas, examples, and curated videos for Science and Social Science—all in one clean, interactive, and user-friendly experience.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Development Notes](#development-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Drip is designed to provide a seamless learning experience for secondary school students. The platform combines structured theoretical content with interactive tools and an AI-powered tutor, making it a comprehensive resource for self-study and revision.

The application is divided into three core subject areas—Physics, Chemistry, and Biology—with a dedicated Artificial Intelligence tutor that leverages a Retrieval-Augmented Generation (RAG) system. This system is built upon a knowledge base derived from NCERT textbooks for Classes 8, 9, and 10.

---

## Features

The platform is organized into the following key modules:

**1. Subject Hubs**
- Dedicated landing pages for Physics, Chemistry, and Biology.
- Each hub provides access to theoretical content, interactive labs, and topic-specific resources.

**2. Interactive Laboratories**
- A suite of interactive tools designed to reinforce learning through practice and experimentation:
    - **Periodic Table**: An interactive table of all 118 elements with detailed properties and electron configurations.
    - **Chemical Equation Balancer**: An advanced tool for balancing chemical equations with step-by-step solutions.
    - **Molar Mass Calculator**: A utility for computing molecular weights with a detailed element-by-element breakdown.
    - **Additional Labs**: Includes a Virtual Lab Simulation, SPDF Orbital Atlas, and Solubility Table (currently under development).

**3. AI Tutor with RAG**
- An AI-powered chatbot that provides personalized learning assistance.
- The tutor answers questions, provides explanations, and offers hints based on a comprehensive knowledge base.
- The system uses a RAG architecture, combining a large language model with a vector database (ChromaDB) for context-aware responses.

**4. Content Management**
- Structured notes, definitions, formulas, and examples for each subject.
- Curated video content to supplement theoretical learning.

---

## Project Structure

The repository is organized as follows:

Drip/
├── index.html # Home page
├── chatbot.html # AI Tutor interface
├── physics_hub.html # Physics hub page
├── chemistry_hub_landing.html # Chemistry landing page
├── chemistry_hub.html # Chemistry theory content
├── chemistry_labs.html # Chemistry interactive labs
├── chemistry_equation_balancer.html # Equation balancing tool
├── chemistry_molar_mass_calculator.html # Molar mass calculator
├── biology_hub.html # Biology hub page
├── README.md # Project documentation
│
├── photoes/ # Image assets
├── vidoes/ # Video content
├── testing/ # Test suite
│
└── rag-chatbot/ # AI Tutor RAG system
├── app.py # Flask server for the chatbot
├── requirements.txt # Python dependencies
├── .env # Environment variables (API keys)
│
├── data/ # NCERT PDF source files
├── chroma_db/ # ChromaDB persistence
│
└── src/ # Core RAG modules
├── config.py # Configuration settings
├── knowledge_base_chroma.py # ChromaDB knowledge base
├── tutor.py # AI Tutor logic
├── rag_chain.py # RAG pipeline
├── student_profile.py # Student progress tracking
└── utils.py # Helper functions


---

## Technology Stack

**Frontend**
- HTML5
- CSS3 (Custom properties, Glassmorphism, Flexbox/Grid)
- JavaScript (ES6)
- Font Awesome (Icon library)

**Backend (AI Tutor)**
- Python 3.10+
- Flask (Web framework)
- ChromaDB (Vector database for knowledge persistence)
- LangChain (Orchestration for RAG pipeline)
- scikit-learn (TF-IDF vectorization)
- sentence-transformers (Embedding generation)

**AI and LLM**
- OpenRouter API (Interface for various LLMs)
- Custom RAG implementation

**Key Python Packages**
- numpy, pandas, scikit-learn
- pypdf2, pdfplumber
- chromadb, langchain, langchain-community
- flask, flask-cors
- python-dotenv, requests

---

## Installation and Setup

Follow the steps below to set up the project locally.

**Prerequisites**
- Python 3.10 or higher
- Node.js (optional, for frontend development)
- Git

**Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd Drip

**Step 2: Set Up the Python Environment**
```bash
cd rag-chatbot
python -m venv venv310
source venv310/bin/activate  # On Windows: venv310\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

**Step 3: Configure Environment Variables**
Create a .env file in the rag-chatbot directory with the following content:
```bash
OPENROUTER_API_KEY=your-openrouter-api-key-here

Obtain an API key from OpenRouter (https://openrouter.ai/keys).

**Step 4: Prepare the Knowledge Base**
Place the NCERT PDF files (Classes 8, 9, 10) in the rag-chatbot/data/ directory.
The system will automatically process and index these files on the first run.

**Step 5: Verify the Installation**
```bash
python -c "import numpy, pandas, sklearn, chromadb; print('All dependencies installed successfully.')"

##Running the Application
**Start the AI Tutor Server**
```bash
cd rag-chatbot
source venv310/bin/activate  # On Windows: venv310\Scripts\activate
python app.py

- The server will start at http://localhost:5000.

##Access the Platform

**Open index.html directly in your browser.**

- Use the AI Tutor at http://localhost:5000 (when the server is running).

**First-Time Load**

The initial startup may take 30–60 seconds to process and index the PDFs.

Subsequent starts will be significantly faster (1–3 seconds) due to ChromaDB persistence.