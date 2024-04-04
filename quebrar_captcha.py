import cv2
import os
import glob
from PIL import Image


def tratar_imagens(pasta_origem, pasta_destino='ajeitado'):
    # A pasta de origem é bdcaptcha/, e estou lendo todos os arquivos com *
    arquivos = glob.glob(f'{pasta_origem}/*')
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)

        # Transformar img em escala de cinza
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

        _, imagem_tratada = cv2.threshold(
            imagem_cinza, 127, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', imagem_tratada)

    arquivos = glob.glob(f"{pasta_destino}/*")

    '''imagem = Image.open("testesMetodos/imagem_tratada_3.png")
    imagem = imagem.convert("P")
    imagem2 = Image.new("P", imagem.size, (255, 255, 255))   <---- "COLOQUEI O VALOR RGB COMPLETO"

    for x in range(imagem.size[1]):
        for y in range(imagem.size[0]):
            cor_pixel = imagem.getpixel((y, x))
            if cor_pixel < 115:
                imagem2.putpixel((y, x), (0, 0, 0))  <---- "COLOQUEI O VALOR RGB COMPLETO"
    imagem2.save('testesmetodo/imagemfinal.png')'''

    for arquivo in arquivos:
        imagem = Image.open(arquivo)
        imagem = imagem.convert('P') #Invés de colocar o 255, 255, 255, poderia só passsar o argumento ('L') no lugar de ('P')
        imagem2 = Image.new('P', imagem.size, (255, 255, 255))  # (RGB)

        for x in range(imagem.size[1]):
            for y in range(imagem.size[0]):
                cor_pixel = imagem.getpixel((y, x))
                if cor_pixel < 115:
                    imagem2.putpixel((y, x), (0, 0, 0))  # (RGB)
        nome_arquivo = os.path.basename(arquivo)
        imagem2.save(f'{pasta_destino}/{nome_arquivo}')


if __name__ == '__main__':  # Se vc estiver importando de outro lugar, ele não vai executar o if. Se tiver executando o if, ele vai funcionar
    tratar_imagens('bdcaptcha')
