"""
API surface the mobile app talks to.

Endpoints:
  POST /courses/{course_id}/upload-pdf     - add a PDF to a course
  POST /courses/{course_id}/upload-text    - add raw text to a course
  POST /courses/{course_id}/add-url        - add a web page to a course
  GET  /courses                            - list courses
  DELETE /courses/{course_id}               - remove a course
  POST /courses/{course_id}/ask            - ask a grounded question
  POST /courses/{course_id}/quiz           - generate a practice quiz
"""

import os
import json
import re

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from config import UPLOAD_DIR
import ingest
import vectorstore
import tutor

app = FastAPI(title="JEE/MBOSE Mentor API")


class UrlIn(BaseModel):
    url: str


class TextIn(BaseModel):
    text: str
    source_name: str = "pasted-text"


class QuestionIn(BaseModel):
    question: str


class QuizIn(BaseModel):
    topic: str
    num_questions: int = 5


@app.post("/courses/{course_id}/upload-pdf")
async def upload_pdf(course_id: str, file: UploadFile = File(...)):
    dest = os.path.join(UPLOAD_DIR, file.filename)
    with open(dest, "wb") as f:
        f.write(await file.read())

    chunks = ingest.process_source("pdf", dest)
    if not chunks:
        raise HTTPException(400, "Could not extract any text from that PDF.")

    count = vectorstore.add_chunks(course_id, chunks, source_name=file.filename)
    return {"status": "ok", "chunks_added": count}


@app.post("/courses/{course_id}/upload-text")
async def upload_text(course_id: str, body: TextIn):
    chunks = ingest.chunk_text(body.text)
    if not chunks:
        raise HTTPException(400, "No text provided.")

    count = vectorstore.add_chunks(course_id, chunks, source_name=body.source_name)
    return {"status": "ok", "chunks_added": count}


@app.post("/courses/{course_id}/add-url")
async def add_url(course_id: str, body: UrlIn):
    chunks = ingest.process_source("url", body.url)
    if not chunks:
        raise HTTPException(400, "Could not extract any text from that URL.")

    count = vectorstore.add_chunks(course_id, chunks, source_name=body.url)
    return {"status": "ok", "chunks_added": count}


@app.get("/courses")
async def list_courses():
    return {"courses": vectorstore.list_courses()}


@app.delete("/courses/{course_id}")
async def delete_course(course_id: str):
    vectorstore.delete_course(course_id)
    return {"status": "deleted"}


@app.post("/courses/{course_id}/ask")
async def ask(course_id: str, body: QuestionIn):
    result = tutor.answer_question(course_id, body.question)
    return result


@app.post("/courses/{course_id}/quiz")
async def quiz(course_id: str, body: QuizIn):
    result = tutor.generate_quiz(course_id, body.topic, body.num_questions)

    # Claude is asked for pure JSON; strip stray code-fences defensively and parse
    cleaned = re.sub(r"```json|```", "", result["raw"]).strip()
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        raise HTTPException(502, "Quiz generation returned malformed output, try again.")

    return parsed


@app.get("/health")
async def health():
    return {"status": "ok"}
