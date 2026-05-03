from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient

from lab4_api_cv.api.main import app

client = TestClient(app)

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
