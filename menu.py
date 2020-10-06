from game_service import Game_service
import os


# Con esta clase lo que se intenta es recolectar y conectar los datos
# ingresados por el jugador/res
class Menu():
    def __init__(self):
        self.service = Game_service('saves/sum.json')

    def clean(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clean')

    def mostrar_menu(self):
        self.clean()
        print("==== BIENVENIDO AL AHORCADO ====\n")
        print('1. Nuevo juego')
        print('2. Agregar palabras')
        print('3. Resumen del ultimo juego')
        return int(input('Elija una opcion! [1-3]: '))

    def datos_nuevo_juego(self):
        diff = 1
        num = int(input('Ingrese el numero de jugadores: '))
        while num > 2 or num < 0:
            print('[ERROR]: VALOR INVALIDO')
            num = int(input('Ingrese el numero de jugadores: '))
        p1 = self.service.new_player(input('Ingrese el nombre del P1: '))
        if num == 2:
            p2 = self.service.new_player(input('Ingrese el nombre del P2: '))
        if num == 1:
            p2 = "AI"
            diff = int(input('Ingrese una dificultad [1-10]: '))
        return num, p1, p2, diff

    def game_loop_single_player(self, num, p1, p2, diff):
        game = self.service.new_game(num, p1, p2, diff)
        return game

    def game_loop_multi(self, num, p1, p2):
        self.clean()
        print('\n====== MODO MULTIJUGADOR =======')
        palabra = input('%s ingresa una palabra que %s adivine: '
                        % (p1.upper(), p2.upper()))
        tipo = input('Ingrese el tipo de palabra: ')
        game = self.service.new_game(num, p1, p2,
                                     palabra=palabra, tipo=tipo, diff=1000)
        return game

    def main_loop(self):
        while True:
            flag = True
            eleccion = self.mostrar_menu()
            if eleccion == 1:
                self.service.reset()
                num, p1, p2, diff = self.datos_nuevo_juego()
            if eleccion == 2:
                pass
            if eleccion == 3:
                flag = False
            if eleccion == 0:
                break
            while flag:
                flag = False
                if num == 1:
                    game = self.game_loop_single_player(num, p1, p2, diff)
                    multi = False
                if num == 2:
                    game = self.game_loop_multi(num, p1, p2)
                    multi = True
                while True:
                    self.clean()
                    # print(game.palabra)  # palabra "secreta" COMENTAR!
                    print('INTENTOS RESTANTES: %d' % game.intentos)
                    print('CATEGORIA: %s' % game.tipo.upper())
                    for i in game.adivinadas:
                        print(i, end=' ')
                    print(' ')
                    letra = input('Ingrese una letra: ')
                    lost, win = self.service.compare_letter(letra, game)
                    if multi and win:
                        print('CAMBIO DE TURNOS')
                        p1, p2 = p2, p1
                    if lost:
                        self.clean()
                        print('PERDISTE :C')
                        print(game)
                        self.service.end_game(game)
                        flag = bool(int(input('Perder otra vez/'
                                    'Cambiar turnos? Si[1]/No[0]: ')))
                        break
                    if win:
                        self.clean()
                        print('\nFELICIDADES GANASTE!\n')
                        print(game)
                        self.service.end_game(game)
                        flag = bool(int(input('Jugar otra vez/'
                                    'Cambiar turnos? Si[1]/No[0]: ')))
                        break
            self.clean()
            print('\n====== RESUMEN DE LA ULTIMA PARTIDA ======\n')
            print(self.service.resumen_partida())
            input('\ncontinuar...')
