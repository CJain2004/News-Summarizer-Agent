import os
import streamlit as st
from groq import Groq

class Summarizer:
    def __init__(self):
        api_key = None

        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except FileNotFoundError:
            api_key = os.environ.get("GROQ_API_KEY")

        self.client = Groq(api_key=api_key) if api_key else None

    def summarize(self, text: str):
        if not text or not self.client:
            return None

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a financial news assistant. "
                            "Summarize the following news article in 30-40 words. "
                            "Focus on the main financial impact or event."
                        )
                    },
                    {
                        "role": "user",
                        "content": text[:4000],
                    }
                ],
                model="llama-3.1-8b-instant",
                timeout=30,
            )
            return chat_completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"Groq Error: {e}")
            return None
