import os
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=api_key)
def get_ai_analysis(prompt):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text