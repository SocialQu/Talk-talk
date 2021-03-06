from .utils import parseText, engine
import openai


def learn_vocabulary(word):
    prompt = 'The following is a list of words in Spanish for English students to learn\n\nadjectives: deslumbrante (dazzling), nuevo (new), bien (well), simpático (sympathetic), diferente (different), intenso (intense), feliz (happy), imposible (impossible), atractivo (attractive), pobre (poor).\nwork: profesional (professional), cuidar (to take care), incapacitado (incapacitated), pago (payment), conocimiento (knowledge), reclutar (recruit), estudiar (study), empresa (company), vacaciones (vacation), cambio (change), colaborar (collaborate), jefe (boss), carpintero (carpenter), proyecto (project).\n' + word + ':'

    completion = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=0.5,
        max_tokens=133,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        stop=['\n']
    )

    text = parseText(completion)
    print('Text:', text)

    words = text.split(',')
    print('Words:', words)
    
    vocabulary = []
    keys = []

    for word in words:
        if not '(' in word: continue        
        if not ')': continue

        question = word.split('(')[0]
        translation = word.split('(')[1]
        answer = translation.lower().replace(')', '').replace('.', '')

        if question in keys: continue

        vocabulary.append({ 'question':question, 'answer':answer })
        keys.append(question)

    print('Vocabulary:', vocabulary)
    return vocabulary
