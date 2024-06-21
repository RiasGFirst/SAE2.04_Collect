import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os


def ensure_capteur_exists(maison, piece, id_capteur):
    load_dotenv()
    db_config = {
        "host": os.getenv("HOST"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE"),
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    # Check if the capteur already exists
    cursor.execute("SELECT id FROM CAPTEUR WHERE id_capteur = %s", (id_capteur,))
    result = cursor.fetchone()
    print(result)
    if result is None:
        # Insert new capteur
        insert_capteur_query = """
        INSERT INTO CAPTEUR (maison, piece, id_capteur)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_capteur_query, (maison, piece, id_capteur))
        cnx.commit()
        print(f"Inserted new capteur: {maison}, {piece}, {id_capteur}")

        # retrieve the id of the newly inserted capteur
        cursor.execute("SELECT id FROM CAPTEUR WHERE id_capteur = %s", (id_capteur,))
        result = cursor.fetchone()
        print(result[0])
        # return the id of the newly inserted capteur
        return result[0]
    else:
        print(f"Capteur already exists: {id_capteur}")
    cnx.commit()
    cursor.close()
    cnx.close()
    return result[0]


def insert_into_db(id_capteur, date, time, temperature):
    load_dotenv()
    db_config = {
        "host": os.getenv("HOST"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE"),
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    insert_donnees_query = """
           INSERT INTO DONNEE (date, heure, temperature, id_capteur_id)
           VALUES (%s, %s, %s, %s)
           """
    cursor.execute(insert_donnees_query, (date, time, temperature, id_capteur))
    cnx.commit()
    cursor.close()
    cnx.close()
    print(f"Inserted new data: {id_capteur}, {date}, {time}, {temperature}")

