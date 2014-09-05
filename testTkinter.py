from tkinter import tix, Frame, Tk, BOTH, Listbox, END, Button, messagebox
from tix import CheckList

class MainWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Batoto downloader")
        self.pack(fill=BOTH, expand=1)

        lst = ["test", "prova"]
        self.lb = tix.Listbox(self)
        for i in lst:
            self.lb.insert(END, i)

        self.lb.bind("<<ListboxSelect>>", self.onSelect)
        self.lb.place(x=10, y=50)

        btnStart = Button(self, text="Start", command=self.onBtnStartClick)
        btnStart.place(x=10, y=10)

    def onBtnStartClick(self):
        messagebox.showinfo("Batoto Downloader", self.lb.get(self.lb.curselection()))

    def onSelect(self, val):
        self.onBtnStartClick()

def main():
    root = Tk()
    root.geometry("250x250+30+30")
    win = MainWindow(root)
    root.mainloop()

main()
