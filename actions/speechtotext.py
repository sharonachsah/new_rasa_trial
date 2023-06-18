""" This script demonstrates how to use whisper to transcribe audio from a microphone in real time."""

import argparse
import io
import os
from datetime import datetime, timedelta, timezone
from queue import Queue
from sys import platform
from tempfile import NamedTemporaryFile
from time import sleep

import speech_recognition as sr
import whisper

latest_transcription = ""


def recognize_speech(audio_model: str, bool_val: bool = False):
    """Transcribe audio from microphone in real time using whisper."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="tiny",
        help="Model to use",
        choices=["tiny", "base", "small", "medium", "large"],
    )
    parser.add_argument(
        "--non_english", action="store_true", help="Don't use the english model."
    )
    parser.add_argument(
        "--energy_threshold",
        default=300,
        help="Energy level for mic to detect.",
        type=int,
    )
    parser.add_argument(
        "--record_timeout",
        default=30,
        help="How real time the recording is in seconds.",
        type=float,
    )
    parser.add_argument(
        "--phrase_timeout",
        default=4,
        help="How much empty space between recordings before we "
        "consider it a new line in the transcription.",
        type=float,
    )
    if "linux" in platform:
        parser.add_argument(
            "--default_microphone",
            default="pulse",
            help="Default microphone name for SpeechRecognition. "
            "Run this with 'list' to view available Microphones.",
            type=str,
        )
    args = parser.parse_args()

    phrase_time = None

    last_sample = bytes()

    data_queue = Queue()

    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold

    recorder.dynamic_energy_threshold = False

    source = sr.Microphone(sample_rate=16000, device_index=0)

    audio_model = whisper.load_model(audio_model)

    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    temp_file = NamedTemporaryFile().name
    transcription = [""]

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """

        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(
        source, record_callback, phrase_time_limit=record_timeout
    )

    print("Model loaded.\n")
    print("Please speak now...")

    while bool_val:
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
                    transcription.append(text)

                else:
                    transcription[-1] = text

                os.system("cls")
                for line in transcription:
                    print(line)

                print("", end="", flush=True)

                sleep(0.1)
        except KeyboardInterrupt:
            break
    print("\n\nTranscription:")
    for line in transcription:
        print(line)
        latest_transcription = line
        print("Latest transcription: ", latest_transcription)
    return transcription[-1]


if __name__ == "__main__":
    recognize_speech(
        audio_model="X:/new_rasa_trial/whisper_models/tiny.en.pt", bool_val=True
    )
