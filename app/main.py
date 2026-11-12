from fastapi import FastAPI

app = FastAPI(title="Resume RAG Bot", description="A Resume Retrieval-Augmented Generation Bot", version="1.0.0")

@app.get("/health", summary="Health Check", description="Check the health of the Resume RAG Bot service.")
def health_check()-> dict[str, str]:
    return {"status": "healthy", "message": "Resume RAG Bot is running smoothly."}
