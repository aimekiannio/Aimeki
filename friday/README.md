# JEE / MBOSE / NCERT AI Mentor — Backend Starter

This is the backend for a personal AI study mentor. You add course material
(PDF, pasted text, or a web URL) per course, and it answers questions and
generates quizzes grounded in that material using Claude.

## How it works

1. You upload content → `ingest.py` extracts and chunks the text.
2. Chunks get embedded locally (free, no API cost) and stored in ChromaDB,
   one collection per course.
3. When you ask a question, it retrieves the most relevant chunks and sends
   them to Claude along with your question, so answers are grounded in your
   own syllabus material rather than generic knowledge.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then paste your Anthropic API key into .env
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`. Interactive docs (auto-generated)
at `http://localhost:8000/docs` — good for testing endpoints before the mobile
app exists.

## Try it without a mobile app yet

```bash
# add a course document
curl -X POST http://localhost:8000/courses/physics11/upload-text \
  -H "Content-Type: application/json" \
  -d '{"text": "Newtons first law states...", "source_name": "chapter1"}'

# ask a question grounded in it
curl -X POST http://localhost:8000/courses/physics11/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain Newtons first law with an example"}'
```

## Not built yet (next steps)

- **Mobile app (React Native)**: a chat screen + course manager screen that
  calls these endpoints. Backend is ready for this — no changes needed to
  start wiring up the UI.
- **User accounts / auth**: right now `course_id` is just a string with no
  ownership — fine for solo use, needed before multiple users.
- **Progress tracking**: quiz results aren't stored yet. Add a table to log
  attempts per topic so weak areas can be identified over time.
- **Web ingestion for JS-heavy pages**: `add-url` uses a simple HTML fetch,
  which won't work on pages that render content via JavaScript. Add a
  headless-browser fallback (e.g. Playwright) if you hit that.
- **Chunking by chapter/heading** rather than raw paragraph length, once your
  PDFs have consistent structure — will improve retrieval quality.

## Project structure

```
backend/
  main.py          - API endpoints
  ingest.py        - PDF/text/URL -> chunked text
  vectorstore.py   - embeddings + ChromaDB storage/retrieval
  tutor.py         - Claude-powered Q&A and quiz generation
  config.py        - settings
  requirements.txt
```
