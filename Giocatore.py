import threading
from threading import Thread, Lock
import random
import logging


class Player(Thread):
    # thread del giocatore
    def __init__(self, game, player_id):
        Thread.__init__(self)
        self.game = game
        self.id = player_id
        self.card = []
        self.number_lock = Lock()
        self.current_number = 0
        self.row_0 = 0
        self.row_1 = 0
        self.row_2 = 0
        self.award = 0  # montepremi vinto finora dal giocatore

    def create_card(self):
        # crea una lista con i numeri della cartella, e poi un'altra lista con gli stessi numeri ma divisi per colonne
        while len(self.card) < 15:
            n = random.randrange(1, 91)
            while n in self.card:
                n = random.randrange(1, 91)
            self.card.append(n)
        self.card.sort()
        splitted_card = []
        for i in [0, 3, 6, 9, 12]:
            column = self.card[i:(i+3)]  # crea una colonna sotto forma di lista contenente i numeri da i a i+3
            splitted_card.append(column)
        return splitted_card

    def number_check(self, c):
        # controlla se il numero è presente nella cartella e, in tal caso, ne individua la riga tramite il suo indice
        if c in self.card:
            number_index = self.card.index(c)
            number_row = number_index % 3
            if number_row == 0:
                self.row_0 += 1
            elif number_row == 1:
                self.row_1 += 1
            elif number_row == 2:
                self.row_2 += 1

    def communicate_victories(self):
        # controlla se il giocatore ha effettuato una vittoria e aggiorna la matrice condivisa di conseguenza
        if not self.game.global_wins[0][3]:  # se non è ancora stato fatto ambo
            if self.row_0 == 2 or self.row_1 == 2 or self.row_2 == 2:
                with self.game.wins_lock:
                    self.game.global_wins[0][1] += 1  # aggiorna il contatore dei giocatori che hanno fatto ambo
                    self.game.victory_event.set()  # segnala che il contatore è stato aggiornato
                    self.game.global_wins[0][2].append(self.id)
        elif not self.game.global_wins[1][3]:  # se non è ancora stato fatto terno
            if self.row_0 == 3 or self.row_1 == 3 or self.row_2 == 3:
                with self.game.wins_lock:
                    self.game.global_wins[1][1] += 1
                    self.game.victory_event.set()
                    self.game.global_wins[1][2].append(self.id)
        elif not self.game.global_wins[2][3]:  # se non è ancora stata fatta quaterna
            if self.row_0 == 4 or self.row_1 == 4 or self.row_2 == 4:
                with self.game.wins_lock:
                    self.game.global_wins[2][1] += 1
                    self.game.victory_event.set()
                    self.game.global_wins[2][2].append(self.id)
        elif not self.game.global_wins[3][3]:  # se non è ancora stata fatta cinquina
            if self.row_0 == 5 or self.row_1 == 5 or self.row_2 == 5:
                with self.game.wins_lock:
                    self.game.global_wins[3][1] += 1
                    self.game.victory_event.set()
                    self.game.global_wins[3][2].append(self.id)
        elif not self.game.global_wins[4][3]:  # se non è ancora stata fatta decina
            if (self.row_0 == 5 and self.row_1 == 5) or (self.row_1 == 5 and self.row_2 == 5) or (self.row_0 == 5 and self.row_2 == 5):
                with self.game.wins_lock:
                    self.game.global_wins[4][1] += 1
                    self.game.victory_event.set()
                    self.game.global_wins[4][2].append(self.id)
        elif not self.game.global_wins[5][3]:  # se non è ancora stata fatta tombola
            if self.row_0 == 5 and self.row_1 == 5 and self.row_2 == 5:
                with self.game.wins_lock:
                    self.game.global_wins[5][1] += 1
                    self.game.victory_event.set()
                    self.game.global_wins[5][2].append(self.id)

    def run(self):
        while not self.game.locked_win():  # controlla che non sia ancora stata fatta tombola
            if not self.game.victory_event.is_set():  # controlla che la matrice condivisa delle vincite sia aggiornata
                c = self.game.read(self.current_number)
                if c is None:  # caso che si verifica se una partita viene interrotta prima del termine
                    break
                self.current_number = c  # aggiorna current_number assegnandogli il numero appena letto
                with self.game.counter_lock:
                    self.game.players_read_number += 1  # aggiorna il contatore per comunicare di aver letto l'ultimo numero
                self.number_check(c)
                self.communicate_victories()

