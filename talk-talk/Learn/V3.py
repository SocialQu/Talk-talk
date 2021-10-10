import os
import openai
import json 

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  engine="davinci-instruct-beta",
  prompt="Teach me 10 words realted to business in Spanish:",
  temperature=0.7,
  max_tokens=75,
  top_p=1,
  frequency_penalty=0.5,
  presence_penalty=0.5,
  stop=["."]
)

print("response", response)

response = dict(response)
print("response", response)


choices = response["choices"][0]
print('choices', choices)

text = choices["text"]
print(text, 'text')

words = text.replace("\n", "")
print("words", words)

words = words.split(",")
print("words", words)
