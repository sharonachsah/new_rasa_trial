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
    recorder.energy_threshold = 100
    recorder.dynamic_energy_threshold = False
    source = sr.Microphone(sample_rate=16000, device_index=0)
    audio_model = load_audio_model(audio_model_path)
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

start_recognition = None

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
        print("Bot said: ", bot_response)
        # st.write(
        #     "Bot said: ", bot_response, "What else can I do for you?"
        # )  # Display bot's response in Streamlit UI

        st.markdown(
            body=f'<div><textarea style="text-align: left;width: 100%; height: 70px; font-size: 16px; font-weight: bold; color: rgb(255, 255, 255); background-color: rgb(38, 39, 48); border: 3px solid rgb(14, 17, 23); border-radius: 10px; padding: 10px; resize: none;" readonly>Bot said: {bot_response}</textarea></div>',
            unsafe_allow_html=True,
        )
        speak(f"{bot_response}")
        sleep(0.2)
    else:
        print("Error: ", response.status_code, response.text)


if __name__ == "__main__":
    st.set_page_config(page_title="Real-Time Speech Recognition", page_icon="🎙️")

    st.header("TrelloTalk: A Voice-Powered TaskMaster!")
    st.write("Instructions: Click the button below to start the TrelloTalk Bot.")
    # st.write("1. Click the button below to start or stop TrelloTalk Bot..")
    # st.write(
    #     "2. Please speak clearly into the microphone when the recognition is active."
    # )

    # model_selection = st.selectbox(
    #     "Select Model",
    #     (
    #         "Tiny (Moderate Accuracy, Fast Response)",
    #         "Base (Higher Accuracy, Slow Response)",
    #         "Small (Highest Accuracy, Slowest Response)",
    #     ),
    # )

    # if model_selection == "Tiny (Moderate Accuracy, Fast Response)":
        # audio_model_path = "C:/new_rasa_trial/whisper_models/tiny.en.pt"
    # elif model_selection == "Base (Higher Accuracy, Slow Response)":
    #     audio_model_path = "C:/new_rasa_trial/whisper_models/base.en.pt"
    # elif model_selection == "Small (Highest Accuracy, Slowest Response)":
    #     audio_model_path = "C:/new_rasa_trial/whisper_models/small.en.pt"

    # mic = st.markdown(body = '<div><button style="padding: 25px; border-color: rgb(255, 249, 236); border-radius: 50%; position: fixed; margin-top: 10%; margin-left: 60%;width: 100px;">🎙️</button></div>', unsafe_allow_html=True)
    # start_recognition = st.markdown(
    #     body='<div data-stale="false" width="704" class="element-container css-1hynsf2 esravye2"><div class="row-widget stButton" style="width: 704px;"><button kind="secondary" class="css-b3z5c9 e1ewe7hr10" style="padding: 15px; border-color: rgb(255, 249, 236); position: fixed; margin-top: 10%; margin-left: 60%;size: 100px 120px; border-radius:50%; background-color: rgb(123 111 124 / 29%)"> <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="64" height="64" viewBox="0 0 64 64"> <ellipse cx="32" cy="61" opacity=".3" rx="15" ry="3"></ellipse><path fill="#a7b3c7" d="M32,42L32,42c-6.627,0-12-5.373-12-12V18c0-6.627,5.373-12,12-12h0c6.627,0,12,5.373,12,12v12	C44,36.627,38.627,42,32,42z"></path><path fill="#a7b3c7" d="M32,51c-11.58,0-21-9.42-21-21c0-1.657,1.343-3,3-3s3,1.343,3,3c0,8.271,6.729,15,15,15 s15-6.729,15-15c0-1.657,1.343-3,3-3s3,1.343,3,3C53,41.58,43.58,51,32,51z"></path><path fill="#a7b3c7" d="M32,57c-1.657,0-3-1.343-3-3v-6c0-1.657,1.343-3,3-3s3,1.343,3,3v6C35,55.657,33.657,57,32,57z"></path><path fill="#6f7b91" d="M44,25h-5c-1.104,0-2,0.896-2,2s0.896,2,2,2h5V25z"></path><path fill="#6f7b91" d="M37,20c0,1.104,0.896,2,2,2h5v-4h-5C37.896,18,37,18.896,37,20z"></path><path fill="#6f7b91" d="M25,22c1.104,0,2-0.896,2-2s-0.896-2-2-2h-5v4H25z"></path><path fill="#6f7b91" d="M27,27c0-1.104-0.896-2-2-2h-5v4h5C26.104,29,27,28.104,27,27z"></path><g><path d="M39,30c0,3.86-3.14,7-7,7c-2.402,0-4.405,1.695-4.886,3.953C28.607,41.621,30.258,42,32,42 c6.627,0,12-5.373,12-12v-5C41.239,25,39,27.239,39,30z" opacity=".15"></path><path fill="#fff" d="M25,18c0-3.86,3.14-7,7-7c2.402,0,4.405-1.695,4.886-3.953C35.393,6.379,33.742,6,32,6 c-6.627,0-12,5.373-12,12v5C22.761,23,25,20.761,25,18z" opacity=".3"></path></g><path fill="none" stroke="#fff" stroke-linecap="round" stroke-miterlimit="10" stroke-width="3" d="M24.63,14.889	c0.405-0.957,0.992-1.819,1.716-2.543s1.586-1.311,2.543-1.716"></path> </svg> <div data-testid="stMarkdownContainer" class="css-x78sv8 eqr7zpz4"></div></button></div></div>',
    #     unsafe_allow_html=True,
    # )

    if start_recognition:= st.button("Start to TrelloTalk Bot"):
        start_recognition = True
        recognize_speech(audio_model_path="C:/new_rasa_trial/whisper_models/tiny.en.pt", start_recognition=start_recognition)
    else:
        start_recognition = False
        recognize_speech(audio_model_path="C:/new_rasa_trial/whisper_models/tiny.en.pt", start_recognition=start_recognition)
        sys.exit()
