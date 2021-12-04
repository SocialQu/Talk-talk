import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

learn_vocabulary = openai.Completion.create(
    engine="curie",
    prompt="The following is a list of words in Spanish for English students to learn\n\nadjectives: deslumbrante (dazzling), nuevo (new), bien (well), simpático (sympathetic), diferente (different), intenso (intense), feliz (happy), imposible (impossible), atractivo (attractive), pobre (poor).\nwork: profesional (professional), cuidar (to take care), incapacitado (incapacitated), pago (payment), conocimiento (knowledge), reclutar (recruit), estudiar (study), empresa (company), vacaciones (vacation), cambio (change), colaborar (collaborate), jefe (boss), carpintero (carpenter), proyecto (project).\nagile:",
    temperature=0.5,
    max_tokens=133,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=["\n"]
)
