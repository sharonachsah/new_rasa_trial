## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions


import requests
import actions.speechtotext as stt

# sender = input("What is your name?\n")

bool_val: bool = True
BOT_MESSAGE = ""
MESSAGE = ""
while BOT_MESSAGE != "Bye":
    if MESSAGE in ["Bye", "bye"]:
        bool_val: bool = False
    MESSAGE = stt.recognize_speech(
        audio_model="X:/new_rasa_trial/whisper_models/tiny.en.pt", bool_val=bool_val
    )
    r = requests.post(
        url="http://localhost:5002/webhooks/rest/webhook",
        json={"message": MESSAGE},
        timeout=200,
    )

    print("Sending message now...")
    MESSAGE = ""

    print("Bot says, ", end=" ")
    for i in r.json():
        BOT_MESSAGE = i["text"]
        print(f"{i['text']}")
