import streamlit as st
import requests
import sys
import os

# Add the current directory to the path to allow imports
sys.path.append(os.path.dirname(__file__))

from app.agent import Agent


st.title("Evolusis – AI Reasoning Agent")

# Initialize agent in session state for persistence across reruns
if 'agent' not in st.session_state:
    st.session_state.agent = Agent()

agent = st.session_state.agent

# Input for user query
query = st.text_input("Enter your query:", placeholder="Ask me anything...")

# Button to submit query
if st.button("Submit"):
    if query.strip():
        # Function to handle the API response
        def process_query():
            try:
                response = requests.post("http://127.0.0.1:8000/ask", json={"query": query})
                response.raise_for_status()
                data = response.json()
                return data["reasoning"], data["answer"], data["used_tools"]
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")
                return None, None, None

        # Run the function
        with st.spinner("Processing your query..."):
            reasoning, answer, tools = process_query()

        if reasoning is not None:
            # Display results
            st.subheader("Reasoning:")
            st.write(reasoning)

            st.subheader("Answer:")
            st.write(answer)

            if tools:
                st.subheader("Tools Used:")
                st.write(", ".join(tools))
    else:
        st.warning("Please enter a query.")

# Optional: Display recent memory for context
if st.checkbox("Show recent conversation history"):
    mem_text = agent.memory.as_text()
    st.subheader("Recent Memory:")
    st.write(mem_text)
