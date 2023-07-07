import time

import uvicorn
import whisper
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware

from actions.voiceassistant import speak

app = FastAPI()

origins = ["http://localhost", "http://localhost:8000", "http://localhost:3000", "*"]

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
    buffer = whisper.load_audio("audio.mp3", sr=16000)
    result = model.transcribe(buffer, fp16=False)
    print(result["text"])
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: {:.2f} seconds".format(execution_time))
    return result["text"]


@app.post("/botspeak")
async def botSpeak(text: str):
    print(text)
    speak(text)
    time.sleep(0.2)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)
