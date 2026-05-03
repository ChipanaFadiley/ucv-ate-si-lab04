from dataclasses import dataclass
import cv2
@dataclass
class ImageAnalyzer:
    low_threshold: int = 50
    high_threshold: int = 150

    def analyze(self, path: str) -> dict[str, int]:
        image = cv2.imread(path, 0)
        if image is None:
            raise ValueError("No se pudo leer la imagen proporcionada.")

        edges = cv2.Canny(image, self.low_threshold, self.high_threshold)
        return {
            "alto": int(image.shape[0]),
            "ancho": int(image.shape[1]),
            "bordes_detectados": int(edges.sum() > 0),
        }

def analizar_imagen(path: str) -> dict[str, int]:
    return ImageAnalyzer().analyze(path)
