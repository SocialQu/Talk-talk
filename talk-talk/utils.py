def parseText(response):
    response = dict(response)
    # print("response", response)

    choices = response["choices"][0]
    # print("choices", choices)

    text = choices["text"]
    return text
