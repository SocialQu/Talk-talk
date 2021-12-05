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
    globals()[id] = { 'word':word, 'vocabulary':vocabulary, 'index':0, 'score':0 }

    data = {'text':vocabulary[0].word, 'thread_ts': id}
    requests.post(slack_url, json = data)

    return


def evaluate(word, id, thread_id):
    thread = globals()[thread_id]
    vocabulary = thread.get('vocabulary')
    index = thread.get('index')

    answer = vocabulary[index].get('answer')
    print('answer', answer)

    answer = answer[1].replace(')', '')
    print('answer', answer)
    
    answer_word = answer.lower().replace(' ', '').replace('.', '')
    word = word.lower().replace(' ', '').replace('.', '')
    print(answer_word, word)

    response = ''
    if answer_word != word:
        data = {'text':'No, the answer is "' + answer + '"', 'thread_ts': id}
        requests.post(slack_url, json = data)

    else:
        good_responses = [ 'Congratulations!', 'Yes, that’s right.', 'Correct!', 'Good Job!', 'Well Done!' ]
        response = good_responses[randint(0, len(good_responses) - 1)] + '\n'


    newIndex = globals()[thread_id]['index'] + 1
    globals()[thread_id]['index'] = newIndex

    nextWord = vocabulary[newIndex].split('(')[0]

    data = {'text':response + nextWord, 'thread_ts':id}
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
            Thread(target=evaluate, args=(text, id, thread_ts)).start()

    return
