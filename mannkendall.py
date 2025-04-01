import tkinter as tk
import pymannkendall as mk
import pandas as pd
from matplotlib.figure import Figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas


# dados = pd.read_excel(filePath, engine='openpyxl')
# dados.columns = ['data', 'mm']
# dados['data'] = pd.to_datetime(dados['data'])
# dados['dias'] = (dados['data'] - dados['data'].min()).dt.days

# def filtrarDados(tipo, filePath):
#     dados = pd.read_excel(filePath, engine='openpyxl')

#     if tipo == 'sem':
#         dadosFiltrados = dados
#     elif tipo == 'mm':
#         if checkMaior.get() == 1 and checkMenor.get() == 1:
#             dadosFiltrados = dados[dados['mm'] > entryFiltrosMmMaior.get()]
#             dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] < entryFiltrosMmMenor.get()]
#         elif checkMaior.get() == 1:
#             dadosFiltrados = dados[dados['mm'] > entryFiltrosMmMaior.get()]
#         else:
#             dadosFiltrados = dados[dados['mm'] < entryFiltrosMmMenor.get()]

#     resultado = mk.original_test(dadosFiltrados['mm'])
#     return resultado
    
        


#dadosFiltrados = dados[dados['data'].dt.year == 1961]
#dadosFiltrados = dadosFiltrados[dadosFiltrados['data'].dt.month <= 1]

#dadosFiltrados = dados[dados['mm'] < 50]

#resultado = mk.original_test(dadosFiltrados['mm'])
#print('\n\n', resultado, '\n\n\n' )

