import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nIs translation correct:"
restart_sequence = "\n\nEnglish: "

response = openai.Completion.create(
  engine="davinci-instruct-beta",
  prompt="Evaluate kindly with yes or no, if \"negocio\" in Spanish translates to \"business\":",
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)
