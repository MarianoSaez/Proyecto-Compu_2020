from game import Game
import json
from random import randint


class Game_service():
    def __init__(self):
        self.resumen = dict()

    def reset(self):
        self.resumen = dict()
        with open("saves/sum.json", "w") as f:
            f.write("{ }")
            f.close()

    def new_game(self, num_p, p1, p2, diff=1, palabra=None, tipo=''):
        if palabra is None:
            palabra, tipo = self.search_word()
        li = list(palabra.upper())
        return Game(num_p, p1, p2, diff, li, tipo)

# Acciones al crear un nuevo jugador
    def new_player(self, name):
        return name.upper()

# Acciones que se realizan al finalizar un juego
    def end_game(self, game):
        with open("saves/sum.json", 'r+') as f:
            key_p1 = "%s" % game.p1
            self.resumen[key_p1] = game.__dict__
            json.dump(self.resumen, f, indent=4)
            f.close()
        return self.resumen

    def resumen_partida(self):
        jugadores = list(self.resumen)
        jugador1 = jugadores[0]
        letras_palabra1 = self.resumen[jugador1]["_Game__palabra"]
        palabra1 = ''
        intentos1 = self.resumen[jugador1]["_Game__intentos"]
        for i in letras_palabra1:
            palabra1 += i
        if len(jugadores) == 1:
            final = 'Jugador1: %s\nPalabra adivinada: %s\nIntentos: %d\n'\
                     % (jugador1, palabra1, intentos1)
        else:
            jugador2 = jugadores[1]
            letras_palabra2 = self.resumen[jugador2]["_Game__palabra"]
            palabra2 = ''
            for i in letras_palabra2:
                palabra2 += i
            intentos2 = self.resumen[jugador2]["_Game__intentos"]
            final = 'Jugador1: %s\nPalabra adivinada: '\
                    '%s\nIntentos Restantes: %d\n'\
                    '\nJugador2: %s\nPalabra adivinada: '\
                    '%s\nIntentos Restantes: %d'\
                    % (jugador1, palabra1, intentos1,
                       jugador2, palabra2, intentos2)
        return final

# Acciones dentro de una partida
# Single Player

    # Recupera del repo una palabra con su tipo
    def search_word(self):
        with open("saves/pool_palabras.json") as f:
            pool_palabras = json.load(f)
            index = str(randint(0, len(pool_palabras)-1))
            palabra = pool_palabras[index]['_palabra']
            tipo = pool_palabras[index]['_tipo_palabra']
            f.close()
        return palabra, tipo

    # Compara si la letra pasada como param se encuentra en la palabra
    def compare_letter(self, letter, game):
        letter = letter.upper()
        lost = False
        stop = False
        for i in range(len(game.palabra)):
            if game.palabra[i] == letter:
                game.adivinadas[i] = letter
        diferencia = [i for i in game.palabra if i in game.adivinadas]
        if len(diferencia) == len(game.palabra):
            stop = True
        game.intentos -= 1
        if game.intentos == 0 and not stop:
            lost = True
            game.intentos = 'PERDIDO'
        return lost, stop

# Multiplayer

# Acciones fuera de juego

    # Permite agregar palabras nuevas
    def add_new_word(self):
        pass
