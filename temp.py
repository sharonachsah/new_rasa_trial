import whisper

model = whisper.load_model("base")
result = model.transcribe("C:/Users/Achsah/Downloads/new rasa trial/mayur_new_new.wav")
print(result["text"])
