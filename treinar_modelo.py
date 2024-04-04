import cv2
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit

dados = []
rotulos = []  # A, B, C, D, E, F...
pasta_base_imagens = 'base_letras'

# Olha dentro da pasta base letras e procurar as imagens e transformar em lista
imagens = paths.list_images(pasta_base_imagens)


for arquivo in imagens:
    rotulo = arquivo.split("\\")[1]  # NO LUGAR DE \  pode ser > (os.path.sep)
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Padronizar a imagem 20x20
    imagem = resize_to_fit(imagem, 20, 20)

    # adicionar uma dimensão para o Keras poder ler a imagem.
    imagem = np.expand_dims(imagem, axis=2)

    # adicionar às listas de dados e rótulos
    rotulos.append(rotulo)
    dados.append(imagem)

dados = np.array(dados, dtype="float") / 255
rotulos = np.array(rotulos)

# separar dados de treino (75%) e dados de teste (25%)
(X_train, X_test, Y_train, Y_test) = train_test_split(dados, rotulos, test_size=0.25, random_state=0)

#   Converter com one-hot encoding
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# salvar o labelbinarizer em um arquivo com o pickle. Salva os numeros sobre o a, b ,c... e traduz
with open('rotulos_modelo.dat', 'wb') as arquivo_pickle:
    pickle.dump(lb, arquivo_pickle)

# Criar e treinar a IA
modelo = Sequential()

# criar as camadas da rede neural
modelo.add(Conv2D(20, (2, 5), padding='same',
           input_shape=(20, 20, 1), activation='relu'))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Criar a 2° camada
modelo.add(Conv2D(50, (5, 5), padding='same', activation='relu'))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Mais uma camada
modelo.add(Flatten())
modelo.add(Dense(500, activation='relu'))

# Camada de saída
modelo.add(Dense(26, activation='softmax'))

# compilar todas as camadas
modelo.compile(loss='categorical_crossentropy',
               optimizer='adam', metrics=['accuracy'])

#################

# Treinar a rede neural (IA)
modelo.fit(X_train, Y_train, validation_data=(
    X_test, Y_test), batch_size=26, epochs=10, verbose=1)

# Salvar o Modelo em um Arquivo
modelo.save('modelo_treinado.hdf5')
