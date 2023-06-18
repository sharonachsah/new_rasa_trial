import io
import os
from datetime import datetime, timedelta, timezone
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
import sys

import speech_recognition as sr
import streamlit as st
import whisper

from trello_functions.voiceassistant import speak


@st.cache_resource
def load_audio_model(audio_model_path):
    return whisper.load_model(audio_model_path)


def recognize_speech(audio_model_path: str, start_recognition: bool = False):
    """Transcribe audio from microphone in real time using whisper."""
    last_sample = bytes()
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = 500
    recorder.dynamic_energy_threshold = False
    source = sr.Microphone(sample_rate=16000, device_index=0)
    audio_model = load_audio_model(audio_model_path)
    record_timeout = 30
    phrase_timeout = 4
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

    # st.write("Model loaded.")

    if start_recognition:
        st.write("Please speak now...")

    transcription_text_area = st.empty()

    counter = 0

    while start_recognition:
        try:
            now = datetime.now(timezone.utc)

            if not data_queue.empty():
                phrase_complete = False

                if phrase_time and now - phrase_time > timedelta(
                    seconds=phrase_timeout
                ):
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
                text = result["text"].strip()

                if phrase_complete:
                    transcription = text
                else:
                    transcription = text

                text_area_key = f"transcription_text_area_{counter}"
                counter += 1
                transcription_text_area.text_area(
                    "Transcription", transcription, key=text_area_key
                )
                speak(transcription)

                sleep(0.1)
        except KeyboardInterrupt:
            break

    return recognizer


if __name__ == "__main__":
    st.set_page_config(page_title="Real-Time Speech Recognition", page_icon="🎙️")

    st.title("Real-Time Speech Recognition")
    st.subheader("Instructions:")
    st.write("1. Click the button below to start or stop the recognition.")
    st.write(
        "2. Please speak clearly into the microphone when the recognition is active."
    )

    model_selection = st.selectbox(
        "Select Model",
        (
            "Tiny (Moderate Accuracy, Fast Response)",
            "Base (Higher Accuracy, Slow Response)",
            "Small (Highest Accuracy, Slowest Response)",
        ),
    )

    if model_selection == "Tiny (Moderate Accuracy, Fast Response)":
        audio_model_path = "X:/new_rasa_trial/whisper_models/tiny.en.pt"
    elif model_selection == "Base (Higher Accuracy, Slow Response)":
        audio_model_path = "X:/new_rasa_trial/whisper_models/base.pt"
    elif model_selection == "Small (Highest Accuracy, Slowest Response)":
        audio_model_path = "X:/new_rasa_trial/whisper_models/small.pt"

    start_recognition = st.checkbox("Start/Stop Recognition")

    if start_recognition:
        recognize_speech(audio_model_path=audio_model_path, start_recognition=True)
    else:
        recognize_speech(audio_model_path=audio_model_path, start_recognition=False)
        sys.exit()
