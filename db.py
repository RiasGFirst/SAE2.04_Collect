import mysql.connector
from dotenv import load_dotenv
import os


def insert_data(maison, piece, id_capteur, dateday, heure, temp):

    load_dotenv()

    HOST = os.getenv("HOST")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    DATABASE = os.getenv("DATABASE")

    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        cursor = conn.cursor()

        print(f"Insertion des données dans la base de données {DATABASE}...")

        cursor.execute('''
        INSERT INTO CAPTEUR (maison, piece, id_capteur) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE maison=VALUES(maison), piece=VALUES(piece)
        ''', (maison, piece, id_capteur))

        cursor.execute('''
        INSERT INTO DONNEES (dateday, heure, temp, capteur) VALUES (%s, %s, %s, %s)
        ''', (dateday, heure, temp, id_capteur))

        conn.commit()

    except mysql.connector.Error as err:
        print(err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connexion à la base de données fermée.")