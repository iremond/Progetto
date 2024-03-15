import tkinter as tk
from Giocatore import Player
from Banditore import Server
from Partita import Game
import logging


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Tombola")
        self.root.resizable(0, 0)
        self.title_label = tk.Label(master=self.root, text="Gioca a tombola!", font="Cambria 20", fg='dark red')
        self.title_label.pack()
        self.awards_frame = tk.Frame(master=self.root, borderwidth=2, relief=tk.RAISED, bg="beige")
        self.awards_frame.pack()
        self.awards_title_label = tk.Label(master=self.awards_frame, text="Premi in palio:", font="Calibri 13", bg="beige")
        self.awards_title_label.pack()
        self.awards_label_1 = tk.Label(master=self.awards_frame, text="Ambo: 4€\tTerno: 6€\tQuaterna: 8€", font="Calibri 11", bg="beige")
        self.awards_label_2 = tk.Label(master=self.awards_frame, text="Cinquina: 10€\tDecina: 20€\tTombola: 30€", font="Calibri 11", bg="beige")
        self.awards_label_1.pack()
        self.awards_label_2.pack()
        self.label = tk.Label(text="Numero di giocatori prenotati:", font="Calibri 11")
        self.label.pack()
        # Crea una entry che tiene traccia del numero di giocatori prenotati
        self.entry = tk.Entry(justify='center', state='disabled', font="Calibri 11")
        self.entry.pack()
        self.number_of_players = tk.IntVar()  # variabile contenente il numero di giocatori
        self.number_of_players.set(0)
        self.entry["textvariable"] = self.number_of_players  # collegamento stabile
        # Crea un bottone che permette di prenotare un nuovo giocatore
        self.enroll_button = tk.Button(text="Aggiungi giocatore", width=16, height=2, bg='light blue', font="Calibri 11")
        self.enroll_button.pack(side=tk.LEFT)
        self.enroll_button.bind('<Button-1>', self.enroll_handler)  # bottone collegato alla funzione enroll_handler
        # Crea un bottone che permette di eliminare un giocatore prenotato
        self.delete_button = tk.Button(text="Rimuovi giocatore", width=16, height=2, bg='pink', font="Calibri 11")
        self.delete_button.pack(side=tk.LEFT)
        self.delete_button.bind('<Button-1>', self.delete_handler)  # bottone collegato alla funzione delete_handler
        # Crea un bottone che permette di confermare il numero di giocatori selezionato
        self.ok_button = tk.Button(text="Ok", bg="light green", width=16, height=2, font="Calibri 11")
        self.ok_button.pack(side=tk.LEFT)
        self.ok_button.bind('<Button-1>', self.ok_handler)  # bottone collegato alla funzione ok_handler
        self.name_labels = []
        self.name_entries = []
        self.names = []
        self.colors = ['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080']
        # Crea un bottone che dà avvio alla partita
        self.start_button = tk.Button(text="Inizia a giocare!", width=16, height=2, bg='light green', font="Calibri 11")
        self.start_button.bind('<Button-1>', self.start_handler)  # il bottone è collegato alla funzione start_handler

        self.game = Game(self.number_of_players.get())  # crea la partita e passa come parametro il numero di giocatori
        self.server = Server(self.game)  # crea il server
        self.game_started_label = tk.Label(text="La partita è iniziata! Impossibile unirsi ora", font="Calibri 11")
        self.last_3_drawn_label = tk.Label(text=f"Ultimi tre numeri estratti:", font='Calibri 15') #  etichetta che conterrà gli ultimi tre numeri estratti
        self.interrupt_button = tk.Button(text="Interrompi partita", font="Calibri 12", bg="pink", height=2)
        self.sure_label = tk.Label(text="Sei sicuro di voler interrompere la partita?", font="Calibri 11")
        self.no_button = tk.Button(text="No, riprendi", width=19, height=2, bg='light green', font="Calibri 11")
        self.yes_button = tk.Button(text="Sì, sono sicuro", width=19, height=2, bg='pink', font="Calibri 11")
        self.all_numbers = []  # lista che conterrà i numeri di tutte le cartelle in gioco
        self.windows_list = []  # lista che conterrà tutte le finestre delle cartelle in gioco
        self.communication_list = []
        self.ending_label = tk.Label(text="La partita è terminata! Ne vuoi iniziare un'altra?", font="Calibri 11")
        self.new_game_button = tk.Button(text="Sì, comincia una nuova partita", height=2, bg='light green', font="Calibri 11")
        self.stop_game_button = tk.Button(text="No, chiudi il gioco", height=2, bg='pink', font="Calibri 11")

    def enroll_handler(self, evento):
        # aggiunge un nuovo giocatore ogni volta che il bottone viene premuto
        n = self.number_of_players.get()
        self.number_of_players.set(n+1)

    def delete_handler(self, evento):
        # elimina un giocatore ogni volta che il bottone viene premuto
        n = self.number_of_players.get()
        if n > 0:
            self.number_of_players.set(n-1)
        else:
            error_window = tk.Tk()
            error_label = tk.Label(master=error_window, text="Attenzione! Deve esserci almeno\nun giocatore per iniziare la partita", font="Calibri 12")
            error_label.pack()

    def ok_handler(self, evento):
        #  permette di confermare il numero di giocatori selezionato e di specificarne i nomi
        if self.number_of_players.get() > 0:  # controlla che ci sia almeno un giocatore prenotato
            self.enroll_button.pack_forget()
            self.delete_button.pack_forget()
            self.ok_button.pack_forget()
            for i in range(self.number_of_players.get()):
                name_label = tk.Label(text=f"Come si chiama il giocatore {i+1}?", font="Calibri 11")
                name_label.pack()
                self.name_labels.append(name_label)
                name_entry = tk.Entry(font='Calibri 11')
                name_entry.pack()
                self.name_entries.append(name_entry)
                name = tk.StringVar()  # variabile contenente il nome
                name.set('')
                name_entry["textvariable"] = name  # collegamento stabile
                self.names.append(name)
            self.start_button.pack()
        else:
            error_window = tk.Tk()
            error_label = tk.Label(master=error_window, text="Attenzione! Deve esserci almeno\nun giocatore per iniziare la partita", font="Calibri 12")
            error_label.pack()

    def start_handler(self, evento):
        # se ogni giocatore ha un nome, chiama avvio_giocatori, fa partire il server e chiama interface_update
        missing = 0
        for i in self.names:
            if len(i.get()) == 0:
                missing_name_window = tk.Tk()  # crea una finestra di errore
                missing_name_label = tk.Label(master=missing_name_window, text="Non hai inserito tutti i nomi dei giocatori!", font="Calibri 12")
                missing_name_label.pack()
                missing += 1
                break
        if missing == 0:
            self.game.number_of_players = self.number_of_players.get()  # aggiorna il numero di giocatori della partita
            self.avvio_giocatori(self.number_of_players.get())  # passa come parametro il numero di giocatori
            self.server.start()  # fa partire il thread server
            self.interface_update()

    def interface_update(self):
        # modifica l'interfaccia distruggendo i bottoni di inizio partita e creando un'entry con i numeri estratti
        self.start_button.pack_forget()
        for i in self.name_labels:
            i.pack_forget()
        for j in self.name_entries:
            j.pack_forget()
        self.game_started_label.pack()
        self.last_3_drawn_label.pack()
        self.update_numbers()  # chiama la funzione update_numbers
        self.interrupt_button.pack()
        self.interrupt_button.bind('<Button-1>', self.interrupt_handler)

    def update_numbers(self):
        # aggiorna continuamente l'interfaccia, mostrando sempre gli ultimi tre numeri estratti
        if len(self.game.estratti) == 1:
            self.last_3_drawn_label['text'] = f"Ultimi tre numeri estratti:\n{(', '.join(map(str, self.game.estratti[-1:])))}"
        elif len(self.game.estratti) == 2:
            self.last_3_drawn_label['text'] = f"Ultimi tre numeri estratti:\n{(', '.join(map(str, self.game.estratti[-2:])))}"
        elif len(self.game.estratti) >= 3:
            self.last_3_drawn_label['text'] = f"Ultimi tre numeri estratti:\n{(', '.join(map(str, self.game.estratti[-3:])))}"
        if not self.game.locked_win():  # se la partita non è ancora finita
            self.root.after(10, self.update_numbers)
        else:
            self.game_started_label.pack_forget()
            self.interrupt_button.pack_forget()
            self.ending_label.pack()
            self.new_game_button.pack(side=tk.LEFT)
            self.new_game_button.bind('<Button-1>', self.new_game_handler)
            self.stop_game_button.pack(side=tk.LEFT)
            self.stop_game_button.bind('<Button-1>', self.stop_handler)

    def stop_handler(self, evento):
        # distrugge l'interfaccia
        self.root.destroy()
        for x in self.windows_list:
            x.destroy()

    def new_game_handler(self, evento):
        # distrugge le cartelle e ripristina l'interfaccia alla versione iniziale, crea una nuova partita e un Server
        for x in self.windows_list:
            x.destroy()
        self.game_started_label.pack_forget()
        self.last_3_drawn_label.pack_forget()
        self.ending_label.pack_forget()
        self.new_game_button.pack_forget()
        self.stop_game_button.pack_forget()
        self.number_of_players.set(0)
        self.enroll_button.pack(side=tk.LEFT)
        self.delete_button.pack(side=tk.LEFT)
        self.ok_button.pack(side=tk.LEFT)
        self.name_labels = []
        self.name_entries = []
        self.names = []
        self.game = Game(self.number_of_players.get())  # crea la partita e passa come parametro il numero di giocatori
        self.server = Server(self.game)  # crea il server
        self.all_numbers = []  # lista che conterrà i numeri di tutte le cartelle in gioco
        self.communication_list = []
        self.windows_list = []

    def interrupt_handler(self, evento):
        self.interrupt_button.pack_forget()
        self.sure_label.pack()
        self.no_button.pack(side='left', fill='both')
        self.no_button.bind('<Button-1>', self.no_handler)
        self.yes_button.pack(side='left', fill='both')
        self.yes_button.bind('<Button-1>', self.yes_handler)

    def no_handler(self, evento):
        self.sure_label.pack_forget()
        self.no_button.pack_forget()
        self.yes_button.pack_forget()
        self.interrupt_button.pack()

    def yes_handler(self, evento):
        # aggiorna il flag tombola per far terminare il server, mette in coda None per far terminare i giocatori, distrugge l'interfaccia
        with self.game.wins_lock:
            self.game.global_wins[5][3] = True
        self.game.write(None)
        self.root.destroy()
        for x in self.windows_list:
            x.destroy()

    def avvio_giocatori(self, number_of_players):
        # fa partire i thread giocatori e assegna a ciascuno una cartella
        for i in range(number_of_players):  # per ogni giocatore prenotato
            g = Player(self.game, i)  # crea un thread Player, passando come parametri partita e indice identificativo
            g.start()  # lo avvia
            window_card = tk.Tk()
            window_card.title(f"Cartella di {self.names[i].get()}")
            window_card.geometry('320x180')
            window_card.configure(bg='gold')
            window_card.resizable(0, 0)
            self.windows_list.append(window_card)
            card = g.create_card()  # chiama il metodo create_card della classe Player per generare i numeri
            for x in range(3):
                window_card.grid_rowconfigure(x, weight=1)
            for y in range(5):
                window_card.grid_columnconfigure(y, weight=1)
            for r in range(3):
                for c in range(5):
                    # per ogni numero nella cartella, crea un frame contenente un'etichetta con il numero
                    frame = tk.Frame(master=window_card, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=r, column=c, padx=5, pady=5)
                    number = tk.Label(master=frame, text=str(card[c][r]), font="Calibri 12")  # etichetta contenente il numero
                    self.all_numbers.append(number)  # aggiunge l'etichetta alla lista globale di tutti i numeri
                    number.pack()
            communication = tk.Label(master=window_card, text=f"\nIl tuo montepremi attuale ammonta a: {self.game.awards[i]}€", bg='gold', font='Cambria 12', fg='#FF5733')
            communication.grid(row=3, columnspan=5)
            self.communication_list.append(communication)
        self.change_label_color()
        self.show_victories()

    def change_label_color(self):
        # cambia il colore delle etichette contenenti i numeri estratti
        for i in self.all_numbers:
            if str(self.server.new_number) == i['text']:
                i.configure(bg='#FF5733')
        if not self.game.locked_win():  # se la partita non è ancora finita
            self.root.after(1, self.change_label_color)

    def show_victories(self):
        for i in self.game.global_wins:
            if i[1] != 0:
                for x in i[2]:  # per ogni giocatore che ha effettuato la vittoria
                    while self.game.victory_event.is_set():
                        pass
                        # aspetta che il flag dell'evento sia False, cosa che accade dopo che i premi vengono aggiornati
                    self.communication_list[x].configure(text=f"Che fortuna! Hai fatto {i[0]}\nIl tuo montepremi attuale ammonta a: {self.game.awards[x]}€")
                break
        if not self.game.locked_win():  # se la partita non è ancora finita
            self.root.after(1, self.show_victories)


if __name__ == '__main__':
    root = tk.Tk()
    Interface(root)
    root.mainloop()
