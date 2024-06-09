import cohere
import json
import pandas as pd
from datetime import datetime
import streamlit as st

# Function to load API key from config file
def load_api_key_from_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config.get('COHERE_API_KEY')

# Function to initialize the Cohere client
def initialize_cohere_client():
    api_key = load_api_key_from_config()
    if not api_key:
        raise ValueError("Cohere API key not found in config file.")
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
    
    results = []
    for event in stream:
        if event.event_type == "text-generation":
            results.append(event.text)
            print(event.text, end='')
    return results

# Function to save results to a JSON file
def save_results_to_file(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

# Function to preprocess and analyze results
def preprocess_and_analyze_results(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    # Example: Convert data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['text'])
    df['timestamp'] = datetime.now()
    
    # Display the DataFrame
    st.write(df)

    # Save DataFrame to a CSV file
    df.to_csv('ai_chat.csv', index=False)
    st.write("Results saved to ai_chat.csv")

# Streamlit app
def main():
    st.title("AI Chatbot")
    
    # Initialize Cohere client
    co = initialize_cohere_client()

    # Input field for the query
    query = st.text_input("Enter your query:", "What is the latest news about AI?")
    
    # Button to fetch results
    if st.button("Fetch Result"):
        with st.spinner("Fetching result..."):
            results = fetch_real_time_data(co, query)
            filename = f'ai_chat_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
            save_results_to_file(results, filename)
            preprocess_and_analyze_results(filename)

if __name__ == "__main__":
    main()
