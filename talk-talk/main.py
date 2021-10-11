# python -m uvicorn main:app --reload

from fastapi import FastAPI, Request
from config import slack, openApi
from threading import Thread
import requests
import openai
import os


openai.api_key = openApi
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


words = []
url = slack


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

    prompt = 'The following is a list of words in Spanish for English students to learn\n\nadjectives: deslumbrante (dazzling), nuevo (new), bien (well), simpático (sympathetic), diferente (different), intenso (intense), feliz (happy), imposible (impossible), atractivo (attractive), pobre (poor).\nwork: profesional (professional), cuidar (to take care), incapacitado (incapacitated), pago (payment), conocimiento (knowledge), reclutar (recruit), estudiar (study), empresa (company), vacaciones (vacation), cambio (change), colaborar (collaborate), jefe (boss), carpintero (carpenter), proyecto (project).\n' + word + ':'
    print("Evaluate prompt:", prompt)

    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        temperature=0.5,
        max_tokens=133,
        top_p=1,
        frequency_penalty=0, # TODO: Test other values.
        presence_penalty=0,  # TODO: Test other values.
        stop=["\n"]  
    )

    text = parseText(response)

    data = {'text':text, "thread_ts": id}
    requests.post(url, json = data)

    learn(globals()['word'], id)
    return




@app.post('/')
async def slack(request: Request):
    body = await request.json()

    # return body.get('challenge')

    event = body["event"]

    text = event["text"]
    id = event["ts"]
    message = event["type"]
    user = event.get("user")


    # app is mentioned
    if message == 'app_mention':
        text = text.replace('<@U02E7R8BWAD>', '')
        globals()['word'] = text
        Thread(target=learn, args=(text, id)).start()

    # message is from user (filters bot replies).
    elif user:
        thread_ts = event.get("thread_ts")

        # message comes in a thread.
        if thread_ts:
            block = event.get('blocks')[0]
            element = block.get('elements')[0]
            text = element.get('elements')[0].get('text')
            Thread(target=evaluate, args=(text, id)).start()

    return
