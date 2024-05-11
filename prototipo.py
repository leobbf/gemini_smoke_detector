##
# Protótipo do projeto para imersão Gemini - Alura+Google
# Autor: Leonardo Brandão Borges de Freitas (contato.leonardobbf@gmail.com)
# Data: 10 Maio 2024
#
# Resumo: Detector de incêndio em imagens, utilizando da IA generativa do Google, Gemini.

import os
from json import loads
from dotenv import load_dotenv
from datetime import datetime

from cv2 import VideoCapture, putText, imshow, waitKey, FONT_HERSHEY_SIMPLEX, imwrite, destroyAllWindows, imread
from clima_ao_vivo_handler import clima_ao_vivo_path

import google.generativeai as genai

# Carrega as variáveis de ambiente
load_dotenv()

###### MODELO GEMINI ######

# Configurando a API KEY de comunicação com o Gemini
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Definindo as configurações para o modelo
model_name = "gemini-1.5-pro-latest"

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# Instanciando o modelo
model = genai.GenerativeModel(model_name=model_name,
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Testando o modelo para validar se as configurações foram efetivadas
response = model.generate_content("De forma breve, recepcione o usuário do programa que utiliza da IA generativa do Google, Gemini, para detectar incêndio em imagens")
print(f'\n\t{response.text}\t\n')

# Iniciando o modo de chat do Gemini, com histório para instrui-lo a ser um classificador de incêndios em imagens
# Os arquivos ./content/ex_1.jpeg e ./content/ex_2.jpeg são exemplos de imagens com incêndios.
# Já os arquivos ./content/ex_3.jpeg e ./content/ex_4.jpeg são exemplos de imagens sem incêndio.
chat = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Aja como um classificador de imagens para identificar se há ou não fumaça em uma imagem de entrada. Como resposta de saída, indique o resultado do processamento da imagem dentre: \"incendio identificado\", para imagens que tenham fumaça ou \"nenhum incendio identificado\", para as imagens sem fumaça. Formate a resposta de saída em JSON. Seguem exemplos.\n"]
  },
  {
    "role": "user",
    "parts": [genai.upload_file("./content/ex_1.jpeg")]
  },
  {
    "role": "user",
    "parts": ["{\"result\":\"incendio identificado\"}"]
  },
  {
    "role": "user",
    "parts": [genai.upload_file("./content/ex_2.jpeg")]
  },
  {
    "role": "user",
    "parts": ["{\"result\":\"incendio identificado\"}"]
  },
  {
    "role": "user",
    "parts": [genai.upload_file("./content/ex_3.jpeg")]
  },
  {
    "role": "user",
    "parts": ["{\"result\":\"nenhum incendio identificado\"}"]
  },
  {
    "role": "user",
    "parts": [genai.upload_file("./content/ex_4.jpeg")]
  },
  {
    "role": "user",
    "parts": ["{\"result\":\"nenhum incendio identificado\"}"]
  },
])


'''
###### TESTE #########
chat.send_message(genai.upload_file("./content/test_1.jpeg"))

model_ret = loads(chat.last.text)
dt = datetime.today()
text = f"{dt} - {str(model_ret['result']).upper()}"

frame = imread("./content/test_1.jpeg")
# Escreve o texto no frame
putText(frame, text, (10, 30), FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Mostra o frame capturado
imshow("Frame", frame)

waitKey(0) # Aguarda uma tecla ser pressionada
destroyAllWindows() # Fecha a janela
'''


####### CAPTURA DE IMAGENS ##########
# Definindo o link até o stream da camera de onde as imagens serão coletadas
source_path = "https://www.climaaovivo.com.br/df/brasilia/combo-livre-brasil-21-esplanada"

# Resolve o caminho até o stream da camera
stream = clima_ao_vivo_path(source_path=source_path)

# Abre um capturador de video openCV apontado para o stream da camera
video_capture = VideoCapture(stream)

# captura um frame do stream da camera
ret, frame = video_capture.read()

if ret:

    # salva a imagem em disco
    imwrite("frame.jpg", frame)

    # Envia a imagem pra análise do modelo
    chat.send_message(genai.upload_file("./frame.jpg"))

    # Define o resultado em texto, inserindo a data atual
    model_ret = loads(chat.last.text)
    dt = datetime.today()
    text = f"{dt} - {str(model_ret['result']).upper()}"

    # Escreve o texto no frame
    putText(frame, text, (10, 30), FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostra o frame capturado
    imshow("Frame", frame)

    waitKey(0) # Aguarda uma tecla ser pressionada
    destroyAllWindows() # Fecha a janela

video_capture.release()
        
