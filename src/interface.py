from tkinter import *
from tkinter.ttk import Combobox

window = Tk()

window.title("Cyfrowe przetwarzanie sygnału")

lbl = Label(window, text="Wybierz rodzaj sygnału:")

lbl.grid(column=0, row=0)

combo = Combobox(window)

combo['values']= ('sinosuidalny', 'taki', 'inny', 4, 5, "Text")

combo.current(1) #set the selected item

combo.grid(column=2, row=0)

window.geometry('1280x720')
window.mainloop()


