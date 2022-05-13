import tkinter
import os
from tkinter import messagebox as mb

try:
    f = open("save.txt", 'x') #open for exclusive creation, failing if the file already exists
    hunger = 100
    happy = 100
    result = 0
except FileExistsError:
    f = open("save.txt")
    args = f.readlines()
    hunger = int(args[0])
    happy = int(args[1])
    result = str(args[2])
f.close()

pressforstart = True
feedflag = 0
playflag = 0
deathflag = 0

class CustomDialog(object):
    def __init__(self, parent, prompt="", default=""):
        self.popup = tkinter.Toplevel(parent) # окно диалога
        self.popup.title(prompt)
        self.popup.transient(parent)
        #сделать окно зависимым от другого окна, указанного в аргументе. Будет сворачиваться вместе с указанным окном.
        #Без аргументов возвращает текущее значение.

        self.var = tkinter.StringVar(value=default) # текст в окне

        label = tkinter.Label(self.popup, text=prompt)
        entry = tkinter.Entry(self.popup, textvariable=self.var) #это виджет, позволяющий пользователю ввести одну строку текста.derwidth
        buttons = tkinter.Frame(self.popup)
        
        buttons.pack(side="bottom", fill="x") #это специальный механизм, который размещает (упаковывает) виджеты на окне
        label.pack(side="top", fill="x", padx=20, pady=10)
        entry.pack(side="top", fill="x", padx=20, pady=10)

        ok = tkinter.Button(buttons, text="Ok",
                            command=self.popup.destroy) #Метод класса для закрытия окна индикатора
        ok.pack(side="top")

        self.entry = entry

    def show(self):
        #Методы  focus_ для управления фокусом ввода с клавиатуры. Виджет, имеющий фокус, получает все события с клавиатуры.
        self.entry.focus_force()
        root.wait_window(self.popup) # ожидание
        return self.var.get() # возвращает строку из StringVar


def cancel():
    answer = mb.askyesno(title="Start over",
                         message="Are you sure,that you want to start over?")
    if answer is True:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), #конкатенацию пути path и компонентов *paths.
                            'save.txt')
        os.remove(path)
        exit()


def exitgame():
    answer = mb.askyesno(title="Exit",
                         message="Are you leavig me?")
    if answer is True:
        root.quit()

def help():
    file = open('help.txt', encoding="utf8")
    mb.showinfo("Help", file.read())

def start_game(start):
    global pressforstart
    
    if pressforstart is False:
        pass
    else:
        startLabel.config(text="")
        update_hunger()
        update_happy()
        update_display()
        pressforstart = False

def update_display():
    global hunger
    global feedflag
    global playflag

    if deathflag == 1:
        Picture.config(image=death)
        Picture.after(100, update_display) #Таймер
    elif feedflag == 1:
        Picture.config(image=Eating)
    elif playflag == 1:
        Picture.config(image=playing)
    else:
        if hunger >= 80 and happy >= 70:
            Picture.config(image=happyphoto)
        elif hunger >= 50 and happy >= 50:
            Picture.config(image=normalphoto)
        elif hunger < 50:
            Picture.config(image=Hungry)
        elif happy < 50:
            Picture.config(image=sad)

    hungerLabel.config(text="I'm full " + str(hunger) + " %")
    happyLabel.config(text="Happines: " + str(happy) + " %")

    if feedflag == 1:
        Picture.after(1000, update_display)
        feedflag = 0
    elif playflag == 1:
        Picture.after(1000, update_display)
        playflag = 0
    else:
        Picture.after(300, update_display)


def update_hunger():
    global hunger
    if hunger > 0:
        hunger -= 1
    if is_alive():
        hungerLabel.after(1000, update_hunger)

def update_happy():

    global happy

    if happy > 0:
        happy -= 1

    if is_alive():
        happyLabel.after(1000, update_happy)

def feed():
    global hunger
    global feedflag

    feedflag = 1

    if is_alive():
        global hunger
        if hunger <= 93:
            hunger += 7

def play():
    global happy
    global playflag

    if is_alive():
        if happy <= 90:
            happy += 10

    playflag = 1

def is_alive():
    global hunger
    global deathflag

    if hunger <= 0:
        deathflag = 1
        startLabel.config(text=(str(result).title()) + " Dead,noooo")
        return False
    else:
        return True


root = tkinter.Tk()
root.title("My petty-pretty")
root.geometry("800x800")

startLabel = tkinter.Label(root, text="Click enter;)",
                           font=('Times New Roman', 20))
startLabel.pack()

hungerLabel = tkinter.Label(root, text="I'm full "
                                       + str(hunger) + " %",
                            font=('Times New Roman', 25))
hungerLabel.pack()

happyLabel = tkinter.Label(root, text="Happines: "
                                      + str(happy) + " %",
                           font=('Times New Roman', 25))
happyLabel.pack()

happyphoto = tkinter.PhotoImage(file="Happy.png")
normalphoto = tkinter.PhotoImage(file="NORM.png")
sad = tkinter.PhotoImage(file="SAD.png")
Hungry = tkinter.PhotoImage(file="Hungry.png")
Eating = tkinter.PhotoImage(file="Eating.png")
playing = tkinter.PhotoImage(file="playing.png")
death = tkinter.PhotoImage(file="DEAD.png")

Picture = tkinter.Label(root, image=normalphoto)
Picture.pack()

btnFeed = tkinter.Button(root, text="Feed me!", command=feed,
                         font=('Times New Roman', 20))
btnFeed.place(x=10, y=250)

btnPlay = tkinter.Button(root, text="Play with me!",
                         command=play, font=('Times New Roman', 20))
btnPlay.place(x=10, y=450)

mainmenu = tkinter.Menu(root)
root.config(menu=mainmenu)

filemenu = tkinter.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Cancel all and start again",
                     command=cancel)
filemenu.add_command(label="Exit (autosave,of course)",
                     command=exitgame)

helpmenu = tkinter.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Help", command=help)
#добавляет элемент меню, который в свою очередь может представлять подменю
mainmenu.add_cascade(label="Menu", menu=filemenu)
mainmenu.add_cascade(label=" Inquiries", menu=helpmenu)

if result == 0:
    dialog = CustomDialog(root, prompt="What's my name?")
    result = dialog.show()


nameLabel = tkinter.Label(root, text="My name is " + str(result),
                          font=('Times New Roman', 25))
nameLabel.pack()

root.bind('<Return>', start_game)
root.mainloop()

f = open("save.txt", 'w')
args = [hunger, happy, result]
f.writelines("%s\n" % i for i in args)
f.close()
