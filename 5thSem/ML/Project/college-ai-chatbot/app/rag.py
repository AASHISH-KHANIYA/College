import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from .database import search


# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(
    api_key=api_key
)


def retrieve_context(question):
    documents = search(question, n_results=5)

    if not documents:
        return ""

    return "\n".join(documents)


def generate_answer(question, context):

    prompt = f"""
You are the AI assistant for a college.

Answer the user's question using ONLY the information
provided in the context.

If the answer is not present in the context, say:
"I don't have that information in my college knowledge base."

Do not make up information.

Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text