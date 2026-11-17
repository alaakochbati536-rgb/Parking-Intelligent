import cv2
import pytesseract
from tkinter import Tk, filedialog
from ultralytics import YOLO

# Configurer Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Charger le modele
modele = YOLO("plate_detector.pt")

# Selectionner une image
fenetre = Tk()
fenetre.withdraw()

chemin = filedialog.askopenfilename(
    title="Selectionner une image",
    filetypes=[("Images", "*.jpg *.jpeg *.png")]
)

if chemin:
    image = cv2.imread(chemin)

    if image is None:
        print("Erreur de chargement")
        exit()

    # Detecter la plaque
    resultats = modele(image, conf=0.05, imgsz=1280)

    if len(resultats[0].boxes) > 0:

        for boite in resultats[0].boxes:

            x1, y1, x2, y2 = map(int, boite.xyxy[0])
            plaque = image[y1:y2, x1:x2]

            # Convertir en niveaux de gris
            gris = cv2.cvtColor(plaque, cv2.COLOR_BGR2GRAY)

            # Agrandir l'image
            agrandie = cv2.resize(
                gris,
                None,
                fx=5,
                fy=5,
                interpolation=cv2.INTER_CUBIC
            )

            # Ameliorer le contraste
            agrandie = cv2.equalizeHist(agrandie)

            # Reconnaissance OCR
            texte = pytesseract.image_to_string(
                agrandie,
                config="--psm 7"
            )

            print("Plaque detectee !")
            print("Numero reconnu :", texte.strip())

            cv2.imshow("Plaque originale", plaque)
            cv2.imshow("Plaque traitee", agrandie)

            cv2.imwrite("plaque_traitee.jpg", agrandie)

    else:
        print("Aucune plaque detectee")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Aucune image selectionnee")