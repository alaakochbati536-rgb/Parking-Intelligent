import tkinter as tk
from tkinter import messagebox
import database

BG = "#F4F6F9"
BLUE = "#1E3A5F"
WHITE = "#FFFFFF"

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


def vider_page():
    for widget in contenu.winfo_children():
        widget.destroy()


def afficher_dashboard():
    vider_page()

    tk.Label(
        contenu,
        text="Tableau de bord",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=BLUE
    ).pack(pady=30)

    connexion = database.connecter()
    curseur = connexion.cursor()

    curseur.execute(
        "SELECT COUNT(*) FROM vehicules WHERE statut='Present'"
    )
    presents = curseur.fetchone()[0]

    connexion.close()

    tk.Label(
        contenu,
        text=f"Véhicules présents : {presents}",
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=BLUE,
        padx=40,
        pady=30
    ).pack(pady=30)


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

    plaque = tk.Entry(contenu, font=("Arial", 16), width=25)
    plaque.pack(pady=10)

    def enregistrer():
        numero = plaque.get().strip()

        if not numero:
            messagebox.showwarning("Attention", "Saisir la plaque !")
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

    plaque = tk.Entry(contenu, font=("Arial", 16), width=25)
    plaque.pack(pady=10)

    def enregistrer():
        numero = plaque.get().strip()

        if not numero:
            messagebox.showwarning("Attention", "Saisir la plaque !")
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

    colonnes = ("Plaque", "Entrée", "Sortie", "Statut")

    from tkinter import ttk

    liste = ttk.Treeview(
        tableau,
        columns=colonnes,
        show="headings"
    )

    for colonne in colonnes:
        liste.heading(colonne, text=colonne)
        liste.column(colonne, width=150)

    liste.pack(fill="both", expand=True)

    connexion = database.connecter()
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT plaque, date_entree, date_sortie, statut
        FROM vehicules
        ORDER BY id DESC
    """)

    for ligne in curseur.fetchall():
        liste.insert("", tk.END, values=ligne)

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


afficher_dashboard()

fenetre.mainloop()