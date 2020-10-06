import unittest
from parameterized import parameterized
from game_service import Game_service
from game import Game
import json


class TestServicio(unittest.TestCase):
    def setUp(self):
        super().setUp()
        with open('test_saves/pool_palabras.json', 'r') as f:
            self.repo = json.load(f)
        self.service = Game_service('test_saves/sum.json')

    @parameterized.expand([
        (1, 'mariano', None, 10),
        (2, 'martin', 'bruno', 10)
    ])
    def test_AI_new_game(self, num_players, p1, p2, diff):
        juego = self.service.new_game(num_players, p1, p2, diff)
        palabra = juego.palabra
        tipo = juego.tipo
        juego_dos = Game(num_players, p1, p2, diff, palabra, tipo)
        self.assertEqual(juego.__dict__, juego_dos.__dict__)

    @parameterized.expand([
        ('semaforo'),
        ('CALculadORA'),
        ('pizza'),
        ('Cafe'),
        ('milanESAS')
    ])
    def test_AII_new_player(self, nombre):
        player = self.service.new_player(nombre)
        self.assertEqual(nombre.upper(), player)

    def test_BI_search_word_palabra(self):
        flag = False
        palabra, tipo = self.service.search_word()
        for i in self.repo:
            if self.repo[i]['_palabra'] == palabra:
                flag = True
                break
        self.assertTrue(flag)

    def test_BII_search_word_tipo(self):
        flag = False
        palabra, tipo = self.service.search_word()
        for i in self.repo:
            if self.repo[i]['_tipo_palabra'] == tipo\
               and self.repo[i]['_palabra'] == palabra:
                flag = True
                break
        self.assertTrue(flag)

    @parameterized.expand([
        ('PYTHON', 'p'),
        ('TAZA', 'a'),
        ('ESCRITORIO', 'O'),
        ('PERRO', 'R')
    ])
    def test_CI_compare_letter_adivinada(self, palabra, letter):
        game = Game(1, 'A', 'B', 1, palabra)
        self.service.compare_letter(letter, game)
        self.assertIn(letter.upper(), game.adivinadas)

    @parameterized.expand([
        ('PYTHON', ['A', 'B', 'C']),
        ('TAZA', ['A', 'B', 'C']),
        ('ESCRITORIO', ['A', 'B', 'C', 'D', 'E']),
        ('PERRO', ['A', 'B', 'C', 'D'])
    ])
    def test_CII_compare_letter_intentos(self, palabra, letters):
        game = Game(1, 'A', 'B', 1, palabra)
        intentos_inicial = game.intentos
        for i in letters:
            self.service.compare_letter(i, game)
        intentos_final = intentos_inicial - len(letters)
        self.assertEqual(intentos_final, game.intentos)

    @parameterized.expand([
        ('SEMAFORO'),
        ('CALCULADORA'),
        ('PIZZA'),
        ('CAFE'),
        ('MILANESAS')
    ])
    def test_CIII_compare_letter_lost(self, palabra):
        game = Game(1, 'A', 'B', 1, palabra)
        for i in range(len(palabra)):
            lost, win = self.service.compare_letter('x', game)
        self.assertTrue(lost)

    @parameterized.expand([
        ('SEMAFORO'),
        ('CALCULADORA'),
        ('PIZZA'),
        ('CAFE'),
        ('MILANESAS')
    ])
    def test_CIV_compare_letter_win(self, palabra):
        game = Game(1, 'A', 'B', 1, palabra)
        for i in list(palabra):
            lost, win = self.service.compare_letter(i, game)
            if win:
                break
        self.assertTrue(win)

    def test_DI_resumen_partida(self):
        pass

    def test_DII_resumen_partida(self):
        pass

    @parameterized.expand([
        ('mariano', 'bruno', 'guitarra'),
        ('nahuel', 'nicolas', 'juegos'),
        ('luciana', 'camila', 'television')
    ])
    def test_EI_end_game(self, p1, p2, palabra):
        self.service.reset()
        game = self.service.new_game(1, p1, p2, 1, palabra)
        resumen = self.service.end_game(game)
        with open('test_saves/sum.json', 'r+') as f:
            archivo = json.load(f)
        self.assertEqual(resumen, archivo)

    @parameterized.expand([
        ('mariano', 'bruno', 'guitarra'),
        ('nahuel', 'nicolas', 'juegos'),
        ('luciana', 'camila', 'television')
    ])
    def test_FI_reset(self, p1, p2, palabra):
        game = self.service.new_game(1, p1, p2, 1, palabra)
        self.service.end_game(game)
        self.service.reset()
        with open('test_saves/sum.json', 'r') as f:
            vacio = json.load(f)
        self.assertEqual(vacio, {})


if __name__ == "__main__":
    unittest.main()
