import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime

import database
import pytesseract
import cv2
from ultralytics import YOLO


# Configuration Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Chargement du modèle YOLO
modele = YOLO("plate_detector.pt")


# Couleurs
BG = "#F4F6F9"
BLUE = "#1E3A5F"
WHITE = "#FFFFFF"


# Fenêtre principale
fenetre = tk.Tk()
fenetre.title("Parking Intelligent")
fenetre.geometry("1100x700")
fenetre.configure(bg=BG)


# Menu gauche
menu = tk.Frame(fenetre, bg=BLUE, width=230)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

tk.Label(
    menu,
    text="PARKING\nINTELLIGENT",
    font=("Arial", 20, "bold"),
    bg=BLUE,
    fg=WHITE
).pack(pady=35)

contenu = tk.Frame(fenetre, bg=BG)
contenu.pack(side="right", fill="both", expand=True)


# Vider le contenu de la page
def vider_page():
    for widget in contenu.winfo_children():
        widget.destroy()


# Détection et lecture de la plaque
def lire_plaque_image(champ):

    chemin = filedialog.askopenfilename(
        title="Choisir une image",
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.bmp")
        ]
    )

    if not chemin:
        return

    image = cv2.imread(chemin)

    if image is None:
        messagebox.showerror(
            "Erreur",
            "Impossible de lire cette image."
        )
        return

    # Détection de la plaque avec YOLO
    resultats = modele.predict(
        image,
        conf=0.25,
        verbose=False
    )

    boites = resultats[0].boxes

    if boites is None or len(boites) == 0:
        messagebox.showwarning(
            "Attention",
            "Aucune plaque détectée !"
        )
        return

    # Sélection de la meilleure détection
    index = int(boites.conf.argmax())

    x1, y1, x2, y2 = map(
        int,
        boites.xyxy[index].tolist()
    )

    # Extraction de la plaque
    plaque_image = image[y1:y2, x1:x2]

    if plaque_image.size == 0:
        messagebox.showerror(
            "Erreur",
            "Impossible d'extraire la plaque."
        )
        return

    # Amélioration de la qualité
    plaque_image = cv2.resize(
        plaque_image,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    gris = cv2.cvtColor(
        plaque_image,
        cv2.COLOR_BGR2GRAY
    )

    # Reconnaissance OCR
    configuration = (
        "--psm 7 "
        "-c tessedit_char_whitelist="
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"
    )

    texte = pytesseract.image_to_string(
        gris,
        config=configuration
    )

    texte = texte.strip().replace(" ", "").replace("\n", "")

    if not texte:
        messagebox.showwarning(
            "Attention",
            "La plaque est détectée mais le texte est illisible."
        )
        return

    # Affichage du résultat
    champ.delete(0, tk.END)
    champ.insert(0, texte.upper())

    messagebox.showinfo(
        "Résultat OCR",
        "Plaque détectée : " + texte.upper()
        + "\n\nVérifiez le numéro avant l'enregistrement."
    )


# Tableau de bord
def afficher_dashboard():

    vider_page()

    tk.Label(
        contenu,
        text="Tableau de bord",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=BLUE
    ).pack(pady=30)

    total, occupees, disponibles = database.obtenir_statistiques()

    statistiques = [
        ("Capacité totale", total),
        ("Places occupées", occupees),
        ("Places disponibles", disponibles)
    ]

    zone = tk.Frame(contenu, bg=BG)
    zone.pack(fill="x", padx=20, pady=30)

    for titre, valeur in statistiques:

        carte = tk.Frame(
            zone,
            bg=WHITE,
            width=200,
            height=140
        )

        carte.pack(side="left", padx=15, expand=True)
        carte.pack_propagate(False)

        tk.Label(
            carte,
            text=titre,
            font=("Arial", 13),
            bg=WHITE,
            fg=BLUE
        ).pack(pady=(25, 10))

        tk.Label(
            carte,
            text=str(valeur),
            font=("Arial", 25, "bold"),
            bg=WHITE,
            fg=BLUE
        ).pack()


# Entrée d'un véhicule
def afficher_entree():

    vider_page()

    tk.Label(
        contenu,
        text="Entrée d'un véhicule",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=BLUE
    ).pack(pady=30)

    tk.Label(
        contenu,
        text="Numéro d'immatriculation :",
        font=("Arial", 14),
        bg=BG
    ).pack(pady=10)

    plaque = tk.Entry(
        contenu,
        font=("Arial", 16),
        width=25
    )
    plaque.pack(pady=10)

    tk.Button(
        contenu,
        text="Choisir une image et lire la plaque",
        font=("Arial", 12),
        bg="#2874A6",
        fg=WHITE,
        command=lambda: lire_plaque_image(plaque)
    ).pack(pady=10)

    def enregistrer():

        numero = plaque.get().strip()

        if not numero:
            messagebox.showwarning(
                "Attention",
                "Saisir la plaque !"
            )
            return

        resultat = database.enregistrer_entree(numero)

        if resultat:

            messagebox.showinfo(
                "Succès",
                "Entrée enregistrée avec succès !"
            )

            plaque.delete(0, tk.END)

        else:

            messagebox.showwarning(
                "Attention",
                "Ce véhicule est déjà présent !"
            )

    tk.Button(
        contenu,
        text="Enregistrer l'entrée",
        font=("Arial", 13, "bold"),
        bg=BLUE,
        fg=WHITE,
        command=enregistrer
    ).pack(pady=20)


# Sortie d'un véhicule
def afficher_sortie():

    vider_page()

    tk.Label(
        contenu,
        text="Sortie d'un véhicule",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=BLUE
    ).pack(pady=30)

    tk.Label(
        contenu,
        text="Numéro d'immatriculation :",
        font=("Arial", 14),
        bg=BG
    ).pack(pady=10)

    plaque = tk.Entry(
        contenu,
        font=("Arial", 16),
        width=25
    )
    plaque.pack(pady=10)

    tk.Button(
        contenu,
        text="Choisir une image et lire la plaque",
        font=("Arial", 12),
        bg="#2874A6",
        fg=WHITE,
        command=lambda: lire_plaque_image(plaque)
    ).pack(pady=10)

    def enregistrer():

        numero = plaque.get().strip()

        if not numero:
            messagebox.showwarning(
                "Attention",
                "Saisir la plaque !"
            )
            return

        resultat = database.enregistrer_sortie(numero)

        if resultat:

            messagebox.showinfo(
                "Succès",
                "Sortie enregistrée avec succès !"
            )

            plaque.delete(0, tk.END)

        else:

            messagebox.showwarning(
                "Attention",
                "Véhicule introuvable dans le parking !"
            )

    tk.Button(
        contenu,
        text="Enregistrer la sortie",
        font=("Arial", 13, "bold"),
        bg=BLUE,
        fg=WHITE,
        command=enregistrer
    ).pack(pady=20)


# Historique des véhicules
def afficher_historique():

    vider_page()

    tk.Label(
        contenu,
        text="Historique des véhicules",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=BLUE
    ).pack(pady=20)

    tableau = tk.Frame(contenu, bg=BG)
    tableau.pack(fill="both", expand=True, padx=20, pady=10)

    colonnes = (
        "Plaque",
        "Entrée",
        "Sortie",
        "Durée",
        "Statut"
    )

    liste = ttk.Treeview(
        tableau,
        columns=colonnes,
        show="headings"
    )

    for colonne in colonnes:
        liste.heading(colonne, text=colonne)
        liste.column(colonne, width=140)

    liste.pack(fill="both", expand=True)

    connexion = database.connecter()
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT plaque, date_entree, date_sortie, statut
        FROM vehicules
        ORDER BY id DESC
    """)

    for plaque, entree, sortie, statut in curseur.fetchall():

        date_entree = datetime.strptime(
            entree,
            "%Y-%m-%d %H:%M:%S"
        )

        if sortie:
            date_sortie = datetime.strptime(
                sortie,
                "%Y-%m-%d %H:%M:%S"
            )
        else:
            date_sortie = datetime.now()

        duree = date_sortie - date_entree

        heures = int(duree.total_seconds() // 3600)
        minutes = int((duree.total_seconds() % 3600) // 60)

        duree_texte = f"{heures} h {minutes} min"

        liste.insert(
            "",
            tk.END,
            values=(
                plaque,
                entree,
                sortie if sortie else "-",
                duree_texte,
                statut
            )
        )

    connexion.close()


# Boutons du menu
pages = [
    ("Tableau de bord", afficher_dashboard),
    ("Entrée véhicule", afficher_entree),
    ("Sortie véhicule", afficher_sortie),
    ("Historique", afficher_historique)
]

for nom, fonction in pages:

    tk.Button(
        menu,
        text=nom,
        font=("Arial", 12),
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        anchor="w",
        padx=20,
        pady=15,
        command=fonction
    ).pack(fill="x", padx=8, pady=5)


# Lancement de l'application
afficher_dashboard()

fenetre.mainloop()