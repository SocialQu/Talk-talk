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
    print('global words:', globals()['words'])

    if len(globals()['words']) == 0:

        response = openai.Completion.create(
            engine="davinci-instruct-beta",
            prompt="Teach me 10 words realted to" + word + "in Spanish:",
            temperature=0.7,
            max_tokens=75,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stop=["."]
        )
        # print("response", response)

        response = dict(response)
        # print("response", response)

        choices = response["choices"][0]
        # print("choices", choices)

        text = choices["text"]
        # print("text", text)

        words = text.replace("\n", "").replace(":", ",").replace('-','')
        # print("words", words)

        words = words.split(",")

        globals()['words'] = words
        print('AI words:', words)

    data = {'text': globals()['words'][0], "thread_ts": id}
    requests.post(url, json = data)

    globals()['words'] = globals()['words'][1:]
    print('Final', words)

    return words


@app.post("/slack")
async def create_item(request: Request):
    body = await request.json()
    event = body["event"]

    text = event["text"]
    id = event["ts"]
    user = event.get("user")

    if '<@U02E7R8BWAD>' in text:
        text = text.replace('<@U02E7R8BWAD>', '')
        Thread(target=learn, args=(text, id)).start()

    elif user:
        print(event, 'event')
        thread_ts = event.get("thread_ts")

        if thread_ts:
            data = {'text': 'Hello World', "thread_ts": id}
            requests.post(url, json = data)

    return
