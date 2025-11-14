class Transporte:

    def __init__(self, capacidade, vel_maxima):
        self.__capacidade = capacidade
        self.__vel_maxima = vel_maxima

    def getCapacidade(self):
        return self.__capacidade
    
    def getVelMaxima(self):
        return self.__vel_maxima
    
    def descricao(self):
        print(f'A capacidade é: {self.getCapacidade()} e a velocidade máxima é: {self.getVelMaxima()}')
        
    def mover(self):
        print('O transporte está em movimento')

class Onibus(Transporte):
    def __init__(self, capacidade, vel_maxima):
        super().__init__(capacidade, vel_maxima)

    def mover(self):
        print('O ônibus está seguindo a rota')

class Bicicleta(Transporte):

    def __init__(self, capacidade, vel_maxima):
        super().__init__(capacidade, vel_maxima)

    def mover(self):
        print('A bicicleta está sendo pedalada')

onibus1 = Onibus(30, '80 km/h')
bike1 = Bicicleta(1, '40 km/h')

onibus1.descricao()
onibus1.mover()

bike1.descricao()
bike1.mover()