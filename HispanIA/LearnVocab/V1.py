import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  engine="curie-instruct-beta",
  prompt="Teach me 10 basic vocabulary words related to business:",
  temperature=0.7,
  max_tokens=75,
  top_p=1,
  frequency_penalty=0.5,
  presence_penalty=0.5,
  stop=["."]
)
