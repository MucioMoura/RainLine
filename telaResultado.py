import tkinter as tk
import pymannkendall as mk
import pandas as pd
from matplotlib.figure import Figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas

import mannkendall as lclMk

janResult = tk.Tk()
janResult.title('Resultado')
janResult.geometry('720x540')
janResult.configure(bg='#120702')
janResult.minsize(540, 380)



janResult.mainloop()