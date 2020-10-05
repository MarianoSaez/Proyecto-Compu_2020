import unittest
from parameterized import parameterized
from game_service import Game_service
from game import Game
import json


class TestServicio(unittest.TestCase):
    def setUp(self):
        super().setUp()
        with open('saves/pool_palabras.json', 'r') as f:
            self.repo = json.load(f)
        self.service = Game_service()

    @parameterized.expand([
        (1, 'mariano', None, 10),
        (2, 'martin', 'bruno', 10)
    ])
    def test_AI_new_game(self, num_players, p1, p2, diff):
        juego = self.service.new_game(num_players, p1, p2, diff)
        palabra = juego.palabra
        tipo = juego.tipo
        juego_dos = Game(num_players, p1, p2, diff, palabra, tipo)
        # En principio los objetos son distintos por lo que
        # los convierto a diccionario para comparar sus atributos
        # que deberian ser identicos
        self.assertEqual(juego.__dict__, juego_dos.__dict__)

    # @parameterized.expand([
    #     ('mariano', {'_Player__name': 'mariano', '_Player__life': 0}),
    #     ('bruno', {'_Player__name': 'bruno', '_Player__life': 0}),
    #     ('agustin', {'_Player__name': 'agustin', '_Player__life': 0})
    # ])
    # def test_AII_new_player(self, name, dicc_jugador):
    #     jugador = self.service.new_player(name)
    #     self.assertDictEqual(jugador.__dict__, dicc_jugador)

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

    def test_BII_compare_letter(self):
        pass


if __name__ == "__main__":
    unittest.main()
