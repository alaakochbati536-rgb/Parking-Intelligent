import cv2
import pytesseract
import numpy as np

# Définir le chemin de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Créer une image blanche
image = 255 * np.ones((200, 600, 3), dtype="uint8")

# Écrire un numéro de plaque d'immatriculation
cv2.putText(
    image,
    "123 TUN 4567",
    (30, 120),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.5,
    (0, 0, 0),
    3
)

# Reconnaître le texte dans l'image
texte = pytesseract.image_to_string(image)

# Afficher le résultat
print("Texte détecté :", texte)