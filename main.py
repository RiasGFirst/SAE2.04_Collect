import paho.mqtt.client as mqtt
from datetime import datetime
import db


broker_address = "test.mosquitto.org"
port = 1883
topic1 = "IUT/Colmar2024/SAE2.04/Maison1"
topic2 = "IUT/Colmar2024/SAE2.04/Maison2"
timeout = 60


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker avec succès")
        client.subscribe(topic1)
        client.subscribe(topic2)
    else:
        print(f"Échec de connexion avec le code {rc}")


def on_message(client, userdata, message):
    print(f"Message reçu sur {message.topic}:")
    maison = message.topic.split("/")[3]
    # separation des informations dans le message
    message = message.payload.decode().split(",")
    # ['Id=B8A5F3569EFF', 'piece=sejour', 'date=20/06/2024', 'time=09:13:22', 'temp=13.78']
    id = message[0].split("=")[1]
    piece = message[1].split("=")[1]
    date = datetime.strptime(message[2].split("=")[1], "%d/%m/%Y").strftime("%Y-%m-%d")
    time = message[3].split("=")[1]
    temp = message[4].split("=")[1]
    print(f"Id: {id}")
    print(f"Piece: {piece}")
    print(f"Date: {date}")
    print(f"Heure: {time}")
    print(f"Température: {temp}")
    id_capteur = db.ensure_capteur_exists(maison, piece, id)
    db.insert_into_db(id_capteur, date, time, temp)
    print("")


def check_broker():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker_address, port, timeout)
        client.loop_start()

        while True:
            pass

    except Exception as e:
        print(f"Erreur lors de la connexion: {e}, Maître.")


if __name__ == "__main__":
    check_broker()
