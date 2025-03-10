from tkinter import *
from tkinter.ttk import Combobox

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from plots import plot_signal
from signals import *


class Interface:

    def __init__(self):

        self.types_of_signal=("szum o rozkładzie jednostajnym", "szum gaussowski", "sygnał sinusoidalny",
                     "sygnał sinusoidalny wyprostowany jednopołówkowo",
                     "sygnał sinusoidalnym wyprostowany dwupołówkowo",
                     "sygnał prostokątny", "sygnał prostokątny symetryczny",
                     "sygnał trójkątny", "skok jednostkowy", "impuls jednostkowy",
                     "szum impulsowy")
        self.window = Tk()

        self.amplituda = DoubleVar()
        self.t1 = DoubleVar()
        self.t2 = DoubleVar()
        self.duration = DoubleVar()
        self.sampling = DoubleVar()

        self.amplituda2 = DoubleVar()
        self.t12 = DoubleVar()
        self.t22 = DoubleVar()
        self.duration2 = DoubleVar()
        self.sampling2 = DoubleVar()

        self.window.title("Cyfrowe przetwarzanie sygnału")
        self.lbl = Label(self.window, text="Wybierz rodzaj sygnału:")
        self.lbl.grid(column=0, row=0)
        self.choose_type = Combobox(self.window)
        self.choose_type['values'] = self.types_of_signal
        self.choose_type.current(1)
        self.choose_type.grid(column=1, row=0)

        self.parameters_text = Label(self.window, text="Parametry sygnału 1")
        self.parameters_text.grid(column=0, row=1)


        self.amplituda_label = Label(self.window, text="Amplituda:")
        self.amplituda_label.grid(column=0, row=2)
        self.amplituda_entry = Entry(self.window, textvariable=self.amplituda, font=('calibre', 10, 'normal'))
        self.amplituda_entry.grid(column=1, row=2)

        self.duration_label = Label(self.window, text="Czas trwania:")
        self.duration_label.grid(column=0, row=3)
        self.duration_entry = Entry(self.window, textvariable=self.duration, font=('calibre', 10, 'normal'))
        self.duration_entry.grid(column=1, row=3)

        self.time1_label = Label(self.window, text="Czas 1:")
        self.time1_label.grid(column=0, row=4)
        self.t1_entry = Entry(self.window, textvariable=self.t1, font=('calibre', 10, 'normal'))
        self.t1_entry.grid(column=1, row=4)

        self.time2_label = Label(self.window, text="Czas 2:")
        self.time2_label.grid(column=0, row=5)
        self.t2_entry = Entry(self.window, textvariable=self.t2, font=('calibre', 10, 'normal'))
        self.t2_entry.grid(column=1, row=5)

        self.sampling_label = Label(self.window, text="Probkowanie:")
        self.sampling_label.grid(column=0, row=6)
        self.sampling_entry = Entry(self.window, textvariable=self.sampling, font=('calibre', 10, 'normal'))
        self.sampling_entry.grid(column=1, row=6)

        plot_button = Button(master=self.window,
                             command=self.plot,
                             height=2,
                             width=10,
                             text="Create")

        plot_button.grid(column=0, row=7)

        self.lbl12 = Label(self.window, text="Parametry sygnału 2")
        self.lbl12.grid(column=0, row=8)

        self.amplituda_label2 = Label(self.window, text="Amplituda:")
        self.amplituda_label2.grid(column=0, row=9)
        self.amplituda_entry2 = Entry(self.window, textvariable=self.amplituda2, font=('calibre', 10, 'normal'))
        self.amplituda_entry2.grid(column=1, row=9)

        self.duration_label2 = Label(self.window, text="Czas trwania:")
        self.duration_label2.grid(column=0, row=10)
        self.duration_entry2 = Entry(self.window, textvariable=self.duration2, font=('calibre', 10, 'normal'))
        self.duration_entry2.grid(column=1, row=10)

        self.time1_label2 = Label(self.window, text="Czas 1:")
        self.time1_label2.grid(column=0, row=11)
        self.t1_entry2 = Entry(self.window, textvariable=self.t12, font=('calibre', 10, 'normal'))
        self.t1_entry2.grid(column=1, row=11)

        self.time2_label2 = Label(self.window, text="Czas 2:")
        self.time2_label2.grid(column=0, row=12)
        self.t2_entry2 = Entry(self.window, textvariable=self.t22, font=('calibre', 10, 'normal'))
        self.t2_entry2.grid(column=1, row=12)

        self.sampling_label2 = Label(self.window, text="Probkowanie:")
        self.sampling_label2.grid(column=0, row=13)
        self.sampling_entry2 = Entry(self.window, textvariable=self.sampling2, font=('calibre', 10, 'normal'))
        self.sampling_entry2.grid(column=1, row=13)


        plot_button = Button(master=self.window,
                             command=self.plot,
                             height=2,
                             width=10,
                             text="Create")

        plot_button.grid(column=0, row=14)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        # setting tkinter window size
        self.window.geometry("%dx%d" % (width, height))
        self.window.mainloop()

    def plot(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)
        # list of squares
        y = [i ** 2 for i in range(101)]
        # adding the subplot
        plot1 = fig.add_subplot(111)
        # plotting the graph
        plot1.plot(uniformly_distributed_noise())
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=self.window)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(column=3, row=0, rowspan=7)
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().grid(column=5, row=1)

        # the main Tkinter window










