'''Pandemic Infection Deck
Code originally made by Gawain Taylor and John Colfer
GUI made by KC Jones with tkinter'''

import random
import os
import sys
import tkinter as tk
'''These lines are magic and make the icon work when the code is compiled into an executable.'''
datafile = 'icon.ico'
if not hasattr(sys, 'frozen'):
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)

'''Initial window class. This tells you where to put the first disease cubes, and sets up some variables.'''
class Initialize(tk.Tk):
    def __init__(self):
        '''This section is pretty much the same in each class. It tells it to open the tkinter window,
        configures some of its settings, and sets its position.'''
        tk.Tk.__init__(self)
        self.title("Initialize") #Sets the title of the window.
        self.attributes("-topmost", True) #Puts this window on top.
        self.iconbitmap(default = datafile) #Sets the window icon.
        self.w = 400
        self.h = 110 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/10) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y)) #All these previouse lines set the dimensions of the window and position it on the screen.

        '''This is the infection deck, where all the cards are stored. The next one is the discard pile, which
        starts out empty. The infection deck is then shuffled for the first time.'''
        self.Infection_Deck = ["B-Atlanta", "B-San_Francisco", "B-Chicago", "B-Toronto", "B-New_York",
         "B-Washington", "B-London", "B-Madrid", "B-Essen", "B-Paris", "B-St._Petersburg", "B-Milan",
         "Y-Los_Angeles", "Y-Mexico_City", "Y-Miami", "Y-Bogota", "Y-Lima", "Y-Santiago", "Y-Buenos_Aires",
         "Y-Sao_Paulo", "Y-Lagos", "Y-Khartoum", "Y-Kinshasa", "Y-Johannesburg", "BL-Algiers", "BL-Cairo",
         "BL-Istanbul", "BL-Moscow", "BL-Riyadh", "BL-Baghdad", "BL-Tehran", "BL-Karachi", "BL-Mumbai",
         "BL-Dehli", "BL-Chennai", "BL-Kolkata", "R-Bangkok", "R-Jakarta", "R-Sydney", "R-Ho_Chi_Minh_City",
         "R-Manilla", "R-Hong_Kong", "R-Taipei", "R-Osaka", "R-Shanghai", "R-Beijing", "R-Seoul", "R-Tokyo"]
        self.Infection_Discard = []
        random.shuffle(self.Infection_Deck)

        '''This creates a label for the initialization step, packs it (shoves it wherever it fits), and
        creates a button to close the window.'''
        self.lblCubes = tk.Label(self, text = "")
        self.lblCubes.pack(padx = 5, pady = 5)
        self.btnCubes = tk.Button(self, text = "OK", command = self.close).pack(padx = 5, pady = 10)
        
        '''This changes the text in the label above, and sets it to the correct cities from the top of the infection
        deck. It then removes them from the deck, and puts them in the discard'''
        self.lblCubes.config(text = "Put 3 cubes on " + ', '.join(self.Infection_Deck[0:3]) + "\nPut 2 cubes on " +
            ', '.join(self.Infection_Deck[3:6]) + "\nPut 1 cube on  " + ', '.join(self.Infection_Deck[6:9]))
        for i in range(9):
            self.Infection_Discard.insert(0, self.Infection_Deck[0])
            self.Infection_Deck.pop(0)

    '''This function is called when btnCubes is pressed, and closes the window.'''
    def close(self):
        self.destroy()
        
        
        
'''This class is the main window, which shows the discard pile and holds the buttons to do all the things.'''
class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Infection")
        self.focus_force() #Sets the focus to this window.
        self.w = 400
        self.h = 150 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/10) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        '''This label shows the discard pile.'''
        self.lblDiscard = tk.Label(self, text = "Discard Pile: " + ', '.join(initialize.Infection_Discard), wraplengt = 390)
        self.lblDiscard.pack(padx = 5, pady = 5)

        '''This is a frame that holds all the buttons, allowing them to be placed next to each other.'''
        self.frmBtn = tk.Frame(self, height = 2, bd = 0, relief = 'sunken')
        self.frmBtn.pack(side = 'bottom', padx = 5, pady = 10)

        '''These are the buttons. They launch other windows that do things to the deck.'''
        self.btnDraw = tk.Button(self.frmBtn, text = "Draw", command = self.draw).pack(side = 'left')
        self.btnEpidemic = tk.Button(self.frmBtn, text = "Epidemic", command = self.epidemic).pack(side = 'left')
        self.btnForecast = tk.Button(self.frmBtn, text = "Forecast", command = self.forecast).pack(side = 'left')
        self.btnEesPop = tk.Button(self.frmBtn, text = "Resilient Population", command = self.resPop).pack(side = 'left')

    '''These functions are called by the buttons. They each define the class holding the window as a variable, then call it.'''
    def draw(self):
        draw = Draw()
        draw.mainloop()

    def epidemic(self):
        epidemic = Epidemic()
        epidemic.mainloop()

    def forecast(self):
        forecast = Forecast()
        forecast.mainloop()
        
    def resPop(self):
        respopulation = ResPopulation()
        respopulation.mainloop()
        
    '''This "refreshes" the discard pile label, resetting the text. It is called at the end of each other window's action.'''
    def refresh(self):
        self.lblDiscard.config(text = "Discard Pile: " + ', '.join(initialize.Infection_Discard))
 
      
'''This window draws a card from the deck, tells you what it is, and discards it.'''
class Draw(tk.Tk):
    def __init__(self):
        '''This set of initialization settings is slightly different from the previous ones.'''
        tk.Tk.__init__(self)
        self.title("Draw")
        self.attributes("-topmost", True)
        self.focus_force()
        main.bind("<FocusIn>", self.alarm) #This and the alarm function it calls prevents the user from clicking the main window.
        self.protocol("WM_DELETE_WINDOW", self.close) #This calls the close function when the window is manually closed.
        self.w = 180
        self.h = 80 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/10) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        '''Creates the label that tells you what card was drawn and a close button.'''
        self.lblDrawn = tk.Label(self, text = "You have drawn " + initialize.Infection_Deck[0]).pack(padx = 5, pady = 5)
        self.btnDrawn = tk.Button(self, text = "OK", command = self.close).pack(padx = 5, pady = 10)
        
        initialize.Infection_Discard.insert(0, initialize.Infection_Deck[0])
        initialize.Infection_Deck.pop(0)

    '''This is called when the close button is pressed, and lets you click the main window again,
    refreshes the discard pile, and kills this window.'''
    def close(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    '''Called when user clicks the main window. It forces focus on this window and makes a ding.'''
    def alarm(self, event):
        self.focus_force()
        self.bell()


'''This one draws the bottom card of the deck, tells the user what it is, and shuffles it and the discard pile back into the main deck.'''
class Epidemic(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Epidemic")
        self.attributes("-topmost", True)
        self.focus_force()
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.w = 180
        self.h = 80
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/10) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        '''Creates the label and close button.'''
        self.lblEpidemic = tk.Label(self, text = "The bottom card is " + initialize.Infection_Deck[len(initialize.Infection_Deck)-1]).pack(padx = 5, pady = 5)
        self.btnEpidemic = tk.Button(self, text = "OK", command = self.close).pack(padx = 5, pady = 10)

        '''Puts the bottom card od the deck in the discard pile, then shuffles the discard pile.'''
        initialize.Infection_Discard.insert(0, initialize.Infection_Deck[len(initialize.Infection_Deck)-1])
        initialize.Infection_Deck.pop(len(initialize.Infection_Deck)-1)
        random.shuffle(initialize.Infection_Discard)

        '''Puts the discard pile on top of the deck, and clears the discard.'''
        initialize.Infection_Deck = initialize.Infection_Discard + initialize.Infection_Deck
        initialize.Infection_Discard = []
            

    def close(self):
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()
        

'''This lets you see the top six cards of the deck, then lets you put them back in order'''
class Forecast(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Forecast")
        self.attributes("-topmost", True)
        self.focus_force()
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 450
        self.h = 120 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/10) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        '''Sets some variables, including button colors.'''
        self.stack = []
        self.bgColor = '#00baba'
        self.fgColor = '#ffffff'

        '''Makes the main labels.'''
        self.lblInfo = tk.Label(self, text = "Click the cities in the order you want them on the deck, top to bottom.").pack(padx = 5, pady = 5)
        self.lblCards = tk.Label(self)
        self.lblCards.pack(padx = 5, pady = 5)

        '''Frame that holds the buttons.'''
        self.frmCards = tk.Frame(self, height = 2, bd = 0, relief = 'sunken')
        self.frmCards.pack(padx = 5, pady = 10)

        '''Sets the top six cards to variables, and takes them out of the deck.'''
        self.idCard1 = initialize.Infection_Deck[0]
        initialize.Infection_Deck.pop(0)
        self.idCard2 = initialize.Infection_Deck[0]
        initialize.Infection_Deck.pop(0)
        self.idCard3 = initialize.Infection_Deck[0]
        initialize.Infection_Deck.pop(0)
        self.idCard4 = initialize.Infection_Deck[0]
        initialize.Infection_Deck.pop(0)
        self.idCard5 = initialize.Infection_Deck[0]
        initialize.Infection_Deck.pop(0)
        self.idCard6 = initialize.Infection_Deck[0]
        initialize.Infection_Deck.pop(0)
        
        '''Creates six buttons, one per card, and sets them to call a function with arguments'''
        self.btnCard1 = tk.Button(self.frmCards, text = self.idCard1, command = lambda: self.cardSet(self.idCard1, self.btnCard1))
        self.btnCard1.pack(side='left')
        self.btnCard2 = tk.Button(self.frmCards, text = self.idCard2, command = lambda: self.cardSet(self.idCard2, self.btnCard2))
        self.btnCard2.pack(side='left')
        self.btnCard3 = tk.Button(self.frmCards, text = self.idCard3, command = lambda: self.cardSet(self.idCard3, self.btnCard3))
        self.btnCard3.pack(side='left')
        self.btnCard4 = tk.Button(self.frmCards, text = self.idCard4, command = lambda: self.cardSet(self.idCard4, self.btnCard4))
        self.btnCard4.pack(side='left')
        self.btnCard5 = tk.Button(self.frmCards, text = self.idCard5, command = lambda: self.cardSet(self.idCard5, self.btnCard5))
        self.btnCard5.pack(side='left')
        self.btnCard6 = tk.Button(self.frmCards, text = self.idCard6, command = lambda: self.cardSet(self.idCard6, self.btnCard6))
        self.btnCard6.pack(side='left')

    '''This is the function powering the buttons. If the button has not been pressed, it puts that buttons card in a list
    and changes the button color. If it has, it takes that cad out of the stack and sets the color back. It then checks to
    see if all six cards are in the stack, and if so, closes the window.'''
    def cardSet(self, cardNum, cardBtn):
        if cardNum not in self.stack:
            self.stack.append(cardNum)
            cardBtn.config(bg = self.bgColor, fg = self.fgColor)
        else:
            self.stack.remove(cardNum)
            cardBtn.config(bg = 'SystemButtonFace', fg = 'SystemButtonText')
            
        self.lblCards.config(text = ', '.join(self.stack))

        if len(self.stack) == 6:
            initialize.Infection_Deck = self.stack + initialize.Infection_Deck
            main.unbind("<FocusIn>")
            main.refresh()
            self.destroy()

    '''This is called if the window is preemptively closed, and puts the cards back on the deck so they don't disappear.'''
    def on_closing(self):
        initialize.Infection_Deck = self.idCard1.split() + self.idCard2.split() + self.idCard3.split()+ self.idCard4.split() + self.idCard5.split() + self.idCard6.split() + initialize.Infection_Deck
        main.unbind("<FocusIn>")
        main.refresh()
        self.destroy()

    def alarm(self, event):
        self.focus_force()
        self.bell()

'''This allows you to remove a card from the discard pile from the game.'''
class ResPopulation(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Resilient Population")
        self.attributes("-topmost", True)
        main.bind("<FocusIn>", self.alarm)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.w = 250
        self.h = 110 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.x = (self.ws/1.3) - (self.w/2)
        self.y = (self.hs/10) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))
        
        '''Creates a label and entry box asking which card should be taken out, as well as a close button.'''
        self.lblRes = tk.Label(self, text = "Which card would you like to remove?").pack(padx = 5, pady = 5)
        self.entRes = tk.Entry(self)
        self.entRes.pack(padx = 5, pady = 5)

        self.btnRes = tk.Button(self, text = "OK", command = self.resPopClose).pack(padx = 5, pady = 10)

    '''Called when the close button is pressed, this checks if the entered card is in the discard pile.
    If so, it takes it out of the discard pile, and, as a result, out of the game. Then it closes the window.'''
    def resPopClose(self):
        if 1 <= int(self.entRes.get()) <= len(initialize.Infection_Discard):
            initialize.Infection_Discard.pop(int(self.entRes.get()) - 1)
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


'''Finally, after the windows are created, they are called here by defining them each as a variable, and calling them.
The main window does not launch until the initial one is closed.'''
initialize = Initialize()
initialize.mainloop()

main = Main()
main.mainloop()
