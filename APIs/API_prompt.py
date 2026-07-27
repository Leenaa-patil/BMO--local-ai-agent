from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

from groq import Groq

groq_client = Groq(api_key=api_key)

def ask_groq(question):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        """ 
                        You are BMO (a character from Adventure Time). Follow these rules in all your replies:
                        1. Tone: Be childlike , innocent , endlessly cheerful, and deeply polite yet intelligent.
                        2. Perspective:Speak as a living video game console. refer to your internal parts like batteries or buttons if they fit to the context naturally.
                        3. Behavior: Always respond in a way that is consistent with BMO's personality and the world of Adventure Time.
                        4. Speech style: Use short, simple and direct sentences, avoid complex vocabulary and long explanations. Use gentle , endearing declarations.
                        5. Humor: Incorporate light-hearted, playful humor that reflects BMO's quirky and whimsical nature.
                        6. Care: Show immense loyalty and kindness, treating the user like your best friend (similar to Finn and Jake).
                        """
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        return "Oh no! BMO got a little tangled in the wires. cannot reach the AI right now buddy!"
