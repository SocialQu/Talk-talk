# python -m uvicorn main:app --reload

from queries.learnVocabulary import learn_vocabulary
from config import slack_url, openApi
from fastapi import FastAPI, Request
from threading import Thread
from utils import parseText
from random import randint
import requests
import openai


openai.api_key = openApi
app = FastAPI()


def learn(word, id):
    vocabulary = learn_vocabulary(word)
    globals()[id] = { 'word':word, 'vocabulary':vocabulary, 'index':0, 'learning':True, 'counter':0 }

    if len(vocabulary) > 0: text = vocabulary[0].question
    else: text = 'Please choose a different word.'

    data = {'text':text, 'thread_ts': id}
    requests.post(slack_url, json = data)

    return



def reply(response, id, thread_id):
    thread = globals()[thread_id]
    if thread.get('learning'): evaluate(response, id, thread_id)
    else: chat(response, id , thread_id)


def evaluate(response, id, thread_id):
    text = ''
    thread = globals()[thread_id]
    vocabulary = thread.get('vocabulary')
    index = thread.get('index')

    answer = vocabulary[index].get('answer')
    print('answer', answer)

    # Evaluate translation
    if response.lower() == answer:
        good_responses = [ 'Congratulations!', 'Yes, that’s right.', 'Correct!', 'Good Job!', 'Well Done!' ]
        text = good_responses[randint(0, len(good_responses) - 1)] + '\n'

    else:
        data = {'text':'No, the answer is "' + answer + '"', 'thread_ts': id}
        requests.post(slack_url, json=data)

    # Next prompt
    if len(vocabulary) == index + 1:
        globals()[thread_id]['learning'] = False
        prompt = 'Now, please use one of the words you learned in a Spanish sentence:'
        data = {'text':text + prompt, 'thread_ts':id}
        requests.post(slack_url, json = data)

    else:
        newIndex = index + 1
        globals()[thread_id]['index'] = newIndex
        nextWord = vocabulary[newIndex].get('question')
        data = {'text':text + nextWord, 'thread_ts':id}
        requests.post(slack_url, json = data)

    return


def correct(): return ''
def talk(): return ''

def chat(response, id, thread_id): 
    correction = correct(response)
    if correction != response:
        data = {'text':'**' + correction + '**' , 'thread_ts':id}
        requests.post(slack_url, json = data)

    thread = globals()[thread_id]
    counter = thread.get('counter')

    if counter < 5: 
        globals()[thread_id]['counter'] = counter + 1
        text = talk()

    else: text = "Great! You've reached 5 interactions, try learning new vocabulary."

    data = {'text': text , 'thread_ts':id}
    requests.post(slack_url, json = data)

    return


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.post('/')
async def slack(request: Request):
    body = await request.json()

    # return body.get('challenge')

    event = body['event']

    text = event['text']
    id = event['ts']
    message = event['type']
    user = event.get('user')


    # app is mentioned
    if message == 'app_mention':
        text = text.replace('<@U02E7R8BWAD>', '')
        globals()['word'] = text
        Thread(target=learn, args=(text, id)).start()

    # message is from user (filters bot replies).
    elif user:
        thread_ts = event.get('thread_ts')

        # message comes in a thread.
        if thread_ts:
            block = event.get('blocks')[0]
            element = block.get('elements')[0]
            text = element.get('elements')[0].get('text')
            Thread(target=reply, args=(text, id, thread_ts)).start()

    return
