import cv2
import os
import numpy as np
import pickle
from imutils import paths
from helpers import resize_to_fit
from keras.models import load_model
from quebrar_captcha import tratar_imagens


def quebrar_captcha():
    # importar o modelo que a gente treinou e importar o tradutor
    with open('rotulos_modelo.dat', 'rb') as arquivo_tradutor:
        lb = pickle.load(arquivo_tradutor)

    modelo = load_model('modelo_treinado.hdf5')

    # Usar o modelo pra resolver os captcha
    tratar_imagens("resolver", pasta_destino='resolver')
    # ler tds os arquivos da pasta resolver
    # Para cada arquivo
    # tratar a imagem
    # identificar as letras
    # pegar as letras e dar pra AI
    # juntar as letras em 1 texto só

    arquivos = list(paths.list_images('resolver'))
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)  # ler o arquivo
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        # EM PRETO E BRANCO
        _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)

    # _ é usado para pegar somente a 1° informação (imagem, ) E ESTOU ENCONTRANDO O CONTORNO DE CADA LETRA
        contornos, _ = cv2.findContours(
            nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        regiao_letras = []

    # Filtrar os contornos que são realmente de letras
        for contorno in contornos:
            (x, y, largura, altura) = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            if area > 115:
                regiao_letras.append((x, y, largura, altura))

        regiao_letras = sorted(regiao_letras, key=lambda x: x[0]) #poderia ser x: x[0] tbm
        # desenhar os contornos e separar as letras em arquivos individuais
        imagem_final = cv2.merge([imagem] * 3)
        previsao = []

      
        for retangulo in regiao_letras:
            x, y, largura, altura = retangulo
            imagem_letra = imagem[y:y+altura, x:x+largura]

            # Dar a letra para AI descobrir que letra é essa
            imagem_letra = resize_to_fit(imagem_letra, 20, 20)

            # Tratamento para o Keras funcionar
            imagem_letra = np.expand_dims(imagem_letra, axis=2)
            imagem_letra = np.expand_dims(imagem_letra, axis=0)

            letra_prevista = modelo.predict(imagem_letra)
            letra_prevista = lb.inverse_transform(letra_prevista)[0]
            previsao.append(letra_prevista)

        texto_previsao = "".join(previsao)
        print(texto_previsao)
        #return texto_previsao


if __name__ == '__main__':
    quebrar_captcha()
