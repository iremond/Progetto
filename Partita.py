import logging
import threading
from threading import Condition, Lock
from queue import Queue
from collections import defaultdict


class Game:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players  # numero di giocatori nella partita
        self.game_lock = Condition()
        self.numbers = Queue(maxsize=1)  # coda contenente, di volta il volta, l'ultimo numero estratto
        self.estratti = []  # lista dei numeri estratti
        self.wins_lock = Lock()
        self.global_wins = [['ambo', 0, [], False, 4], ['terno', 0, [], False, 6], ['quaterna', 0, [], False, 8],
                            ['cinquina', 0, [], False, 10], ['decina', 0, [], False, 20], ['tombola', 0, [], False, 30]]
        # per ogni vincita: nome, numero di vincite contemporanee, ID del/dei giocatori che le hanno fatte, flag, premio
        self.victory_event = threading.Event()
        self.players_read_number = 0  # contatore che si aggiorna ogni volta che un giocatore legge l'ultimo numero
        self.counter_lock = Lock()
        self.awards = defaultdict(int)  # dizionario che conterrà i montepremi in denaro di ogni giocatore
        for i in range(self.number_of_players):
            self.awards[i] = 0

    def write(self, number):
        # scrive il nuovo numero nella coda
        self.game_lock.acquire()
        while self.numbers.full():
            self.game_lock.wait()
        self.numbers.put(number)
        logging.info(number)
        self.game_lock.notify_all()
        self.game_lock.release()

    def read(self, num):
        # legge e restituisce l'ultimo numero messo in coda o, se è vuota, l'ultimo della lista dei numeri estratti
        self.game_lock.acquire()
        while not self.numbers.full():  # se la coda è vuota
            if len(self.estratti) == 0 or num == self.estratti[len(self.estratti)-1]:
                # se non è ancora stato estratto alcun numero, o se il numero appena letto è uguale all'ultimo della lista estratti
                self.game_lock.wait()
            else:  # se il numero appena letto è diverso dall'ultimo numero della lista degli estratti
                self.game_lock.notify_all()
                self.game_lock.release()
                return self.estratti[len(self.estratti)-1]  # restituisce l'ultimo numero della lista degli estratti
        number = self.numbers.get()  # prende il numero in coda
        self.estratti.append(number)  # aggiunge il numero alla lista degli estratti
        self.numbers.task_done()
        self.game_lock.notify_all()
        self.game_lock.release()
        return number

    def locked_win(self):
        # controlla, dopo aver acquisito una lock, se è stata fatta tombola oppure no
        with self.wins_lock:
            value = self.global_wins[5][3]
        return value

    def check_victories(self):
        # controlla la matrice global_wins per vedere se ci sono state vincite: in tal caso aggiorna la matrice e il montepremi
        with self.wins_lock:
            for i in self.global_wins:
                if not i[3]:  # se la vincita i ha il flag a False, cioè non è ancora stata fatta
                    if i[1] == 1:  # se solo un giocatore ha effettuato la vincita i con l'ultimo numero
                        self.awards[i[2][0]] += i[4]  # aggiorna il montepremi del vincitore nell'apposito dizionario
                        i[3] = True  # aggiorna il flag
                        i[1] = 0  # azzera il contatore dei vincitori
                        break  # non serve controllare che siano state effettuate anche le vincite successive
                    elif i[1] > 1:  # se più giocatori hanno effettuato la vincita i con l'ultimo numero
                        for x in i[2]:  # per ogni giocatore che ha effettuato la vincita
                            self.awards[x] += (i[4]/i[1])  # divide il premio tra i vincitori e aggiorna il dizionario
                        i[3] = True  # aggiorna il flag
                        i[1] = 0  # azzera il contatore dei vincitori
                        break  # non serve controllare che siano state effettuate anche le vincite successive
