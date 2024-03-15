from threading import Thread
import random
import time
import logging


class Server(Thread):
    def __init__(self, game):
        Thread.__init__(self)
        self.game = game
        self.tabellone = list(range(1, 91))  # lista di numeri da 1 a 90
        self.new_number = None

    def draw(self):
        # estrae i numeri e chiama il metodo write di Game
        index = random.randrange(len(self.tabellone))  # estrae a caso un indice della lista
        self.new_number = self.tabellone[index]
        self.game.write(self.new_number)
        self.tabellone.remove(self.new_number)  # rimuove il numero estratto dal tabellone, per evitare che esca ancora
        time.sleep(2)

    def run(self):
        while not self.game.locked_win():  # controlla che non sia ancora stata fatta tombola
            if len(self.game.estratti) == 0:  # se non è ancora stato estratto nessun numero
                self.draw()
            elif self.game.players_read_number == self.game.number_of_players:
                # aspetta che tutti i giocatori abbiano letto l'ultimo numero estratto
                self.game.players_read_number = 0
                self.draw()
                if self.game.victory_event.is_set():  # se il contatore dei vincitori è stato aggiornato
                    self.game.check_victories()
                    self.game.victory_event.clear()
