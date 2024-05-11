###### GEMINI HANDLER ######

import google.generativeai as genai

def chat_config(google_api_key: str):

    # Configurando a API KEY de comunicação com o Gemini
    genai.configure(api_key=google_api_key)

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
    response = model.generate_content("De forma breve, recepcione o usuário do programa que utiliza da IA generativa do Google, Gemini, para detectar incêndio em imagens. Não de instruções de uso.")
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

    return chat