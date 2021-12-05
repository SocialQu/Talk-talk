from ..utils import parseText
from ..config import engine
import openai


def talk(conversation):
    completion = openai.Completion.create(
        engine=engine,
        prompt="La siguiente es una conversación entre un mexicano y un estudiante de Español. El mexicano es educado, creativo, inteligente y muy amigable.\n\nEstudiante: " + conversation + "\nMexicano:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"]
    )

    text = parseText(completion)
    print('Text:', text)

    return text
