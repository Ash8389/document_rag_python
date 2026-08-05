import os, shutil, uuid

from fastapi import APIRouter, UploadFile, File

from app.services.ingest_service import IngestService

ingest_service = IngestService()

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)

@router.post("/pdf")
async def ingest_pdf(file : UploadFile = File(...)):

    os.makedirs("document", exist_ok=True)

    file_path = os.path.join("document", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await ingest_service.inget_service(path = file_path)

    return {
        "message": "Uploaded successfully",
        "path": file_path
    }