import cv2
from tkinter import Tk, filedialog

# Créer la fenêtre de sélection
fenetre = Tk()
fenetre.withdraw()

# Sélectionner une image
chemin = filedialog.askopenfilename(
    title="Sélectionner une image de véhicule",
    filetypes=[
        ("Images", "*.jpg *.jpeg *.png")
    ]
)

# Vérifier si une image est sélectionnée
if chemin:
    image = cv2.imread(chemin)

    if image is not None:
        cv2.imshow("Image du véhicule", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Erreur lors du chargement de l'image")
else:
    print("Aucune image sélectionnée")