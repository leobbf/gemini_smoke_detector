####### CAPTURA DE IMAGENS OPENCV ##########

from clima_ao_vivo_handler import clima_ao_vivo_path
from cv2 import VideoCapture, putText, imshow, waitKey, FONT_HERSHEY_SIMPLEX, imwrite, destroyAllWindows

def capture_handler(source_path) -> tuple:

    # Resolve o caminho até o stream da camera
    stream = clima_ao_vivo_path(source_path=source_path)

    # Abre um capturador de video openCV apontado para o stream da camera
    video_capture = VideoCapture(stream)

    # captura um frame do stream da camera
    ret, frame = video_capture.read()

    if ret:

        # salva a imagem em disco
        imwrite("frame.jpg", frame)
        ret = ("frame.jpg", frame)

    else:
        print('ERRO AO CAPTURAR O FRAME DO STREAMING DA CAMERA')

    video_capture.release()
    return ret

def print_img_text(frame, text):

    # Escreve o texto no frame
    putText(frame, text, (10, 30), FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostra o frame capturado
    imshow("Frame", frame)

    waitKey(0) # Aguarda uma tecla ser pressionada
    destroyAllWindows() # Fecha a janela