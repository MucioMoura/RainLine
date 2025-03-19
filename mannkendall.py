import tkinter as tk
import pymannkendall as mk
import pandas as pd
from matplotlib.figure import Figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas

import main as lclMain

dados = pd.read_excel(lclMain.filePath, engine='openpyxl')
dados.columns = ['data', 'mm']
dados['data'] = pd.to_datetime(dados['data'])
dados['dias'] = (dados['data'] - dados['data'].min()).dt.days

def filtrarDados(tipo):
    if tipo == 'sem':
        dadosFiltrados = dados
    elif tipo == 'mm':
        if lclMain.checkMaior.get() == 1 and lclMain.checkMenor.get() == 1:
            dadosFiltrados = dados[dados['mm'] > lclMain.entryFiltrosMmMaior.get()]
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] < lclMain.entryFiltrosMmMenor.get()]
        elif lclMain.checkMaior.get() == 1:
            dadosFiltrados = dados[dados['mm'] > lclMain.entryFiltrosMmMaior.get()]
        else:
            dadosFiltrados = dados[dados['mm'] < lclMain.entryFiltrosMmMenor.get()]

    resultado = mk.original_test(dadosFiltrados['mm'])
    
        


#dadosFiltrados = dados[dados['data'].dt.year == 1961]
#dadosFiltrados = dadosFiltrados[dadosFiltrados['data'].dt.month <= 1]

#dadosFiltrados = dados[dados['mm'] < 50]

#resultado = mk.original_test(dadosFiltrados['mm'])
#print('\n\n', resultado, '\n\n\n' )

