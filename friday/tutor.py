"""
Where the actual "mentor" behavior lives: takes retrieved course chunks
plus a student question and asks Claude to answer grounded in that
material, in a JEE/MBOSE-appropriate way.
"""

import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from vectorstore import query

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

TUTOR_SYSTEM_PROMPT = """You are an academic mentor for a student preparing for \
JEE Main, JEE Advanced, and MBOSE board exams (Classes 11-12, NCERT syllabus).

Rules:
- Base your answer primarily on the CONTEXT provided below, which comes from \
the student's own course material.
- If the context doesn't fully cover the question, say so plainly, then you \
may supplement with general NCERT-level knowledge - but flag clearly which \
part is from their material and which is general knowledge.
- Show step-by-step working for numericals/derivations, the way a JEE answer \
should be structured.
- Match the difficulty level implied by the question (basic NCERT concept vs \
JEE Advanced level problem).
- Be encouraging but not falsely reassuring - if the student's approach is \
wrong, correct it directly.
"""


def answer_question(course_id: str, question: str) -> dict:
    hits = query(course_id, question, n_results=5)

    if not hits:
        context_block = "(No course material found for this course yet.)"
    else:
        context_block = "\n\n---\n\n".join(
            f"[Source: {h['source']}]\n{h['text']}" for h in hits
        )

    user_message = f"CONTEXT:\n{context_block}\n\nQUESTION:\n{question}"

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1500,
        system=TUTOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    answer_text = "".join(
        block.text for block in response.content if block.type == "text"
    )

    return {
        "answer": answer_text,
        "sources_used": list({h["source"] for h in hits}),
    }


def generate_quiz(course_id: str, topic: str, num_questions: int = 5) -> dict:
    hits = query(course_id, topic, n_results=8)
    context_block = "\n\n---\n\n".join(h["text"] for h in hits) or "(no material found)"

    prompt = f"""Using ONLY the material below, write {num_questions} JEE-style \
practice questions on "{topic}". Mix difficulty: some NCERT-basic, some JEE \
Main level, at least one JEE Advanced level if the material supports it.

For each question give: the question, 4 options if MCQ (or state if it's \
numerical), the correct answer, and a short explanation.

MATERIAL:
{context_block}

Respond ONLY in this JSON structure, nothing else:
{{
  "questions": [
    {{"question": "...", "options": ["A", "B", "C", "D"], "answer": "...", "explanation": "..."}}
  ]
}}"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = "".join(block.text for block in response.content if block.type == "text")
    return {"raw": raw}  # main.py parses/validates this before returning to the app
