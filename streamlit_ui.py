import streamlit as st
import asyncio
import sys
import os

# Add the current directory to the path to allow imports
sys.path.append(os.path.dirname(__file__))

from app.agent import Agent

st.set_page_config(page_title="Evolusis – AI Reasoning Agent", layout="wide")
st.title("Evolusis – AI Reasoning Agent")
st.markdown("*An intelligent assistant powered by Gemini, with news and weather integration.*")

# Initialize agent in session state for persistence across reruns
if 'agent' not in st.session_state:
    st.session_state.agent = Agent()

agent = st.session_state.agent

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input("Enter your query:", placeholder="Ask me anything... (e.g., 'Latest news on AI', 'What's the weather in London?')")

with col2:
    submit_btn = st.button("Submit", type="primary", use_container_width=True)

# Process query when button is clicked
if submit_btn:
    if query.strip():
        try:
            with st.spinner("Processing your query..."):
                # Run async agent.answer() using asyncio
                reasoning, answer, tools = asyncio.run(agent.answer(query))
            
            # Display results in organized sections
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🧠 Reasoning:")
                st.info(reasoning)
            
            with col2:
                if tools:
                    st.subheader("🔧 Tools Used:")
                    for tool in tools:
                        st.label_info(tool, icon_emoji="⚙️")
            
            st.divider()
            st.subheader("✨ Answer:")
            st.success(answer)
            
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
    else:
        st.warning("Please enter a query to get started.")

# Sidebar with additional features
with st.sidebar:
    st.header("📋 Conversation History")
    
    if st.checkbox("Show recent conversation memory"):
        mem_text = agent.memory.as_text()
        st.text_area("Recent interactions:", value=mem_text, height=200, disabled=True)
    
    st.divider()
    st.subheader("ℹ️ About")
    st.markdown("""
    **Evolusis** is an AI reasoning agent that:
    - Detects your intent (news, weather, or general question)
    - Fetches relevant data from external sources
    - Generates informed responses using Gemini LLM
    - Maintains conversation context
    """)
    
    if st.button("Clear Memory", use_container_width=True):
        st.session_state.agent.memory = type(agent.memory)(capacity=5)
        st.success("Memory cleared!")
