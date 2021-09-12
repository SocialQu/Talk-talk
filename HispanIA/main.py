# python uvicorn main:app --reload
# python -m uvicorn main:app --reload

from fastapi import FastAPI, Request
from threading import Thread
from typing import Optional
import requests
import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


words = []
url = 'https://hooks.slack.com/services/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'


def parseText(response):
    response = dict(response)
    # print("response", response)

    choices = response["choices"][0]
    # print("choices", choices)

    text = choices["text"]
    return text


def learn(word, id):
    prompt="Student: Please teach me a new word related to " + word + " in Spanish.\n\nTeacher: Sure! A new word you can learn is",
    print("Learn prompt:", prompt)

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.8,
        max_tokens=44,
        top_p=0.5,
        frequency_penalty=0.5,
        presence_penalty=0.7,
        stop=[".", "and", "which", "-"]
    )

    text = parseText(response)
    print("Learn response:", text)

    data = {'text': text, "thread_ts": id}
    requests.post(url, json = data)

    globals()['lastWord'] = text
    return words


def evaluate(word, id):
    lastWord = globals()['lastWord']
    
    prompt = 'Spanish student: ' + lastWord + ' in Spanish translates to ' + word + '?\n\nSpanish teacher:'
    print("Evaluate prompt:", prompt)

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=44,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]  
    )

    text = parseText(response)

    data = {'text':text, "thread_ts": id}
    requests.post(url, json = data)

    learn(globals()['word'], id)
    return




@app.post("/slack")
async def slack(request: Request):
    body = await request.json()
    event = body["event"]

    text = event["text"]
    id = event["ts"]
    message = event["type"]
    user = event.get("user")


    if message == 'app_mention':
        text = text.replace('<@U02E7R8BWAD>', '')
        globals()['word'] = text
        Thread(target=learn, args=(text, id)).start()

    elif user:
        thread_ts = event.get("thread_ts")

        if thread_ts:
            block = event.get('blocks')[0]
            element = block.get('elements')[0]
            text = element.get('elements')[0].get('text')
            Thread(target=evaluate, args=(text, id)).start()

    return
