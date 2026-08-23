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
    - **Periodic Table**: An interactive table of all 118 elements with detailed properties, electron configurations, and element details.
    - **Chemical Equation Balancer**: An advanced tool for balancing chemical equations with step-by-step solutions and visual feedback.
    - **Molar Mass Calculator**: A utility for computing molecular weights with a detailed element-by-element breakdown and percentage composition.
    - **Virtual Lab Simulation**: An interactive chemistry lab with beakers, chemicals, real-time reactions, and particle effects. Mix chemicals and observe reactions like neutralization, gas evolution, and precipitation.
    - **SPDF Orbital Atlas**: Interactive 3D visualizations of all 16 atomic orbital shapes (s, p, d, f orbitals) with multiple viewing modes and rotation controls.
    - **Solubility Table**: A comprehensive reference for ionic compound solubilities with search functionality and filter options.

**3. AI Tutor with RAG**

- An AI-powered chatbot that provides personalized learning assistance.
- The tutor answers questions, provides explanations, and offers hints based on a comprehensive knowledge base.
- The system uses a RAG architecture, combining a large language model with a vector database (ChromaDB) for context-aware responses.
- Offline mode with built-in knowledge base when the AI server is not available.

**4. Content Management**

- Structured notes, definitions, formulas, and examples for each subject.
- Curated video content to supplement theoretical learning.

---

## Project Structure

The repository is organized as follows:

```text
Drip/
├── index.html
├── chatbot.html
├── physics_hub.html
├── chemistry_hub_landing.html
├── chemistry_hub.html
├── chemistry_labs.html
├── chemistry_equation_balancer.html
├── chemistry_molar_mass_calculator.html
├── chemistry_virtual_lab.html
├── chemistry_spdf_orbital_atlas.html
├── chemistry_solubility_table.html
├── biology_hub.html
├── README.md
│
├── photoes/
├── vidoes/
├── testing/
│
└── rag-chatbot/
    ├── app.py
    ├── requirements.txt
    ├── .env
    │
    ├── data/
    ├── chroma_db/
    │
    └── src/
        ├── config.py
        ├── knowledge_base_chroma.py
        ├── tutor.py
        ├── rag_chain.py
        ├── student_profile.py
        └── utils.py
```

---

## Technology Stack

**Frontend**

- HTML5
- CSS3 (Custom properties, Glassmorphism, Flexbox/Grid, Animations)
- JavaScript (ES6)
- Font Awesome (Icon library)
- Marked.js (Markdown rendering)

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

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Drip
```

### Step 2: Set Up the Python Environment

```bash
cd rag-chatbot
python -m venv venv310

# Windows
venv310\Scripts\activate

# macOS/Linux
source venv310/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the `rag-chatbot` directory:

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

Obtain an API key from OpenRouter.

### Step 4: Prepare the Knowledge Base

Place the NCERT PDF files for Classes 8, 9, and 10 in:

```text
rag-chatbot/data/
```

The system will automatically process and index these files on the first run.

### Step 5: Verify the Installation

```bash
python -c "import numpy, pandas, sklearn, chromadb; print('All dependencies installed successfully.')"
```

---

## Running the Application

The application runs on two separate servers for optimal performance.

### Start the AI Tutor Server

```bash
cd rag-chatbot

# Windows
venv310\Scripts\activate

# macOS/Linux
source venv310/bin/activate

python app.py
```

The AI server will start at:

```text
http://localhost:5000
```

### Start the Web Server

Open a **new terminal**:

```bash
cd Drip
python -m http.server 8000
```

The website will be available at:

```text
http://localhost:8000
```

### Access the Platform

- Home Page: `http://localhost:8000`
- All Subject Pages: `http://localhost:8000`
- AI Tutor: Click the AI Tutor card on the home page → `http://localhost:5000/chatbot.html`

### First-Time Load

- The initial startup of the AI server may take 30–60 seconds to process and index the PDFs.
- Subsequent starts will be significantly faster (1–3 seconds) due to ChromaDB persistence.
- The website loads instantly regardless of the AI server state.

---

## Usage Guide

### Home Page

- Navigate to subject hubs: Physics, Chemistry, and Biology.
- Access the AI Tutor directly.

### Subject Hubs

- Select **Theory** for structured notes and content.
- Select **Interactive Labs** for hands-on tools.

### Chemistry Labs

- **Periodic Table**: Click an element to view its properties, electron configuration, and details.
- **Equation Balancer**: Input an equation such as `H2 + O2 -> H2O` and click "Balance" to see step-by-step solutions.
- **Molar Mass Calculator**: Enter a formula such as `H2O` to compute its molar mass with element breakdown.
- **Virtual Lab**: Mix chemicals from the available options, adjust temperature, and observe real-time reactions with particle effects.
- **SPDF Orbital Atlas**: Explore all 16 atomic orbitals with interactive 3D visualizations. Switch between views such as 3D, Top, Side, and Wireframe, and toggle rotation.
- **Solubility Table**: Search for compounds, filter by solubility type, and view detailed rules and exceptions.

### AI Tutor

- Type a science-related question in the chat interface.
- The tutor responds with context-aware explanations based on the NCERT knowledge base.
- If the AI server is unavailable, the tutor automatically switches to offline mode using the built-in knowledge base.
- The system tracks student progress and can provide personalized recommendations.

---

## Development Notes

### Performance Optimization

- ChromaDB is used for persistent storage to reduce load times.
- TF-IDF vectorization is optimized with reduced feature dimensions for faster search.
- The website and AI server run on separate ports to avoid conflicts and improve performance.
- Particle animations are limited to improve frontend performance.

### Customization

Modify `src/config.py` to adjust:

- Default model and temperature.
- ChromaDB settings.
- Chunk size and overlap for text processing.

### Adding New Content

- Place new PDF files in the `data/` directory.
- Update `CHAPTER_NAMES` and `CHAPTER_TOPICS` in `src/config.py` if needed.
- The system will automatically index new files on restart.

---

## Troubleshooting

### Issue: onnxruntime DLL load error on Windows

- Install the Microsoft Visual C++ Redistributable.
- Alternatively, use an older version:

```bash
pip install onnxruntime==1.14.1
```

### Issue: ChromaDB import error

```bash
pip install chromadb==0.4.22 --force-reinstall --no-cache-dir
```

### Issue: Slow first load

- This is expected as the system indexes PDFs for the first time.
- Ensure the `data/` folder contains the required PDFs.

### Issue: API key not recognized

- Verify that the `.env` file exists in the `rag-chatbot` directory.
- Ensure the key format is correct and starts with `sk-or-v1-`.

### Issue: Server not starting

Check that ports are not already in use:

```bash
netstat -ano | findstr :5000
netstat -ano | findstr :8000
```

Then activate the virtual environment before running:

```bash
python app.py
```

### Issue: Chatbot not connecting

- Ensure the AI server is running on port 5000.
- Check that the website is running on port 8000.
- The chatbot card on the home page automatically redirects to the correct port.

---

## Contributing

Contributions are welcome. Please follow these guidelines:

- Fork the repository and create a feature branch.
- Ensure code quality and consistency with the existing style.
- Update documentation for any new features.
- Submit a pull request with a clear description of changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For questions or support, please contact the project maintainer:

- **Name:** Koroushine
- **Project:** Drip – Interactive Science Learning

---

*Last updated: August 2026*