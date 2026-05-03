from typing import Annotated
from pathlib import Path
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile

from lab4_api_cv.services.image_service import analizar_imagen

app = FastAPI(title="Lab 4 API CV", version="0.1.0")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"mensaje": "API activa"}

@app.post(
    "/analyze-image",
    responses={
        400: {
            "description": "Archivo invalido o imagen no procesable.",
        }
    },
)
def analyze_image(file: Annotated[UploadFile, File(...)]) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="El archivo debe tener nombre.")

    destination = UPLOAD_DIR / file.filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resultado = analizar_imagen(str(destination))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"mensaje": "Procesamiento exitoso", "resultado": resultado}
