from fastapi import FastAPI, File, HTTPException, UploadFile

from pathlib import Path

app = FastAPI(title="Resume RAG Bot", description="A Resume Retrieval-Augmented Generation Bot", version="1.0.0")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@app.get("/health", summary="Health Check", description="Check the health of the Resume RAG Bot service.")
def health_check()-> dict[str, str]:
    return {"status": "healthy", "message": "Resume RAG Bot is running smoothly."}

@app.post("/resumes", summary="Upload Resume", description="Upload a new resume to the system.")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, str | int]:
    filename = file.filename or ""

    if Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File must be no larger than 5 MB.",
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not appear to be a PDF.",
        )

    return {
        "status": "accepted",
        "filename": filename,
        "size_bytes": len(content),
    }