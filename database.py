import sqlite3
from datetime import datetime


def connecter():
    return sqlite3.connect("parking.db")


def creer_tables():
    connexion = connecter()
    curseur = connexion.cursor()

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS vehicules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plaque TEXT NOT NULL,
            date_entree TEXT NOT NULL,
            date_sortie TEXT,
            statut TEXT DEFAULT 'Present'
        )
    """)

    connexion.commit()
    connexion.close()


def enregistrer_entree(plaque):
    connexion = connecter()
    curseur = connexion.cursor()

    plaque = plaque.strip().upper()

    curseur.execute("""
        SELECT id FROM vehicules
        WHERE plaque = ? AND statut = 'Present'
    """, (plaque,))

    if curseur.fetchone():
        connexion.close()
        return False

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    curseur.execute("""
        INSERT INTO vehicules (plaque, date_entree)
        VALUES (?, ?)
    """, (plaque, date))

    connexion.commit()
    connexion.close()
    return True


def enregistrer_sortie(plaque):
    connexion = connecter()
    curseur = connexion.cursor()

    plaque = plaque.strip().upper()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    curseur.execute("""
        UPDATE vehicules
        SET date_sortie = ?, statut = 'Sorti'
        WHERE plaque = ? AND statut = 'Present'
    """, (date, plaque))

    resultat = curseur.rowcount

    connexion.commit()
    connexion.close()

    return resultat > 0


creer_tables()
CAPACITE_PARKING = 50


def obtenir_statistiques():
    connexion = connecter()
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT COUNT(*)
        FROM vehicules
        WHERE statut = 'Present'
    """)

    places_occupees = curseur.fetchone()[0]
    places_disponibles = CAPACITE_PARKING - places_occupees

    connexion.close()

    return CAPACITE_PARKING, places_occupees, places_disponibles