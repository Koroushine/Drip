# src/config.py

import os
from dotenv import load_dotenv

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# API Configuration
# ============================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("⚠️ OPENROUTER_API_KEY not found in .env file!")
    print("   Please add: OPENROUTER_API_KEY=sk-or-v1-...")
    OPENROUTER_API_KEY = "your-key-here"

# ============================================================
# Model Configuration
# ============================================================

MODELS = {
    'best': 'anthropic/claude-3.5-sonnet',
    'gpt4': 'openai/gpt-4o',
    'gemini': 'google/gemini-2.0-flash-lite-preview-02-05',
    'fast': 'meta-llama/llama-3.2-3b-instruct',
    'free': 'openrouter/free',
}

DEFAULT_MODEL = 'free'
DEFAULT_TEMPERATURE = 0.4
DEFAULT_MAX_TOKENS = 800
DEFAULT_TOP_K = 4

# ============================================================
# Paths
# ============================================================

DATA_FOLDER = "./data"
RESULTS_FOLDER = "./results"

# ============================================================
# ChromaDB Settings
# ============================================================

USE_CHROMA = True
CHROMA_PATH = "./chroma_db"

# ============================================================
# Grade Mapping
# ============================================================

GRADE_MAPPING = {
    "hecu": "Class 8",
    "iesc": "Class 9",
    "jesc": "Class 10",
}


def get_grade_from_file(filename: str) -> str:
    """Get grade from filename prefix"""
    for prefix, grade in GRADE_MAPPING.items():
        if filename.startswith(prefix):
            return grade
    return "Unknown"


def get_class_from_filename(filename: str) -> int:
    """Extract class number from filename"""
    if filename.startswith("hecu"):
        return 8
    elif filename.startswith("iesc"):
        return 9
    elif filename.startswith("jesc"):
        return 10
    return 0


# ============================================================
# Chapter Names
# ============================================================

CHAPTER_NAMES = {
    # Class 8
    "hecu1ps.pdf": "Class 8 - Front Matter",
    "hecu101.pdf": "Class 8 - Exploring the Investigative World of Science",
    "hecu102.pdf": "Class 8 - The Invisible Living World",
    "hecu103.pdf": "Class 8 - Health: The Ultimate Treasure",
    "hecu104.pdf": "Class 8 - Electricity: Magnetic and Heating Effects",
    "hecu105.pdf": "Class 8 - Force",
    "hecu106.pdf": "Class 8 - Pressure, Winds, Storms, and Cyclones",
    "hecu107.pdf": "Class 8 - Particulate Nature of Matter",
    "hecu108.pdf": "Class 8 - Elements, Compounds, and Mixtures",
    "hecu109.pdf": "Class 8 - Solutes, Solvents, and Solutions",
    "hecu110.pdf": "Class 8 - Light: Mirrors and Lenses",
    "hecu111.pdf": "Class 8 - Keeping Time with the Skies",
    "hecu112.pdf": "Class 8 - Ecosystems",
    "hecu113.pdf": "Class 8 - Our Home: Earth",

    # Class 9
    "iesc1ps.pdf": "Class 9 - Front Matter",
    "iesc101.pdf": "Class 9 - Exploration: Entering the World of Secondary Science",
    "iesc102.pdf": "Class 9 - Cell: The Building Block of Life",
    "iesc103.pdf": "Class 9 - Tissues in Action",
    "iesc104.pdf": "Class 9 - Describing Motion Around Us",
    "iesc105.pdf": "Class 9 - Exploring Mixtures and their Separation",
    "iesc106.pdf": "Class 9 - How Forces Affect Motion",
    "iesc107.pdf": "Class 9 - Work, Energy, and Simple Machines",
    "iesc108.pdf": "Class 9 - Journey Inside the Atom",
    "iesc109.pdf": "Class 9 - Atomic Foundations of Matter",
    "iesc110.pdf": "Class 9 - Sound Waves",
    "iesc111.pdf": "Class 9 - Reproduction: How Life Continues",
    "iesc112.pdf": "Class 9 - Patterns in Life: Diversity and Classification",
    "iesc113.pdf": "Class 9 - Earth as a System",

    # Class 10
    "jesc1ps.pdf": "Class 10 - Front Matter",
    "jesc101.pdf": "Class 10 - Chemical Reactions and Equations",
    "jesc102.pdf": "Class 10 - Acids, Bases and Salts",
    "jesc103.pdf": "Class 10 - Metals and Non-metals",
    "jesc104.pdf": "Class 10 - Carbon and its Compounds",
    "jesc105.pdf": "Class 10 - Life Processes",
    "jesc106.pdf": "Class 10 - Control and Coordination",
    "jesc107.pdf": "Class 10 - How do Organisms Reproduce",
    "jesc108.pdf": "Class 10 - Heredity",
    "jesc109.pdf": "Class 10 - Light: Reflection and Refraction",
    "jesc110.pdf": "Class 10 - The Human Eye and the Colourful World",
    "jesc111.pdf": "Class 10 - Electricity",
    "jesc112.pdf": "Class 10 - Magnetic Effects of Electric Current",
    "jesc113.pdf": "Class 10 - Our Environment",
    "jesc1an.pdf": "Class 10 - Answers",
}

# ============================================================
# Chapter Topics
# ============================================================

CHAPTER_TOPICS = {
    # Class 8
    "hecu1ps.pdf": ["front matter", "preface", "introduction"],
    "hecu101.pdf": ["scientific method", "investigation", "experiment", "observation"],
    "hecu102.pdf": ["cell", "microorganism", "bacteria", "fungi", "protozoa", "nucleus", "cytoplasm"],
    "hecu103.pdf": ["health", "disease", "immunity", "vaccine", "antibiotic", "infection", "hygiene"],
    "hecu104.pdf": ["electricity", "magnet", "electromagnet", "circuit", "current", "battery"],
    "hecu105.pdf": ["force", "friction", "gravity", "motion", "weight", "pressure"],
    "hecu106.pdf": ["pressure", "wind", "storm", "cyclone", "atmosphere", "thunderstorm"],
    "hecu107.pdf": ["matter", "particle", "solid", "liquid", "gas", "melting", "boiling"],
    "hecu108.pdf": ["element", "compound", "mixture", "metal", "non-metal", "alloy"],
    "hecu109.pdf": ["solution", "solute", "solvent", "solubility", "density", "saturation"],
    "hecu110.pdf": ["light", "mirror", "lens", "reflection", "refraction", "convex", "concave"],
    "hecu111.pdf": ["moon", "phase", "calendar", "satellite", "lunar", "solar"],
    "hecu112.pdf": ["ecosystem", "food chain", "habitat", "decomposer", "biodiversity"],
    "hecu113.pdf": ["earth", "atmosphere", "hydrosphere", "biosphere", "reproduction", "climate"],

    # Class 9
    "iesc1ps.pdf": ["front matter", "preface"],
    "iesc101.pdf": ["scientific method", "model", "measurement", "units", "estimation"],
    "iesc102.pdf": ["cell", "microscope", "cell membrane", "nucleus", "cytoplasm", "organelle", "mitochondria"],
    "iesc103.pdf": ["tissue", "meristem", "epithelial", "connective", "muscle", "nervous", "joint", "skeleton"],
    "iesc104.pdf": ["motion", "displacement", "velocity", "acceleration", "graph", "kinematic"],
    "iesc105.pdf": ["mixture", "solution", "suspension", "colloid", "crystallization", "distillation"],
    "iesc106.pdf": ["force", "newton", "friction", "momentum", "inertia", "acceleration"],
    "iesc107.pdf": ["work", "energy", "power", "kinetic", "potential", "machine", "lever", "pulley"],
    "iesc108.pdf": ["atom", "nucleus", "electron", "proton", "neutron", "isotope", "isobar"],
    "iesc109.pdf": ["compound", "chemical bond", "covalent", "ionic", "molecular mass"],
    "iesc110.pdf": ["sound", "wave", "frequency", "amplitude", "echo", "sonar", "ultrasound"],
    "iesc111.pdf": ["reproduction", "asexual", "sexual", "pollination", "fertilization", "menstrual"],
    "iesc112.pdf": ["classification", "biodiversity", "taxonomy", "kingdom", "species", "vertebrate"],
    "iesc113.pdf": ["biogeochemical", "carbon cycle", "nitrogen cycle", "water cycle", "climate"],

    # Class 10
    "jesc1ps.pdf": ["front matter", "preface"],
    "jesc101.pdf": ["chemical reaction", "equation", "combination", "decomposition", "displacement", "redox"],
    "jesc102.pdf": ["acid", "base", "salt", "pH", "neutralization", "indicator"],
    "jesc103.pdf": ["metal", "non-metal", "reactivity", "corrosion", "alloy", "extraction"],
    "jesc104.pdf": ["carbon", "covalent", "hydrocarbon", "functional group", "ethanol", "soap"],
    "jesc105.pdf": ["photosynthesis", "respiration", "digestion", "circulation", "excretion"],
    "jesc106.pdf": ["nervous system", "reflex", "hormone", "coordination", "neuron"],
    "jesc107.pdf": ["reproduction", "asexual", "sexual", "flower", "human reproduction", "contraception"],
    "jesc108.pdf": ["heredity", "genetics", "mendel", "dominant", "recessive", "sex determination"],
    "jesc109.pdf": ["light", "reflection", "refraction", "mirror", "lens", "power"],
    "jesc110.pdf": ["human eye", "vision", "dispersion", "rainbow", "atmospheric refraction"],
    "jesc111.pdf": ["electricity", "current", "resistance", "ohm", "circuit", "power"],
    "jesc112.pdf": ["magnetic effect", "electromagnet", "motor", "induction", "fuse"],
    "jesc113.pdf": ["ecosystem", "food web", "energy flow", "ozone", "waste management"],
    "jesc1an.pdf": ["answers", "solutions"],
}

# ============================================================
# Topic Index
# ============================================================

TOPIC_INDEX = {
    "cell": ["hecu102.pdf", "iesc102.pdf", "jesc105.pdf"],
    "tissue": ["iesc103.pdf", "jesc105.pdf"],
    "force": ["hecu105.pdf", "iesc106.pdf"],
    "motion": ["iesc104.pdf"],
    "energy": ["iesc107.pdf"],
    "work": ["iesc107.pdf"],
    "light": ["hecu110.pdf", "jesc109.pdf", "jesc110.pdf"],
    "mirror": ["hecu110.pdf", "jesc109.pdf"],
    "lens": ["hecu110.pdf", "jesc109.pdf"],
    "electricity": ["hecu104.pdf", "jesc111.pdf", "jesc112.pdf"],
    "magnet": ["hecu104.pdf", "jesc112.pdf"],
    "atom": ["iesc108.pdf"],
    "compound": ["hecu108.pdf", "iesc109.pdf", "jesc104.pdf"],
    "element": ["hecu108.pdf", "iesc109.pdf", "jesc103.pdf"],
    "acid": ["jesc102.pdf"],
    "base": ["jesc102.pdf"],
    "salt": ["jesc102.pdf"],
    "reproduction": ["iesc111.pdf", "jesc107.pdf"],
    "heredity": ["jesc108.pdf"],
    "genetics": ["jesc108.pdf"],
    "ecosystem": ["hecu112.pdf", "jesc113.pdf"],
    "food chain": ["hecu112.pdf", "jesc113.pdf"],
    "environment": ["jesc113.pdf"],
    "health": ["hecu103.pdf"],
    "disease": ["hecu103.pdf"],
}

# ============================================================
# Test Questions
# ============================================================

TEST_QUESTIONS = {
    "Class 8": [
        "What is a cell?",
        "What is the difference between plant and animal cells?",
        "What is pressure?",
        "What are the three states of matter?",
        "What is the difference between elements and compounds?",
        "What is a food chain?",
    ],
    "Class 9": [
        "What is the difference between distance and displacement?",
        "What is Newton's first law of motion?",
        "What is the structure of an atom?",
        "What is the difference between covalent and ionic bonds?",
        "What is a food chain?",
        "What is the difference between speed and velocity?",
    ],
    "Class 10": [
        "What is a chemical reaction?",
        "What is the pH scale?",
        "What is Ohm's law?",
        "What is the difference between concave and convex mirrors?",
        "What is the role of DNA in reproduction?",
        "What is a food web?",
        "What is the difference between AC and DC current?",
    ],
}