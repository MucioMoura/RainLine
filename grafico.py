import tkinter as tk
import pymannkendall as mk
import pandas as pd
from matplotlib.figure import Figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas

import mannkendall as lclMk

trendX = lclMk.dadosFiltrados['dias']
trendY = lclMk.resultado.slope * trendX + lclMk.resultado.intercept

graf = fig(figsize=(10, 8), dpi=100)
plot = graf.add_subplot(111)


plot.plot(lclMk.dadosFiltrados['data'], lclMk.dadosFiltrados['mm'], label='Dados', color='black', lw=0.80, marker='o', ms=2)
plot.plot(lclMk.dadosFiltrados['data'], trendY, label='Tendência', color='red', marker='o')
plot.legend()
plot.grid()
plot.set_xlabel('Data')
plot.set_ylabel('mm')
#plot.set_ylim(-300, 300)

# canvasTend = figCanvas(graf, master=janMenu)
# canvasTend.draw()
# canvasTend.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)