import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

# Where uploaded files and the local vector DB live
DATA_DIR = os.environ.get("DATA_DIR", "./data")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

# Chunking
CHUNK_SIZE = 900        # characters per chunk
CHUNK_OVERLAP = 150     # overlap between chunks so context isn't cut mid-idea

# Embedding model (runs locally, free, no API needed)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

os.makedirs(CHROMA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
