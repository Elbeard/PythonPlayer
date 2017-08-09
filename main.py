import tkinter
import tkinter.filedialog
from pyglet import media
#если на компьтере отсутствуют прописанные выше библиотеки программа не заработает
#надо их подгрузить в консоли набрать pip install (<название библиотеки>)
#через переменную "createdMainWindow" можно отследить взаимодействие классов
#программа пока играет только Wav файлы для mp3 надо устанавливать системную библиотеку AVbin

class View:                                                 #класс отрисовки
    def __init__(self):
        self.createdMainWindow = tkinter.Tk()               #создаём объект окна
        self.drawWindow(self.createdMainWindow)             #запускаем рисование

    def drawWindow(self, createdMainWindow):                #рисуем окно, и его элементы
        self.createdMainWindow = createdMainWindow
        self.createdMainWindow.config(height="50", width="300")        #конфигурируем главное окно
        self.createdMainWindow.title("Питониум")
        self.createdMainWindow.resizable(False, False)
        self.frame1 = tkinter.Frame(createdMainWindow)      #делим окно на две невидимые рамки
        self.frame2 = tkinter.Frame(createdMainWindow)
        self.frame1.grid(row=0)
        self.frame2.grid(row=1)
        self.btnOpen = tkinter.Button(self.frame1, text="Open")             #рисуем кнопки
        self.btnPlay = tkinter.Button(self.frame1, text="Play/Pause")
        self.btnStop = tkinter.Button(self.frame1, text="Stop")
        self.btnOpen.grid(row=0, column=0, padx=45, pady=3)
        self.btnPlay.grid(row=0, column=1, padx=45, pady=3)
        self.btnStop.grid(row=0, column=2, padx=45, pady=3)
        self.playList = tkinter.Listbox(self.frame2, width=70, height=15, selectmode='SINGLE')
        self.playList.grid(row=0, column=0)
        self.label = tkinter.Label(self.frame2)         #метка для тестирования методов списка(listbox)
        self.label.grid(row=1, column=0)



class Controller:                                       #класс управления
    def __init__(self):
        self.view = View()                              #подключаем Viuw 
        self.player = media.Player()                    #укорачиваем вызов функции
        self.btnPlay = False                            #состояние кнопки Play/Pause
        #-----------------------обрабатываем событие нажатия на кнопки--------------------#
        self.view.btnOpen.bind("<ButtonRelease-1>", self.openFile)
        self.view.btnPlay.bind("<Button-1>", self.play)
        self.view.btnStop.bind("<Button-1>", self.stop)
        self.view.playList.bind("<Double-Button-1>", self.listBoxSelect)

    def openFile(self, event):                          #получаем адрес файла у системы
        self.files = tkinter.filedialog.askopenfilenames()       #средствами Tkinter.filedialog
        for self.file in self.files:
            self.view.playList.insert(0, self.file)

    def load(self, file):                               #загрузка файла в плеер
        self.file = file
        self.loadFile = media.load(self.file)           # !!!музыка запускается сама, надо разобраться!!!
        self.player.queue(self.loadFile)
        self.player.pause()                             # !!!тут костыль!!!

    def play(self, event):                              #собственно Play/Pause в деле
        self.btnPlay = not self.btnPlay                 #при повторном вызове если нажата отжать
        if self.btnPlay == True:
            self.player.play()
            self.view.btnPlay.config(text="Pause")
        else:
            self.player.pause()
            self.view.btnPlay.config(text="Play")

    def stop(self, event):
        self.player.delete()                            #Выгружает оз памяти песню и перестаёт её играть
        self.load(self.LBsel)                           #подгружаем обратно чтобы было что играть
                                                        #если нажмут Play
        self.btnPlay = False                            #возвращаем кнопку плей в отжатое состояние
        self.view.btnPlay.config(text="Play")           #меняем надпись на кнопке

    def listBoxSelect(self, event):                     #выбор песни из плейлиста
        self.LBsel = self.view.playList.get(self.view.playList.curselection())
        self.view.label.config(text=self.LBsel)
        self.player.delete()
        self.load(self.LBsel)
        self.player.play()
        self.btnPlay = True
        self.view.btnPlay.config(text="Pause")


controller = Controller()                               #создание экземпляра класса Controller
controller.view.createdMainWindow.mainloop()                  #запуск основного цикла программы


#!!!почитать про метод  insert!!!