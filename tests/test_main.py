from fastapi.testclient import TestClient

from app.main import MAX_FILE_SIZE, app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "Resume RAG Bot is running smoothly.",
    }


def test_upload_valid_pdf():
    pdf_content = b"%PDF-1.7\nexample PDF content"

    response = client.post(
        "/resumes",
        files={"file": ("sample.pdf", pdf_content, "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "accepted",
        "filename": "sample.pdf",
        "size_bytes": len(pdf_content),
    }


def test_upload_rejects_non_pdf_extension():
    response = client.post(
        "/resumes",
        files={"file": ("resume.txt", b"%PDF-1.7\nexample", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed."


def test_upload_rejects_invalid_pdf_content():
    response = client.post(
        "/resumes",
        files={"file": ("resume.pdf", b"not a PDF", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The uploaded file does not appear to be a PDF."


def test_upload_rejects_oversized_pdf():
    oversized_content = b"%PDF-" + b"x" * MAX_FILE_SIZE

    response = client.post(
        "/resumes",
        files={"file": ("large.pdf", oversized_content, "application/pdf")},
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "File must be no larger than 5 MB."