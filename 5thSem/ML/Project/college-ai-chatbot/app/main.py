from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil

from .excel_processor import process_excel
from .database import add_documents
from .rag import retrieve_context, generate_answer


app = FastAPI(
    title="College AI Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():

    return {
        "message": "College AI Assistant is running"
    }


@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...)
):

    uploaded = []
    total_documents = 0

    for file in files:

        if not file.filename.endswith(
            (".xlsx", ".xls")
        ):
            continue

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        documents = process_excel(file_path)

        count = add_documents(documents)

        total_documents += count

        uploaded.append({
            "filename": file.filename,
            "documents": count
        })

    return {
        "message": "Files processed successfully",
        "files": uploaded,
        "total_documents": total_documents
    }


@app.post("/chat")
async def chat(question: str):

    context = retrieve_context(question)

    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "answer": answer
    }