from tkinter import *
from tkinter import messagebox
from random import randint

class setupwindow():
    def __init__(window): #window is the master object of the setup window
        window.root = Tk()
        window.root.title("Setup")
        window.root.grid()

        window.finish = "N"

        labels = ["Height:    ", "Width:    ", "Mines:    "]
        window.label = ["","",""]
        window.entry = ["","",""]
        
        for i in range(3):
            window.label[i] = Label(text = labels[i])
            window.label[i].grid(row = i, column = 1)
            window.entry[i] = Entry()
            window.entry[i].grid(row = i, column = 2)

        window.AImode = IntVar()
        window.ai = Checkbutton(text = "AI mode", variable = window.AImode, command = lambda: setupwindow.addentry(window)).grid(row = 3, column = 2)

        window.startbutton = Button(text = "Start", command = lambda: setupwindow.onclick(window))
        window.startbutton.grid(row = 5, column = 2)
        window.root.mainloop()

    def addentry(window):
        checkstate = window.AImode.get()
        if checkstate == 1:
            window.entry.append("")
            window.AIlabel = Label(text = "AI speed:")
            window.AIlabel.grid(row = 4, column = 1)
            window.entry[3] = Entry()
            window.entry[3].grid(row = 4, column = 2)
        else:
            window.AIlabel.destroy()
            window.entry[3].destroy()
            del window.entry[3]

    def onclick(window):
        setupwindow.verification(window)
        if window.verf == "Y":
            window.finish = "Y"
            window.root.destroy()
            return window

    def verification(window):
        height = window.entry[0].get()
        width = window.entry[1].get()
        mines = window.entry[2].get()

        window.verf = "N"
        if height.isdigit() and width.isdigit() and mines.isdigit():
            height = int(height)
            width = int(width)
            mines = int(mines)

            if height > 0 and height <= 24:
                totalsquares = height * width

                if width > 0 and width <= 48:

                    if mines > 0:
                        if mines < totalsquares:

                            window.verf = "Y"
                            window.height = height
                            window.width = width
                            window.mines = mines
                            window.delay = "None"

                            if len(window.entry) == 4:
                                delay = window.entry[3].get()
                                try:
                                    delay = float(delay)
                                    delaytemp = int(float(delay) * 1000)
                                    window.delay = delaytemp
                                    
                                except ValueError:
                                    messagebox.showerror("Invalid", "AI delay must be a decimal or whole number!")
                                    window.verf = "N"

                        else:
                            messagebox.showerror("Invalid", "You cannot have more mines than squares!")
                    else:
                        messagebox.showerror("Invalid", "You can't play minesweeper without mines!")
                else:
                    messagebox.showerror("Invalid", "Width must be between 1 and 48 inclusive!")
            else:
                messagebox.showerror("Invalid", "Height must be between 1 and 24 inclusive!")
        else:
            messagebox.showerror("Invalid", "All values must be integers!")


class gamewindow():
    def __init__(s, setup):  #s is the master object of the main game
        s.height = setup.height
        s.width = setup.width
        s.mines = setup.mines
        s.delay = setup.delay
        
        s.root = Tk()
        s.root.title("Minesweeper")
        s.root.grid()

        s.finish = "N"
        s.maingrid = list()
        for i in range(s.height):
            s.maingrid.append([])
            for x in range(s.width):
                s.maingrid[i].append(" ")
                s.maingrid[i][x] = Button(height = 0, width = 3, font = "Calibri 15 bold", text = "", bg = "gray90", command = lambda i=i, x=x: gamewindow.onclick(s, i, x))

                s.maingrid[i][x].bind("<Button-3>", lambda event="<Button-3>", i=i, x=x: gamewindow.rightclick(event, s, i, x))
                s.maingrid[i][x].grid(row = i, column = x)
                s.maingrid[i][x].mine = "False"

        totalsquares = s.height * s.width
        s.scoreneeded = totalsquares - s.mines
        s.score = 0
        
        tempindexlist = list(range(totalsquares))

        s.indexlist = list(range(totalsquares))
        
        spaceschosen = list() #where the mines are going to be
        for i in range(s.mines):
            chosenspace = randint(0, len(tempindexlist) - 1)
            spaceschosen.append(tempindexlist[chosenspace])
            del tempindexlist[chosenspace]
        
        for i in range(len(spaceschosen)):
            xvalue = int(spaceschosen[i] % s.width)
            ivalue = int(spaceschosen[i] / s.width)

            s.maingrid[ivalue][xvalue].mine = "True"

        if s.delay != "None":
            gamewindow.AI(s)
        
        s.root.mainloop()


    def onclick(s, i, x):
        colourlist = ["PlaceHolder", "Blue", "Green", "Red", "Purple", "Brown", "Turquoise3", "Black", "Gray"]

        if s.maingrid[i][x]["text"] != "F" and s.maingrid[i][x]["relief"] != "sunken":
            if s.maingrid[i][x].mine == "False":
                s.score += 1

                indexvalue = s.width * i
                indexvalue += x
                
                s.indexlist.remove(indexvalue)

                s.combinationsi = [1, -1, 0, 0, 1, 1, -1, -1]
                s.combinationsx = [0, 0, 1, -1, 1, -1, 1, -1] #All the surrounding spaces

                minecount = 0
                for combinations in range(8):
                    tempi = i + s.combinationsi[combinations]
                    tempx = x + s.combinationsx[combinations]

                    if tempi < s.height and tempx < s.width and tempi >= 0 and tempx >= 0:
                        if s.maingrid[tempi][tempx].mine == "True":
                            minecount = minecount + 1

                if minecount == 0:
                    minecount = ""

                s.maingrid[i][x].configure(text = minecount, relief = "sunken", bg = "gray85")

                if str(minecount).isdigit():
                    s.maingrid[i][x].configure(fg = colourlist[minecount])
                
                if minecount == "":
                    for z in range(8):
                        if s.finish == "N":
                            ivalue = i + int(s.combinationsi[z])
                            xvalue = x + int(s.combinationsx[z])

                            if ivalue >= 0 and ivalue < s.height and xvalue >=0 and xvalue < s.width:
                                if s.maingrid[ivalue][xvalue]["relief"] != "sunken":
                                    gamewindow.onclick(s, ivalue, xvalue)

                if s.score == s.scoreneeded and s.finish == "N":
                    messagebox.showinfo("Congratulations", "A winner is you!")
                    s.finish = "Y"
                    s.root.destroy()

                
            else:
                s.maingrid[i][x].configure(bg = "Red", text = "*")
                for a in range(len(s.maingrid)):
                    for b in range(len(s.maingrid[a])):
                        if s.maingrid[a][b].mine == "True":
                            if s.maingrid[a][b]["text"] == "F":
                                s.maingrid[a][b].configure(bg = "Green")
                            elif s.maingrid[a][b]["bg"] != "Red":
                                s.maingrid[a][b].configure(bg = "Pink", text = "*")

                        elif s.maingrid[a][b]["text"] == "F":
                            s.maingrid[a][b].configure(bg = "Yellow")
                            
                messagebox.showinfo("GAME OVER", "You have lost")
                s.root.destroy()

    def AI(s):
        found = "N"
        for i in range(len(s.maingrid)):
            for x in range(len(s.maingrid[i])):
                if found == "N":
                    if str(s.maingrid[i][x]["text"]).isdigit():

                        flagcount = 0
                        spaceschecked = list()
                        for combinations in range(8):
                            tempi = i + s.combinationsi[combinations]
                            tempx = x + s.combinationsx[combinations]
                            if tempi < s.height and tempx < s.width and tempi >= 0 and tempx >= 0:
                                if s.maingrid[tempi][tempx]["relief"] != "sunken":
                                    if s.maingrid[tempi][tempx]["text"] == "F":
                                        flagcount += 1
                                    elif s.maingrid[tempi][tempx]["text"] == "":
                                        spaceschecked.append([tempi, tempx])

                        for index in range(len(spaceschecked)):
                            ivalue = spaceschecked[index][0]
                            xvalue = spaceschecked[index][1]

                            if flagcount == s.maingrid[i][x]["text"]:
                                found = "Y"
                                gamewindow.onclick(s, ivalue, xvalue)
                                
                            elif len(spaceschecked) + flagcount == s.maingrid[i][x]["text"]:
                                found = "Y"
                                event = "<Button-3>"
                                indexvalue = ivalue * s.width
                                indexvalue += xvalue
                                s.indexlist.remove(indexvalue)
                                gamewindow.rightclick(event, s, ivalue, xvalue)

        if found == "N":
            guess = randint(0, len(s.indexlist) - 1)
            
            ivalue = int(s.indexlist[guess] / s.width)
            xvalue = int(s.indexlist[guess] % s.width)
            
            gamewindow.onclick(s, ivalue, xvalue)

        s.root.after(int(s.delay), gamewindow.AI, s)

        
                    

    def rightclick(event, s, i, x):
        if s.maingrid[i][x]["relief"] != "sunken":
            if s.maingrid[i][x]["text"] == "":
                s.maingrid[i][x].config(text = "F")
            elif s.maingrid[i][x]["text"] == "F":
                s.maingrid[i][x].config(text = "?")
            else:
                s.maingrid[i][x].config(text = "")

if __name__ == "__main__":
    setup = setupwindow()
    if setup.finish == "Y":
        game = gamewindow(setup)
    quit()


