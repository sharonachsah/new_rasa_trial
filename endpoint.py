import time
from time import sleep

import requests
import uvicorn
import whisper
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from actions.voiceassistant import speak

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return "pong"


@app.post("/audio")
async def audio_model_load(file: bytes = File()):
    with open("audio.mp3", "wb") as f:
        f.write(file)
    start_time = time.time()
    model = whisper.load_model("C:/new_rasa_trial/whisper_models/base.en.pt")
    buffer = whisper.load_audio("audio.mp3",sr=16000)
    result = model.transcribe(buffer,fp16=False)
    print(result["text"])
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: {:.2f} seconds".format(execution_time))
    return result["text"]

@app.post("/botspeak")
async def botSpeak(text: str):
    print(text)
    speak(text)
    sleep(0.2)

# def send_transcription_to_rasa(transcription: str):
#     """Send transcription to Rasa and display bot's response in Streamlit UI."""
#     rasa_server_url = "http://localhost:5005"
#     # Remove dot from transcription
#     transcription = transcription.strip(".")

#     print("\nTranscription Payload:", transcription)

#     payload = {"message": transcription.lower()}

#     response = requests.post(
#         url=f"{rasa_server_url}/webhooks/rest/webhook", json=payload
#     )
#     bot_response: str = response.json()[0]["text"]
#     print("Bot said: ", bot_response)
#     speak(f"{bot_response}")
#     sleep(0.2)

    # if response.status_code == 200:
    #     bot_response: str = response.json()[0]["text"]
    #     print("Bot said: ", bot_response)
    #     # st.write(
    #     #     "Bot said: ", bot_response, "What else can I do for you?"
    #     # )  # Display bot's response in Streamlit UI
    #     speak(f"{bot_response}")
    #     sleep(0.2)
    # else:
    #     print("Error: ", response.status_code, response.text)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)