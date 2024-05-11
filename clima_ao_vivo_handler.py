import re
import urllib.request
from json import loads, dumps

####### STREAM DO CLIMA AO VIVO (https://www.climaaovivo.com.br/cidades) ##########

def clima_ao_vivo_path(source_path: str):

    # Isola as informações de local e estado onde a camera esta instalada, proveninete do caminho de captura
    local = source_path.split('/')[-1]
    estado = source_path.split('/')[3]

    # Compila o URL para conseguir o token de conexão com o streaming da câmera
    TOKEN_URL = 'https://cmsv2.climaaovivo.com.br/api/cameras/' + '{}?dessigla={}'.format(local, estado)
    #print(TOKEN_URL)

    # Faz a requisição HTTP GET a partir do URL compilado anteriormente
    with urllib.request.urlopen(TOKEN_URL) as response:
                html = response.read()

    # Decodifica o html em utf-8 e organiza as informações em JSON 
    json_html = loads(html.decode('utf-8'))
    #print(dumps(json_html, indent=4))
    
    # Isola o descodigo da camera (cidade#.estado), provenientes do JSON
    descodigo = json_html['data'].get('descodigo')

    # Isola o token de conexão, proveniente do html
    token = re.sub(r".*token=(.*)&remot.*", r'\1', str(html))

    # Monta o link até o stream da câmera a partir do descodigo e do token
    STREAM_URL = f"https://streaming3.climaaovivo.com.br/{descodigo}/index.m3u8?token={token}"
    #print(STREAM_URL)

    # Retorna o path verdadeiro com o token 
    return STREAM_URL