class Game():
    def __init__(self, num_players, p1, p2, diff=1, palabra='', tipo=''):
        self.adivinadas = []
        self.intentos = 1
        self.p1 = p1
        self.p2 = p2  # Posiblemente no se use
        self.diff = diff
        self.palabra = palabra
        self.tipo = tipo

    def __str__(self):
        return ('Jugador: %s\nPalabra adivinada: %s\nIntentos Restantes: %s\n'
                % (self.p1, self.concat_palabra(), self.intentos))

    # Atributos de una partida
    @property
    def p1(self):
        return self.__p1

    @p1.setter
    def p1(self, value):
        self.__p1 = value

    @property
    def p2(self):
        return self.__p2

    @p2.setter
    def p2(self, value):
        self.__p2 = value

    @property
    def diff(self):
        return self.__diff

    @diff.setter
    def diff(self, value):
        self.__diff = value

    @property
    def palabra(self):
        return self.__palabra

    @palabra.setter
    def palabra(self, value):
        self.__palabra = value
        for i in self.palabra:
            self.adivinadas.append('_')
        self.intentos = len(self.palabra)*self.diff

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, value):
        self.__tipo = value

    @property
    def intentos(self):
        return self.__intentos

    @intentos.setter
    def intentos(self, value):
        self.__intentos = value

    @property
    def adivinadas(self):
        return self.__adivinadas

    @adivinadas.setter
    def adivinadas(self, value):
        self.__adivinadas = value

    def concat_palabra(self):
        concat = ''
        for i in self.palabra:
            concat += i
        return concat
