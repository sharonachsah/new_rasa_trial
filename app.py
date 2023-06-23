import io
import sys
from datetime import datetime, timedelta, timezone
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

import requests
import speech_recognition as sr
import whisper
from fastapi import FastAPI

from actions.voiceassistant import speak

app = FastAPI()

@app.get("/ping")
async def ping():
    return "Hello World!"

@app.post("/voice_recognition")
def recognize_speech():
    """
    This function uses a pre-trained audio model to transcribe speech from a microphone and sends the
    transcription to a Rasa chatbot.
    :return: a `recognizer` object of type `speech_recognition.Recognizer`.
    """
    audio_model_path = "C:/new_rasa_trial/whisper_models/tiny.en.pt"
    last_sample = bytes()
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = 100
    recorder.dynamic_energy_threshold = False
    source = sr.Microphone(sample_rate=16000, device_index=0)
    audio_model = whisper.load_model(audio_model_path)
    record_timeout = 15
    phrase_timeout = 3
    temp_file = NamedTemporaryFile().name
    transcription = ""
    phrase_time = None

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        data = audio.get_raw_data()
        data_queue.put(data)

    recognizer = recorder.listen_in_background(
        source, record_callback, phrase_time_limit=record_timeout
    )

    while True:
        try:
            now = datetime.now(timezone.utc)

            if not data_queue.empty():
                phrase_complete = False

                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True

                phrase_time = now

                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                audio_data = sr.AudioData(
                    last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH
                )
                wav_data = io.BytesIO(audio_data.get_wav_data())

                with open(temp_file, "w+b") as f:
                    f.write(wav_data.read())

                result = audio_model.transcribe(temp_file, fp16=False)
                text = result["text"]

                if phrase_complete:
                    transcription = text
                else:
                    transcription += text

                if transcription:
                    send_transcription_to_rasa(transcription)
                # speak(transcription)
                sleep(0.2)
        except KeyboardInterrupt:
            break

    return recognizer


def send_transcription_to_rasa(transcription: str):
    """Send transcription to Rasa and display bot's response in Streamlit UI."""
    rasa_server_url = "http://localhost:5005"
    # Remove dot from transcription
    transcription = transcription.strip(".")
    if transcription in {
        "Bye",
        "bye",
        "Goodbye",
        "goodbye",
        "See you later",
        "see you later",
        "Bye!",
        "bye!",
        "Goodbye!",
        "goodbye!",
        "See you later!",
        "see you later!",
    }:
        start_recognition = False
        sys.exit()

    print("\nTranscription Payload:", transcription)

    payload = {"message": transcription.lower()}

    response = requests.post(
        url=f"{rasa_server_url}/webhooks/rest/webhook", json=payload
    )

    if response.status_code == 200:
        bot_response: str = response.json()[0]["text"]
        speak(f"{bot_response}")
        sleep(0.2)
    else:
        print("Error: ", response.status_code, response.text)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
