# Name: Shamita Goyal
# Lab 2: Data Analysis / Visualization, GUI

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as tkmb
from rainfall import Rainfall

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Main Window setup
        self.geometry("500x350+3+6")
        self.title("Rainfall")
        self.configure(bg="aquamarine4")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # label1 description --> SF Rainfall 1850-2023
        label1 = tk.Label(text="SF Rainfall 1850-2023",fg="LightGoldenrodYellow", font=("Courier", 35, "bold"), bg="aquamarine4")
        label1.grid(sticky="n", pady=10)


        # Button Frame for the 3 buttons
        button_frame = tk.Frame(bg="aquamarine4")
        button_frame.grid(row=0, column=0, columnspan=3, sticky=tk.EW)
        button_frame.columnconfigure(1, weight=1)

        # Make the 3 Buttons --> Monthly Average, Monthly Range, Yearly Total
        button1 = tk.Button(button_frame, text="Monthly Average", command=self.monthAvg, highlightbackground="aquamarine4")
        button2 = tk.Button(button_frame,text="Monthly Range", command=self.monthRange, highlightbackground="aquamarine4")
        button3 = tk.Button(button_frame, text="Yearly Total", command=self.openDialogWin, highlightbackground="aquamarine4")

        # Show the 3 buttons in main window
        button1.grid(row=0, column=0, pady=3, padx=3, sticky="w")
        button2.grid(row=0, column=1, pady=3, padx=3)
        button3.grid(row=0, column=2, pady=3, padx=3, sticky="e")

        # Make the 3 stats labels --> Highest, Lowest, Median yearly rainfall
        year, inches = r.get_highestR
        H1 = tk.Label(self, text=f'Highest yearly rainfall: {year}, {inches:.2f} inches', font=("Inter", 17), fg="LightGoldenrodYellow", bg="aquamarine4")

        year, inches = r.get_lowestR
        H2 = tk.Label(self, text=f'Lowest yearly rainfall: {year}, {inches:.2f} inches', font=("Inter", 17), fg="LightGoldenrodYellow", bg="aquamarine4")

        inches = r.get_medianR
        H3 = tk.Label(self, text=f'Median yearly rainfall: {inches:.2f} inches', font=("Inter", 17), fg="LightGoldenrodYellow", bg="aquamarine4")

        # Show the 3 stats in main window
        H1.grid(pady=3, padx=3)
        H2.grid(pady=3, padx=3)
        H3.grid(pady=3, padx=3)
    def monthAvg(self):
        """
        - method is triggered when user presses button1 --> Monthly Average
        - monthlyDist method from Rainfall class is stored in method
        - object is instantiated, PlotWindow class passes the method to plot graph
        """
        method = r.monthlyDist
        self.toplevel = PlotWindow(self, method)


    def monthRange(self):
        """
        - method is triggered when user presses button2 --> Monthly Range
        - avgMonthly method from the Rainfall class is stored in method
        - object is instantiated, PlotWindow class passes the method to plot graph
        """
        method = r.avgMonthly
        self.toplevel = PlotWindow(self, method)

    def openDialogWin(self):
        """
        - method is triggered when user presses button3 --> Yearly Total
        - main window withdraws from the screen temporarily
        - object is instantiated, DialogWindow class will pop up a new window
        """
        self.withdraw()
        dialogWin = DialogWindow(self)

    def yearlyTotal(self, start, end):
        """
        - method is triggered through DialogWindow
        - needs start and end parameters which are the years to plot graph
        -  yearlyR method from the Rainfall class is stored in method
        - object is instantiated, PlotWindow class passes the method to plot graph
        """
        self.start = start
        self.end = end
        method = r.yearlyR
        self.toplevel = PlotWindow(self, method)


class PlotWindow(tk.Toplevel):
    """plots the graphs for the 3 options of rainfall from the MainWindow"""
    def __init__(self, master, method):
        super().__init__(master)

        # checking which method needs two parameters
        self.plotMethod = method
        if self.plotMethod == r.yearlyR:
            self.plotMethod(master.start, master.end)
        else:
            self.plotMethod()

        canvas = FigureCanvasTkAgg(r.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class DialogWindow(tk.Toplevel):
    """window is created by the MainWindow when the user selects the ‘Yearly Total’ button"""
    def __init__(self, master):
        super().__init__(master)

        # Dialog Window setup
        self.geometry("500x350+3+6")
        self.configure(bg="aquamarine4")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # widget entry type --> string
        self.yearInt = tk.StringVar()

        def callPlot(event):
            """
            - checks if the years inputted are valid
            - if valid --> calls MainWindow which will call PlotWindow to graph plot
            - if not valid --> error message box pops up and calls the windows to graph a default plot
            """

            start, end = self.yearInt.get().split()
            lowY, highY = r.get_lowY_highY

            try:
                start = int(start)
                end = int(end)
                if len(str(start)) != 4 or len(str(end)) != 4:
                    raise ValueError("Start and end years must be four digits long")
                if not start < end:
                    raise ValueError(f"Start year has to be less than end year.")
                if not (lowY <= start <= highY and lowY <= end <= highY):
                    raise ValueError(f"Year must be in the range {lowY}-{highY}")
            except ValueError:
                start, end = int(lowY), int(highY)
                tkmb.showerror("Error", f"Invalid years, using {start} {end}", parent= master)

            master.yearlyTotal(start, end)
            self.entry.delete(0, tk.END)

        label3 = tk.Label(self, text="Enter the range of years, format: Start End",fg="LightGoldenrodYellow", font=("Courier", 18, "bold"), bg="aquamarine4")
        label4 = tk.Label(self, text="example: 1878 2004",fg="LightGoldenrod1", font=("Inter", 14), bg="aquamarine4")

        label3.grid()
        label4.grid()

        # entry widget
        self.entry = tk.Entry(self, textvariable=self.yearInt)
        self.entry.grid(pady=110)
        self.entry.bind("<Return>", callPlot)

    def on_close(self):
        """closes dialog window and makes the main window reappear"""
        self.destroy()
        self.master.deiconify()


# checks if file is found when instantiating object from Rainfall class
# error message pop up if file is not found
try:
    r = Rainfall()
except FileNotFoundError as e:
    tkmb.showerror("Error", f"File: {e}")
    raise SystemExit

app = MainWindow()
app.mainloop()

