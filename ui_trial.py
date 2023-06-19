import streamlit as st

def main():
    st.title("Chatbot Interface")

    conversation = []
    user_input = st.text_input("User")
    bot_response = st.text_input("Bot")

    if st.button("Send"):
        if user_input:
            conversation.append(("User", user_input))
            user_input = ""
        if bot_response:
            conversation.append(("Bot", bot_response))
            bot_response = ""

    # Display conversation history
    st.subheader("Conversation History")
    for sender, message in conversation:
        if sender == "User":
            st.text_area("User", value=message, key=message)
        elif sender == "Bot":
            st.text_area("Bot", value=message, key=message)

if __name__ == "__main__":
    main()
