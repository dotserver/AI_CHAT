import streamlit as st
import cohere

# Function to initialize the Cohere client
def initialize_cohere_client():
    api_key = st.secrets["COHERE_API_KEY"]
    if not api_key:
        raise ValueError("Cohere API key not found in secrets.")
    co = cohere.Client(api_key)
    return co

def main():
    st.title("AI Chatbot")

    # Initialize Cohere client
    co = initialize_cohere_client()

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input field for the query within a form
    with st.form(key='query_form'):
        user_query = st.text_input("Enter your query:", "What is the latest news about AI?")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_query:
        try:
            with st.spinner("Fetching response..."):
                response = co.chat(
                    message=user_query,
                    model='command-r-plus',
                    temperature=0.3,
                    chat_history=st.session_state.chat_history,
                    prompt_truncation='AUTO',
                    connectors=[{"id": "web-search"}]
                )
                # Log the response to understand its structure
                st.write("Response from Cohere API:", response)

                # Assuming the response object has the expected structure
                bot_response = response.generations[0].text
                st.session_state.chat_history.append({"user": user_query, "bot": bot_response})
                user_query = ""
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write("Full response object:", response)

    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")

if __name__ == "__main__":
    main()
