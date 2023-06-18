import tkinter as tk
import speech_recognition as sr
import rasa
from gtts import gTTS
from playsound import playsound


class VoiceBotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("VoiceBot")
        self.window.geometry("400x400")

        self.input_text = tk.StringVar()
        self.output_text = tk.StringVar()

        self.input_label = tk.Label(self.window, text="User Input:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self.window, textvariable=self.input_text)
        self.input_entry.pack()

        self.output_label = tk.Label(self.window, text="Bot Output:")
        self.output_label.pack()

        self.output_entry = tk.Entry(self.window, textvariable=self.output_text)
        self.output_entry.pack()

        self.mic_button = tk.Button(self.window, text="Speak", command=self.voice_input)
        self.mic_button.pack()

    def voice_input(self):
        # Initialize speech recognition engine
        r = sr.Recognizer()

        # Use microphone as audio source
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source)

        # Convert speech to text
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)

            # Set input text in GUI
            self.input_text.set(text)

            # Pass text input to Rasa chatbot
            response = rasa.core.run(text)

            # Set output text in GUI
            self.output_text.set(response)

            # Convert chatbot response to audio clip
            tts = gTTS(response)
            tts.save("response.mp3")

            # Play audio clip for user
            playsound("response.mp3")

        except sr.UnknownValueError:
            print("Sorry, I could not understand your voice input.")
            self.input_text.set("")
            self.output_text.set("Sorry, I could not understand your voice input.")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )
            self.input_text.set("")
            self.output_text.set(
                "Could not request results from Google Speech Recognition service."
            )

    def run(self):
        self.window.mainloop()


if __name__ == "_main_":
    VoiceBotGUI().run()
