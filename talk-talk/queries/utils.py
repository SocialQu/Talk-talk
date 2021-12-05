def parseText(response):
    response = dict(response)
    choices = response['choices'][0]

    text = choices['text']
    return text
