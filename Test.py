import unittest
from Partita import Game
from Banditore import Server
from Giocatore import Player


class Test(unittest.TestCase):
    def setUp(self):
        self.game = Game(1)
        self.banditore = Server(self.game)
        self.giocatore = Player(self.game, 0)

    def test_write_and_read_queue(self):
        number = 4
        self.game.write(number)
        number_read = self.game.read(8)
        self.assertIs(number, number_read)

    def test_splitted_card_length(self):
        card = self.giocatore.create_card()
        self.assertEqual(len(card), 5)

    def test_card_length(self):
        self.giocatore.create_card()
        self.assertEqual(len(self.giocatore.card), 15)

    def test_card_columns_length(self):
        card = self.giocatore.create_card()
        self.assertEqual(len(card[0]), 3)

    def test_number_check(self):
        card = self.giocatore.create_card()
        self.giocatore.number_check(card[0][0])  # passo come parametro a number_check il primo numero della cartella
        self.assertEqual(self.giocatore.row_0, 1)  # verifica che il contatore dei numeri estratti nella prima riga sia 1

    def test_communicate_victories(self):
        self.giocatore.row_0 = 2  # la prima riga contiene due numeri estratti
        self.giocatore.communicate_victories()
        self.assertEqual(self.game.global_wins[0][1], 1)

    def test_check_victories(self):
        self.game.global_wins[0][1] = 2  # due giocatori hanno fatto ambo
        self.game.global_wins[0][2] = [0, 1]
        self.game.check_victories()
        self.assertEqual(self.game.awards[0], 2)  # verifica che il loro montempremi sia di 2 euro a testa


if __name__ == '__main__':
    unittest.main()
