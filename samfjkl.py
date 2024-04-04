class quadrado:
    def __init__(self, lado):
        self.lado = lado
        self.area = lado * lado
        self.perimetro = 4 * lado
        print('O lado é: ', self.lado)
        print('A área é:', self.area)

    def calculoPerimetro(self):
        print('O perímetro é:', self.perimetro)
        
    '''@hdskj
    def calculoPerimetro(self):
        print('O perímetro é:', self.perimetro)
        def ksakl(self):
        def 
            def '''


lado = int(input('Digite o lado do quadrado: '))
q1 = quadrado(lado)

q1.calculoPerimetro()






def hdskj(func):
    def wrapper():
        print('0')
        func()
    return wrapper
