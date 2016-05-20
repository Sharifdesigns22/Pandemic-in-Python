'''Pandemic Blue Deck
Code originally made by Gawain Taylor, John Colfer, and KC Jones
GUI made by KC Jones with tkinter'''

import random
import os
import sys
import tkinter as tk

Player_Hands = [[], [], [], []]
Discard_Pile = []
'''These lines are magic and make the icon work when the code is compiled into an executable.'''
datafile = 'icon.ico'
if not hasattr(sys, 'frozen'):
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)

#This class is the window which asks the preliminary questions.
class Initialize(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Initialize")
        self.attributes("-topmost", True)
        self.iconbitmap(default = datafile)
        self.w = 250
        self.h = 230
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        self.lblPlayers = tk.Label(self, text = "How many people are playing?").pack(padx = 5, pady = 5)
        self.entryPlayers = tk.Entry(self)
        self.entryPlayers.focus_force()
        self.entryPlayers.pack(padx = 5, pady = 5)
        self.lblCards = tk.Label(self, text = "How many cards are in each hand for setup?").pack(padx = 5, pady = 5)
        self.entryCards = tk.Entry(self)
        self.entryCards.pack(padx = 5, pady = 5)
        self.lblEpidemics = tk.Label(self, text = "How many Epidemics do you want?").pack(padx = 5, pady = 5)
        self.entryEpidemics = tk.Entry(self)
        self.entryEpidemics.pack(padx = 5, pady = 5)
        
        self.btnSubmit = tk.Button(self, text = "Submit", command = self.setVars).pack(padx = 5, pady = 10)

    #This sets the variables for players, cards, and epidemics.
    #They can be called with initialize.<name>
    def setVars(self):
        if 2 <= int(self.entryPlayers.get()) <= 4:
            self.Players = self.entryPlayers.get()
            if 1 <= int(self.entryCards.get()) <= 7:
                self.Cards = self.entryCards.get()
                if 1 <= int(self.entryEpidemics.get()) <= 6:
                    self.Epidemics = self.entryEpidemics.get()
                    self.destroy()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


#This is the main window with the players' hands and actions. 
class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Blue Deck")
        self.focus_force()
        self.w = 350
        self.h = 400 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.4) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        self.Role_List = ["Medic", "Dispatcher", "Researcher", "Scientist", "Operations Expert", "Contingency Planner", "Quarantine Specialist"]
        self.Player_Deck = ["B-Atlanta", "B-San_Francisco", "B-Chicago", "B-Toronto",
            "B-New_York", "B-Washington", "B-London", "B-Madrid", "B-Essen", "B-Paris",
            "B-St._Petersburg", "B-Milan", "Y-Los_Angeles", "Y-Mexico_City", "Y-Miami",
            "Y-Bogota", "Y-Lima", "Y-Santiago", "Y-Buenos_Aires", "Y-Sao_Paulo", "Y-Lagos",
            "Y-Khartoum", "Y-Kinshasa", "Y-Johannesburg", "BL-Algiers", "BL-Cairo",
            "BL-Istanbul", "BL-Moscow", "BL-Riyadh", "BL-Baghdad", "BL-Tehran", "BL-Karachi",
            "BL-Mumbai", "BL-Dehli", "BL-Chennai", "BL-Kolkata", "R-Bangkok", "R-Jakarta",
            "R-Sydney", "R-Ho_Chi_Minh_City", "R-Manilla", "R-Hong_Kong", "R-Taipei", "R-Osaka",
            "R-Shanghai", "R-Beijing", "R-Seoul", "R-Tokyo", "Forecast", "One_Quiet_Night", "Airlift", "Government_Grant"]
        random.shuffle(self.Role_List)
        random.shuffle(self.Player_Deck)
        self.contCard = ''
        self.listRoles = []
        for i in range(int(initialize.Players)):
            self.listRoles.append(self.Role_List[i])
        
        self.Hand_Maker()
        self.Player_Deck = self.Shuffle_Deck(self.Player_Deck, initialize.Epidemics)
        self.hands = tk.Label(self, text = "", wraplengt = 300)
        self.hands.pack(padx = 5, pady = 5)
        self.refresh()

        self.frmBtn = tk.Frame(self, height = 2, bd = 0, relief = 'sunken')
        self.frmBtn.pack(side = 'bottom', padx = 5, pady = 10)
        
        self.btnDraw = tk.Button(self.frmBtn, text = "Draw", command = self.draw).pack(side = 'left')
        self.btnDiscard = tk.Button(self.frmBtn, text = "Discard", command = self.discard).pack(side = 'left')
        self.btnRoles = tk.Button(self.frmBtn, text = "Show Roles", command = self.showroles).pack(side = 'left')
        self.btnGive = tk.Button(self.frmBtn, text = "Give", command = self.give).pack(side = 'left')
        self.btnContPlanner = tk.Button(self.frmBtn, text = "Contingency Planner", command = self.contPlanner)
        
        self.btnContPlanner.pack(side = 'left') if 'Contingency Planner' in self.listRoles else ''
        

    #This draws the players hands, putting them into the Player_Hands list.
    def Hand_Maker(self):
        Hand_Count = 0
        while(Hand_Count < int(initialize.Players)):
            Counter = 0
            while(Counter < int(initialize.Cards)):
                Player_Hands[Hand_Count].insert(0, self.Player_Deck[0])
                self.Player_Deck.pop(0)
                Counter += 1
            Hand_Count += 1

    #This shuffles the epidemics into the deck.
    def Shuffle_Deck(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        for i in out:
            i.append("Epidemic")
            random.shuffle(i)
        return [val for sublist in out for val in sublist]

    #These call other classes, which are windows for each of the actions.
    def draw(self):
        draw = Draw()
        draw.mainloop()

    def discard(self):
        discard = Discard()
        discard.mainloop()

    def showroles(self):
        showroles = ShowRoles()
        showroles.mainloop()

    def give(self):
        give = Give()
        give.mainloop()

    def contPlanner(self):
        contplanner = ContPlanner()
        contplanner.mainloop()

    #This refreshes the player hands in the main window.    
    def refresh(self):
        if int(initialize.Players) == 2:
            self.hands.config(text="Player 1: " + ', '.join(Player_Hands[0]) + "\nPlayer 2: " + ', '.join(Player_Hands[1]) + "\nDiscard Pile: " + ', '.join(Discard_Pile))
        elif int(initialize.Players) == 3:
            self.hands.config(text="Player 1: " + ', '.join(Player_Hands[0]) + "\nPlayer 2: " + ', '.join(Player_Hands[1]) + "\nPlayer 3: " + ', '.join(Player_Hands[2]) + "\nDiscard Pile: " + ', '.join(Discard_Pile))
        elif int(initialize.Players) == 4:
            self.hands.config(text="Player 1: " + ', '.join(Player_Hands[0]) + "\nPlayer 2: " + ', '.join(Player_Hands[1]) + "\nPlayer 3: " + ', '.join(Player_Hands[2]) + "\nPlayer 4: " + ', '.join(Player_Hands[3]) + "\nDiscard Pile: " + ', '.join(Discard_Pile))


#The following classes are windows for each of the actions.
class Draw(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Draw")
        self.attributes("-topmost", True)
        self.geometry("200x100")
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 250
        self.h = 150 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
                
        self.lblDrawing = tk.Label(self, text = "Which player is drawing?").pack(padx = 5, pady = 5)
        self.entDrawing = tk.Entry(self)
        self.entDrawing.focus_force()
        self.entDrawing.pack(padx = 5, pady = 5)
        self.btnDrawing = tk.Button(self, text = "OK", command = self.setDrawing).pack(padx = 5, pady = 10)

      
    def setDrawing(self):
        if self.entDrawing.get() != '':
            if 1 <= int(self.entDrawing.get()) <= int(initialize.Players):
                if len(main.Player_Deck) >= 2:
                    self.drawing = int(self.entDrawing.get()) - 1
                    Player_Hands[self.drawing].insert(0, main.Player_Deck[0])
                    main.Player_Deck.pop(0)
                    Player_Hands[self.drawing].insert(0, main.Player_Deck[0])
                    main.Player_Deck.pop(0)
                else:
                    self.destroy()
                    lose = Lose()
                    lose.mainloop()

                main.unbind("<FocusIn>")
                main.refresh()
                self.destroy()

    def on_closing(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()


class Discard(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Discard")
        self.attributes("-topmost", True)
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 250
        self.h = 180 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        self.lblDiscardPlayer = tk.Label(self, text = "Which player is discarding?").pack(padx = 5, pady = 5)
        self.entDiscardPlayer = tk.Entry(self)
        self.entDiscardPlayer.focus_force()
        self.entDiscardPlayer.pack(padx = 5, pady = 5)
        self.lblDiscardCard = tk.Label(self, text = "Which card are you discarding?").pack(padx = 5, pady = 5)
        self.entDiscardCard = tk.Entry(self)
        self.entDiscardCard.pack(padx = 5, pady = 5)
        self.btnDiscard = tk.Button(self, text = "OK", command = self.setDiscard).pack(padx = 5, pady = 10)

    def setDiscard(self):
        if self.entDiscardPlayer.get() != '' or self.entDiscardCards.get() != '':
            if 1 <= int(self.entDiscardPlayer.get()) <= int(initialize.Players) and 1 <= int(self.entDiscardCard.get()) <= int(len(Player_Hands[int(self.entDiscardPlayer.get()) - 1])):
                self.discardPlayer = int(self.entDiscardPlayer.get()) - 1
                self.discardCard = int(self.entDiscardCard.get()) - 1
                Discard_Pile.insert(0, Player_Hands[self.discardPlayer][self.discardCard])
                Player_Hands[self.discardPlayer].pop(self.discardCard)
                main.unbind("<FocusIn>")
                main.refresh()
                self.destroy()

    def on_closing(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()


class ShowRoles(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Show Roles")
        self.attributes("-topmost", True)
        self.focus_force()
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 250
        self.h = 130 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        self.lblRoles = tk.Label(self, text = "")
        self.lblRoles.pack(padx = 5, pady = 5)
        self.btnRoles = tk.Button(self, text = "OK", command = self.close).pack(padx = 5, pady = 5)
        
        self.lblRoles.config(text = '\n'.join(main.listRoles))
            

    def close(self):
        main.unbind("<FocusIn>")
        self.destroy()

    def on_closing(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()


class Give(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Give")
        self.attributes("-topmost", True)
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 250
        self.h = 230 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        self.lblGiving = tk.Label(self, text = "Which player is giving?").pack(padx = 5, pady = 5)
        self.entGiving = tk.Entry(self)
        self.entGiving.focus_force()
        self.entGiving.pack(padx = 5, pady = 5)
        
        self.lblRecieving = tk.Label(self, text = "Which player is recieving?").pack(padx = 5, pady = 5)
        self.entRecieving = tk.Entry(self)
        self.entRecieving.pack(padx = 5, pady = 5)
        
        self.lblCard = tk.Label(self, text = "Which card will be given?").pack(padx = 5, pady = 5)
        self.entCard = tk.Entry(self)
        self.entCard.pack(padx = 5, pady = 5)
        
        self.btnGiving = tk.Button(self, text = "OK", command = self.setGive).pack(padx = 5, pady = 10)

    def setGive(self):
        if self.entGiving.get() != '' and self.entRecieving.get() != '' and self.entCard.get() != '':
            if 1 <= int(self.entGiving.get()) <= int(initialize.Players) and 1 <= int(self.entRecieving.get()) <= int(initialize.Players) and 1 <= int(self.entCard.get()) <= int(len(Player_Hands[int(self.entGiving.get())])):
                self.giving = int(self.entGiving.get()) - 1
                self.recieving = int(self.entRecieving.get()) - 1
                self.card = int(self.entCard.get()) - 1
                Player_Hands[self.recieving].insert(0, Player_Hands[self.giving][self.card])
                Player_Hands[self.giving].pop(self.card)
                main.unbind("<FocusIn>")
                main.refresh()
                self.destroy()

    def on_closing(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()


class ContPlanner(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Contingency Planner")
        self.attributes("-topmost", True)
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 250
        self.h = 110 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/1.2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        if main.contCard == '':
            self.lblCont = tk.Label(self, text = "Which card would you like to take?").pack(padx = 5, pady = 5)
            self.entCont = tk.Entry(self)
            self.entCont.focus_force()
            self.entCont.pack(padx = 5, pady = 5)
            self.btnCont = tk.Button(self, text = "OK", command = self.contClose).pack(padx = 5, pady = 10)

        else:
            self.lblCont = tk.Label(self, text = "The card is " + main.contCard).pack(padx = 5, pady = 5)
            self.frmBtn = tk.Frame(self, height = 2, bd = 0, relief = 'sunken')
            self.frmBtn.pack(padx = 5, pady = 10)
            self.btnUse = tk.Button(self.frmBtn, text = "Use", command = self.contUse).pack(side = 'left')
            self.btnClose = tk.Button(self.frmBtn, text = "Close", command = self.endClose).pack(side = 'left')


    def contClose(self):
        if 1 <= int(self.entCont.get()) <= len(Discard_Pile):
            main.contCard = Discard_Pile[int(self.entCont.get()) - 1]
            Discard_Pile.pop(int(self.entCont.get()) - 1)
            self.endClose()

    def contUse(self):
        main.contCard = ''
        self.endClose()            

    def endClose(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def on_closing(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()
        
        


#This class is the window that pops up when you lose, and quits everything.
class Lose(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Pandemic")
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.lblLose = tk.Label(self, text = "You Lose!").pack(padx = 5, pady = 5)
        self.btnLose = tk.Button(self, text = "Close", command = self.close).pack(padx = 5, pady = 10)

    def close(self):
        main.unbind("<FocusIn>")
        main.destroy()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#This defines the class as a variable, allowing variables inside them to be called.
initialize = Initialize()
#This one calls the window to open.
initialize.mainloop()

#Same thing, with the main class.
main = Main()
main.mainloop()
