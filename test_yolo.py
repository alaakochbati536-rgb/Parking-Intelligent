import cv2
from tkinter import Tk, filedialog
from ultralytics import YOLO

# Charger le modèle YOLO
modele = YOLO("yolov8n.pt")

# Créer la fenêtre de sélection
fenetre = Tk()
fenetre.withdraw()

# Sélectionner une image
chemin = filedialog.askopenfilename(
    title="Sélectionner une image",
    filetypes=[("Images", "*.jpg *.jpeg *.png")]
)

if chemin:
    # Lire l'image
    image = cv2.imread(chemin)

    # Détecter les véhicules
    resultats = modele(image, conf=0.4)

    # Classes COCO : voiture, moto, bus et camion
    classes_vehicules = [2, 3, 5, 7]

    nombre_vehicules = 0

    for resultat in resultats:
        for boite in resultat.boxes:
            classe = int(boite.cls[0])

            if classe in classes_vehicules:
                nombre_vehicules += 1

    # Afficher les résultats
    image_resultat = resultats[0].plot()

    print("Nombre de véhicules détectés :", nombre_vehicules)

    cv2.imshow("Détection des véhicules", image_resultat)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Aucune image sélectionnée")