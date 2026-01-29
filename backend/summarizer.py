import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv(override=True)

class Summarizer:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                print("Groq Client Initialized.")
            except Exception as e:
                print(f"Failed to init Groq: {e}")

    def summarize(self, text: str) -> str:
        if not text:
            return "No content available to summarize."

        # REAL AI SUMMARY
        if self.client:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a financial news assistant. Summarize the following news article in 30-40 words. Focus on the main financial impact or event."
                        },
                        {
                            "role": "user",
                            "content": text[:4000], 
                        }
                    ],
                    model="llama-3.1-8b-instant",
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                print(f"Groq Error: {e}")
                # Fallback to simple if error

        # FALLBACK / MOCK SUMMARY (Improved)
        # Take the first 300 characters but try to end on a sentence
        sentences = text.split('. ')
        summary = ". ".join(sentences[:3]) + "."
        words = summary.split()
        if len(words) > 40:
            summary = " ".join(words[:40]) + "..."
            
        return summary
