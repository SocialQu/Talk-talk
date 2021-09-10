# python uvicorn main:app --reload
# python -m uvicorn main:app --reload

from fastapi import FastAPI, Request
from threading import Thread
from typing import Optional
import requests
import openai
import os
import json


openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


words = []
url = 'https://hooks.slack.com/services/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'

def learn(word, id):
    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt="Teach me 10 words realted to" + word + "in Spanish:\n\n1.",
        temperature=0.7,
        max_tokens=25,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        stop=["2"]
    )
    # print("response", response)

    response = dict(response)
    # print("response", response)

    choices = response["choices"][0]
    # print("choices", choices)

    text = choices["text"]
    print("text", text)

    words = text.replace(":", "\n").replace('-','\n')
    # print("words", words)

    words = words.split("\n")

    print('AI words:', words)

    data = {'text': words[0], "thread_ts": id}
    requests.post(url, json = data)

    return words


@app.post("/slack")
async def create_item(request: Request):
    body = await request.json()
    event = body["event"]

    text = event["text"]
    id = event["ts"]
    message = event["type"]
    user = event.get("user")


    if message == 'app_mention':
        text = text.replace('<@U02E7R8BWAD>', '')
        Thread(target=learn, args=(text, id)).start()

    elif user:
        thread_ts = event.get("thread_ts")

        if thread_ts:
            data = {'text': 'Hello World', "thread_ts": id}
            requests.post(url, json = data)

    return
