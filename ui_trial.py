import streamlit as st


# @st.cache_resource
# def load_audio_model(audio_model_path):
#     return whisper.load_model(audio_model_path)

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
    st.write("Model loaded.")
    st.write("Please speak now...")
    transcription = "Hello"
    col1, col2 = st.columns(2)
    with col1:
        # Add empty space using markdown
        st.markdown("<br/>", unsafe_allow_html=True)
    with col2:
        # Add empty space using markdown using <p> tag
        st.markdown(
            body=f'<div><span><textarea style="text-align: right; width:100%; height: 50px; font-weight: bold; font-size: 16px; color: #ffffff; background-color: #2281e7; border: 3px solid #0e1117; border-radius: 10px; padding: 10px; resize: none;" readonly rows="5" cols="30" wrap="off">{transcription}   :👤</textarea></span></div>',
            unsafe_allow_html=True,
        )
        st.markdown("<p></p>", unsafe_allow_html=True)

    bot_response = "Hello. I am bot powered by Rasa. How can I help you?"
    with col2:
        # Add empty space using markdown
        st.markdown("<br/>", unsafe_allow_html=True)
    with col1:
        # Add empty space using markdown
        st.markdown("<br/>", unsafe_allow_html=True)
        # st.write(":robot_face: Bot said: ", bot_response)
        st.markdown(
            body=f'<div><span><textarea style="text-align: left; width: 100%; font-size: 16px; font-weight: bold; background-color: #ffffff; border: 3px solid rgb(14, 17, 23); border-radius: 10px; padding: 10px; resize: none;" readonly>🤖:   {bot_response}</textarea></span></div>',
            unsafe_allow_html=True,
        )
