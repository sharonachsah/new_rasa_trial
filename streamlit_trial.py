import io
import sys
from datetime import datetime, timedelta, timezone
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

import requests
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
    recorder.energy_threshold = 300
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

    bot_response_text_area = st.empty()

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
                text = result["text"]
                # Save list to string
                # text = " ".join(text)
                # print("Text from transcribe:", text, type(text))

                # text = text[-1].strip()

                transcription = text if phrase_complete else text
                text_area_key = f"transcription_text_area_{counter}"
                counter += 1
                st.markdown(
                    body=f'<div><textarea style="text-align: right;width: 100%; height: 70px; font-size: 16px; font-weight: bold; color: #ffffff; background-color: #262730; border: 3px solid #0e1117; border-radius: 10px; padding: 10px; resize: none;" readonly>{transcription}</textarea></div>',
                    unsafe_allow_html=True,
                )
                # bot_response_text_area.text_area(
                #     label="Transcription",
                #     value=transcription,
                #     key=text_area_key,
                #     height=70,
                # )

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
    print("\nTranscription Payload:", transcription)

    payload = {"message": transcription.lower()}

    response = requests.post(
        url=f"{rasa_server_url}/webhooks/rest/webhook", json=payload
    )

    if response.status_code == 200:
        bot_response: str = response.json()[0]["text"]
        print("Bot said: ", bot_response)
        # st.write(
        #     "Bot said: ", bot_response, "What else can I do for you?"
        # )  # Display bot's response in Streamlit UI

        st.markdown(
            body=f'<div><textarea style="text-align: left;width: 100%; height: 70px; font-size: 16px; font-weight: bold; color: rgb(255, 255, 255); background-color: rgb(38, 39, 48); border: 3px solid rgb(14, 17, 23); border-radius: 10px; padding: 10px; resize: none;" readonly>Bot said: {bot_response}</textarea></div>',
            unsafe_allow_html=True,
        )
        speak(f"{bot_response} What else can I do for you?")
        sleep(0.2)
    else:
        print("Error: ", response.status_code, response.text)


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
        audio_model_path = "X:/new_rasa_trial/whisper_models/base.en.pt"
    elif model_selection == "Small (Highest Accuracy, Slowest Response)":
        audio_model_path = "X:/new_rasa_trial/whisper_models/small.en.pt"

    if start_recognition := st.checkbox("Start/Stop Recognition"):
        recognize_speech(audio_model_path=audio_model_path, start_recognition=True)
    else:
        recognize_speech(audio_model_path=audio_model_path, start_recognition=False)
        sys.exit()
