## Imersão Gemini - Alura+Google
# Função principal do projeto projeto de detecção de incendios em imagem
# Autor: Leonardo Brandão Borges de Freitas (contato.leonardobbf@gmail.com)
# Data: 10 Maio 2024
#
# Resumo: Detector de incêndio em imagens, utilizando da IA generativa do Google, Gemini.

from json import loads
from datetime import datetime

import google.generativeai as genai
from gemini_handler import chat_config
from capture_handler import capture_handler, print_img_text

# Solicita a APIKEY do google
GOOGLE_API_KEY = input("Insira a GOOGLE API KEY: ")

# Configura o modelo Gemini, bem como
# inicializa um chat treinado om um histórico para ser um
# classificador de imagens em busca de incêndio
chat = chat_config(GOOGLE_API_KEY)

# Coleta a opção do usuário e define o URL até a câmera de onde a imagem será retirada
print("Escolha qual camera deseja avaliar:")
print("\t 1 - Brasilia - Esplanada - https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-esplanada")
print("\t 2 - Brasilia - Estádio - https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-mane-garrincha")
print("\t 3 - Brasilia - Parque - https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-parque-da-cidade")
escolha = input()

if escolha == "1":
    source_path = "https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-esplanada"
elif escolha == "2":
    source_path = "https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-mane-garrincha"
elif escolha == "3":
    source_path = "https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-parque-da-cidade"

# Captura uma imagem do stream da camera escolhida
# salvando-a como um arquivo .jpg no disco local
img_file, img_frame = capture_handler(source_path=source_path)

# Envia a imagem pra análise
chat.send_message(genai.upload_file("./frame.jpg"))

# Define o resultado em texto, inserindo a data atual
model_ret = loads(chat.last.text)
dt = datetime.today()
text = f"{dt} - {str(model_ret['result']).upper()}"

# Apresenta a imagem na tela junto com o resultado em texto
print_img_text(frame=img_frame, text=text)








