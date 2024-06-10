import cohere
import streamlit as st
import os



# Function to initialize the Cohere client
def initialize_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Cohere API key not found in environment variables.")
    co = cohere.Client(api_key)
    return co

# Function to fetch real-time data using Cohere chat stream
def fetch_real_time_data(co, query):
    stream = co.chat_stream(
        model='command-r-plus',
        message=query,
        temperature=0.3,
        chat_history=[],
        prompt_truncation='AUTO',
        connectors=[{"id":"web-search"}]
    )
    
    response = ""
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text
    return response

# Streamlit app
def main():
    st.title("AI News Chatbot")
    
    # Initialize Cohere client
    co = initialize_cohere_client()

    # Input field for the query
    query = st.text_input("Enter your query:", "What is the latest news about AI?")
    
    # Chat history to maintain the state of the conversation
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Button to fetch results
    if st.button("Send"):
        if query:
            with st.spinner("Fetching news..."):
                response = fetch_real_time_data(co, query)
                # Add user query and response to chat history
                st.session_state.chat_history.append({"user": query, "bot": response})

    # Display chat history
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.write(f"**You:** {chat['user']}")
            st.write(f"**Bot:** {chat['bot']}")

if __name__ == "__main__":
    main()
