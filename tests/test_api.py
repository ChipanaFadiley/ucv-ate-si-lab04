from pathlib import Path

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from lab4_api_cv.api.main import app
from lab4_api_cv.services.image_service import analizar_imagen

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"mensaje": "API activa"}


def test_api_analyze_image(tmp_path: Path) -> None:
    image_path = tmp_path / "test_image.png"
    image = np.zeros((20, 20), dtype=np.uint8)
    cv2.rectangle(image, (5, 5), (15, 15), 255, 1)
    cv2.imwrite(str(image_path), image)

    with image_path.open("rb") as image_file:
        response = client.post(
            "/analyze-image",
            files={"file": ("test_image.png", image_file, "image/png")},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["mensaje"] == "Procesamiento exitoso"
    assert body["resultado"]["alto"] == 20
    assert body["resultado"]["ancho"] == 20
    assert body["resultado"]["bordes_detectados"] == 1


def test_api_rejects_invalid_image() -> None:
    response = client.post(
        "/analyze-image",
        files={"file": ("archivo.txt", b"esto no es una imagen", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "No se pudo leer la imagen proporcionada."
    }


def test_service_raises_error_for_invalid_path(tmp_path: Path) -> None:
    invalid_path = tmp_path / "missing_image.png"

    with pytest.raises(ValueError, match="No se pudo leer la imagen proporcionada."):
        analizar_imagen(str(invalid_path))
