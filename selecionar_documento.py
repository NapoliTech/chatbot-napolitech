from groq import Groq
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))
modelo ="meta-llama/llama-4-scout-17b-16e-instruct"

politicas_bonari = carrega('dados/políticas_bonari.txt')
dados_bonari = carrega('dados/dados_bonari.txt')
produtos_bonari = carrega('dados/produtos_bonari.txt')

def selecionar_documento(resposta_openai):
    if "políticas" in resposta_openai:
        return dados_bonari + "\n" + politicas_bonari
    elif "produtos" in resposta_openai:
        return dados_bonari + "\n" + produtos_bonari
    else:
        return dados_bonari 

def selecionar_contexto(mensagem_usuario):
    prompt_sistema = f"""
    A empresa bonari possui três documentos principais que detalham diferentes aspectos do negócio:

    #Documento 1 "\n {dados_bonari} "\n"
    #Documento 2 "\n" {politicas_bonari} "\n"
    #Documento 3 "\n" {produtos_bonari} "\n"

    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne dados se for o Documento 1, políticas se for o Documento 2 e produtos se for o Documento 3. 

    """
    
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content" : mensagem_usuario
            }
        ],
        temperature=1,
    )

    contexto = resposta.choices[0].message.content.lower()

    return contexto