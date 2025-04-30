import tkinter as tk
import tkinter.messagebox as mb
import pymannkendall as mk
import pandas as pd
from matplotlib.figure import Figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas
import matplotlib.dates as mdates


# VERSÃO -----------------------------------------------------------------
version = 'v0.0.0-proto'

# Local do arquivo de dados ----------------------------------------------
filePath = 'dados/dados.xlsx'
# Carregar dados
try:
    global multiSheet
    teste = pd.ExcelFile(filePath, engine='openpyxl')

    planNome = pd.ExcelFile(filePath).sheet_names
    planNum = len(planNome)
    if planNum > 1:
        multiSheet = True

    fileVer = True
    teste = None
except:
    fileVer = False
    multiSheet = False

def escolhaFiltro(tipo):
    global dados
    if multiSheet:
        dados = pd.read_excel(filePath, sheet_name=planSelected.get(), engine='openpyxl')
    else:
        dados = pd.read_excel(filePath, engine='openpyxl')
    dados.columns = ['data', 'mm']
    dados['data'] = pd.to_datetime(dados['data'])
    dados['dias'] = (dados['data'] - dados['data'].min()).dt.days
    dados['anos'] = dados['data'].dt.year

    filtro = tipo
    if filtro == 'sem':
        filtrarDados(filtro)
    else:
        definirFiltros(filtro)


def definirFiltros(filtro):

    global janFiltros
    janFiltros = tk.Toplevel()
    janFiltros.geometry('360x220')
    janFiltros.configure(bg='#120702')
    janFiltros.maxsize(360, 220)
    janFiltros.minsize(360, 220)

    if filtro == 'mm':
        global entryFiltrosMmMaior, entryFiltrosMmMenor

        janFiltros.title('Filtro de milímetros')
        mmMax = dados['mm'].max()
        mmMin = dados['mm'].min()

        txtFiltrosMm = tk.Label(janFiltros, text='De ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosMm.grid(row=0, column=0, padx=(40,0), pady=(40,0))
        entryFiltrosMmMaior = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=5)
        entryFiltrosMmMaior.grid(row=0, column=1, padx=0, pady=(40,0))
        
        txtFiltrosMm2 = tk.Label(janFiltros, text='Até ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosMm2.grid(row=1, column=0, padx=(40,0))
        entryFiltrosMmMenor = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=5)
        entryFiltrosMmMenor.grid(row=1, column=1, padx=0)

        txtFiltrosMm3 = tk.Label(janFiltros, text=f'Valores entre {mmMin} e {mmMax}', bg='#120702', fg='#E1F4E3', font=('Arial', 8, 'italic underline'))
        txtFiltrosMm3.grid(row=2, column=0, padx=(80,0), pady=(0,0))

        btFiltrosMm = tk.Button(janFiltros, text='Aplicar', bg='#FF6219', fg='#120702', font=('Arial', 16), width=10, height=1, activebackground='#89D28F', border=0, command=lambda:filtrarDados(filtro))
        btFiltrosMm.grid(row=3, column=0, columnspan=3, padx=(200,0), pady=(20,0))
    elif filtro == 'data':
        global entryFiltrosDataIni, entryFiltrosDataFim

        janFiltros.title('Filtro de data')
        anosMax = dados['anos'].max()
        anosMin = dados['anos'].min()

        txtFiltrosData = tk.Label(janFiltros, text='Ano inicial ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosData.grid(row=0, column=0, padx=(40,0), pady=(40,0))
        entryFiltrosDataIni = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=10)
        entryFiltrosDataIni.grid(row=0, column=1, padx=0, pady=(40,0))

        txtFiltrosData2 = tk.Label(janFiltros, text='Ano final ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosData2.grid(row=1, column=0, padx=(40,0))
        entryFiltrosDataFim = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=10)
        entryFiltrosDataFim.grid(row=1, column=1, padx=0)

        txtFiltrosData3 = tk.Label(janFiltros, text=f'Valores entre {anosMin} e {anosMax}', bg='#120702', fg='#E1F4E3', font=('Arial', 8, 'italic underline'))
        txtFiltrosData3.grid(row=2, column=0, padx=(80,0), pady=(0,0))

        btFiltrosData = tk.Button(janFiltros, text='Aplicar', bg='#FF6219', fg='#120702', font=('Arial', 16), width=10, height=1, activebackground='#89D28F', border=0, command=lambda:filtrarDados(filtro))
        btFiltrosData.grid(row=3, column=0, columnspan=3, padx=(200,0), pady=(20,0))
    elif filtro == 'ambos':
        def continuarAmbos(entryFiltrosDataIni, entryFiltrosDataFim):
            dataIni = entryFiltrosDataIni.get()
            dataFim = entryFiltrosDataFim.get()
            if dataIni == '' and dataFim == '':
                mb.showerror('Nenhum filtro aplicado!', message='Insira pelo menos um filtro.\nPara utilização sem filtros, clique no botão "Sem filtros" no menu principal.')
                return
            elif dataIni == '':
                aux = dados[dados['data'].dt.year <= int(dataFim)]
            elif dataFim == '':
                aux = dados[dados['data'].dt.year >= int(dataIni)]
            else:
                if dataIni > dataFim:
                    mb.showerror('Erro!', message='Ano inicial maior que ano final.')
                    return
                aux = dados[dados['data'].dt.year >= int(dataIni)]
                aux = aux[aux['data'].dt.year <= int(dataFim)]

            mmMax = aux['mm'].max()
            mmMin = aux['mm'].min()
            aux = None
            txtFiltrosMm.config(fg='#E1F4E3')
            entryFiltrosMmMaior.config(state='normal')
            txtFiltrosMm2.config(fg='#E1F4E3')
            entryFiltrosMmMenor.config(state='normal')
            txtFiltrosMm3.config(text=f'Valores entre {mmMin} e {mmMax}', fg='#E1F4E3')
            btFiltrosMm.config(state='normal')


        janFiltros.title('Filtro de data e milímetros')
        janFiltros.geometry('360x360')
        janFiltros.maxsize(360, 360)
        janFiltros.minsize(360, 360)
        anosMax = dados['anos'].max()
        anosMin = dados['anos'].min()

        txtFiltrosData = tk.Label(janFiltros, text='Ano inicial ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosData.grid(row=0, column=0, padx=(40,0), pady=(40,0))
        entryFiltrosDataIni = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=10)
        entryFiltrosDataIni.grid(row=0, column=1, padx=0, pady=(40,0))

        txtFiltrosData2 = tk.Label(janFiltros, text='Ano final ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosData2.grid(row=1, column=0, padx=(40,0))
        entryFiltrosDataFim = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=10)
        entryFiltrosDataFim.grid(row=1, column=1, padx=0)

        txtFiltrosData3 = tk.Label(janFiltros, text=f'Valores entre {anosMin} e {anosMax}', bg='#120702', fg='#E1F4E3', font=('Arial', 8, 'italic underline'))
        txtFiltrosData3.grid(row=2, column=0, padx=(80,0), pady=(0,0))

        btFiltrosData = tk.Button(janFiltros, text='Continuar...', bg='#FF6219', fg='#120702', font=('Arial', 16), width=10, height=1, activebackground='#89D28F', border=0, command=lambda:continuarAmbos(entryFiltrosDataIni, entryFiltrosDataFim))
        btFiltrosData.grid(row=3, column=0, columnspan=3, padx=(200,0), pady=(20,0))

        ###

        txtFiltrosMm = tk.Label(janFiltros, text='De ', bg='#120702', fg='#6d6d6d', font=('Arial', 16))
        txtFiltrosMm.grid(row=4, column=0, padx=(40,0), pady=(10,0))
        entryFiltrosMmMaior = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=5, state='disabled')
        entryFiltrosMmMaior.grid(row=4, column=1, padx=0, pady=(10,0))
        
        txtFiltrosMm2 = tk.Label(janFiltros, text='Até ', bg='#120702', fg='#6d6d6d', font=('Arial', 16))
        txtFiltrosMm2.grid(row=5, column=0, padx=(40,0))
        entryFiltrosMmMenor = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=5, state='disabled')
        entryFiltrosMmMenor.grid(row=5, column=1, padx=0)

        txtFiltrosMm3 = tk.Label(janFiltros, text=f'Aguardando...', bg='#120702', fg='#6d6d6d', font=('Arial', 8, 'italic underline'))
        txtFiltrosMm3.grid(row=6, column=0, padx=(80,0), pady=(0,0))

        btFiltrosMm = tk.Button(janFiltros, text='Aplicar', bg='#FF6219', fg='#120702', font=('Arial', 16), width=10, height=1, activebackground='#89D28F', border=0, command=lambda:filtrarDados(filtro), state='disabled')
        btFiltrosMm.grid(row=7, column=0, columnspan=3, padx=(200,0), pady=(20,0))


def filtrarDados(filtro):
    global dadosFiltrados, resultado

    if filtro == 'sem': ######################################################
        dadosFiltrados = dados
    elif filtro == 'mm': ######################################################
        mmMaior = entryFiltrosMmMaior.get()
        mmMenor = entryFiltrosMmMenor.get()
        if mmMaior == '' and mmMenor == '':
            mb.showerror('Nenhum filtro aplicado!', message='Insira pelo menos um filtro.\nPara utilização sem filtros, clique no botão "Sem filtros" no menu principal.')
            janFiltros.destroy()
            return
        elif mmMenor == '':
            dadosFiltrados = dados[dados['mm'] > float(mmMaior)]
        elif mmMaior == '':
            dadosFiltrados = dados[dados['mm'] < float(mmMenor)]
        else:
            if float(mmMaior) > float(mmMenor):
                mb.showerror('Erro!', message='Valor inicial é maior que o valor final.')
                janFiltros.destroy()
                return
            dadosFiltrados = dados[dados['mm'] > float(mmMaior)]
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] < float(mmMenor)]
    elif filtro == 'data': ######################################################
        dataIni = entryFiltrosDataIni.get()
        dataFim = entryFiltrosDataFim.get()
        if dataIni == '' and dataFim == '':
            mb.showerror('Nenhum filtro aplicado!', message='Insira pelo menos um filtro.\nPara utilização sem filtros, clique no botão "Sem filtros" no menu principal.')
            janFiltros.destroy()
            return
        elif dataIni == '':
            dadosFiltrados = dados[dados['data'].dt.year <= int(dataFim)]
        elif dataFim == '':
            dadosFiltrados = dados[dados['data'].dt.year >= int(dataIni)]
        else:
            if dataIni > dataFim:
                mb.showerror('Erro!', message='Ano inicial maior que ano final.')
                janFiltros.destroy()
                return
            dadosFiltrados = dados[dados['data'].dt.year >= int(dataIni)]
            dadosFiltrados = dadosFiltrados[dadosFiltrados['data'].dt.year <= int(dataFim)]
    elif filtro == 'ambos': ######################################################
        dataIni = entryFiltrosDataIni.get()
        dataFim = entryFiltrosDataFim.get()
        mmMaior = entryFiltrosMmMaior.get()
        mmMenor = entryFiltrosMmMenor.get()
        if mmMaior == '' and mmMenor == '':
            mb.showerror('Nenhum filtro aplicado!', message='Insira pelo menos um filtro.\nPara utilização sem filtros, clique no botão "Sem filtros" no menu principal.')
            janFiltros.destroy()
            return
        
        if dataIni == '':
            print('-- 1 --')
            dadosFiltrados = dados[dados['data'].dt.year <= int(dataFim)]
        elif dataFim == '':
            print('-- 2 --')
            dadosFiltrados = dados[dados['data'].dt.year >= int(dataIni)]
        else:
            print('-- 3 --')
            if dataIni > dataFim:
                mb.showerror('Erro!', message='Ano inicial maior que ano final.')
                janFiltros.destroy()
                return
            dadosFiltrados = dados[dados['data'].dt.year >= int(dataIni)]
            dadosFiltrados = dadosFiltrados[dadosFiltrados['data'].dt.year <= int(dataFim)]

        if mmMaior == '' and mmMenor == '':
            mb.showerror('Nenhum filtro aplicado!', message='Insira pelo menos um filtro.\nPara utilização sem filtros, clique no botão "Sem filtros" no menu principal.')
            janFiltros.destroy()
            return
        elif mmMenor == '':
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] > float(mmMaior)]
        elif mmMaior == '':
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] < float(mmMenor)]
        else:
            if float(mmMaior) > float(mmMenor):
                mb.showerror('Erro!', message='Valor inicial é maior que o valor final.')
                janFiltros.destroy()
                return
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] > float(mmMaior)]
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] < float(mmMenor)]
            

    resultado = mk.original_test(dadosFiltrados['mm'])
    telaResultado(filtro)

def telaResultado(filtro):
    janResult = tk.Toplevel()
    janResult.title('Resultado')
    janResult.geometry('720x540')
    janResult.configure(bg='#120702')
    janResult.minsize(720, 540)
    janResult.state('zoomed')

    #grafico
    dadosFiltrados['t'] = dadosFiltrados['dias'] / 365.25
    trendX = dadosFiltrados['t']
    trendY = resultado.slope * trendX + resultado.intercept
    graf = fig(figsize=(10, 6), dpi=100)
    plot = graf.add_subplot(111)
    plot.plot(dadosFiltrados['data'], dadosFiltrados['mm'], label='Dados', color='blue', lw=0.80, marker='o', ms=2, alpha=0.5)
    plot.plot(dadosFiltrados['data'], trendY, label='Tendência', color='red')
    plot.legend()
    plot.grid()
    plot.set_xlabel('Data')
    plot.set_ylabel('mm')

    frameResultL = tk.Frame(janResult, bg='#120702')
    frameResultR = tk.Frame(janResult, bg='#120702')
    frameResultL.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    frameResultR.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    canvasTend = figCanvas(graf, master=frameResultR)
    canvasTend.draw()
    canvasTend.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    # Informações
    try:
        mmMaior = float(entryFiltrosMmMaior.get())
    except:
        mmMaior = 0
    try:
        mmMenor = float(entryFiltrosMmMenor.get())
    except:
        mmMenor = 0
    anosMax = dadosFiltrados['anos'].max()
    anosMin = dadosFiltrados['anos'].min()
    mmMax = dadosFiltrados['mm'].max()
    mmMin = dadosFiltrados['mm'].min()
    qtdDados = len(dadosFiltrados['mm'])

    txtInfo = tk.Label(frameResultL, text=f'Dados de {anosMin} a {anosMax}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo.grid(row=0, column=0, padx=(5), pady=(8), sticky='nw')
    txtInfo2 = tk.Label(frameResultL, text='Filtros:', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo2.grid(row=1, column=0, padx=(5), pady=(8,0), sticky='nw')
    txtInfo3 = tk.Label(frameResultL, text='-> Milímetros | Não aplicado.', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo3.grid(row=2, column=0, padx=(5), pady=(0), sticky='nw')
    txtInfo4 = tk.Label(frameResultL, text='-> Data | Não aplicado.', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo4.grid(row=3, column=0, padx=(5), pady=(0,8), sticky='nw')
    
    if filtro == 'sem':
        txtInfo3.config(text='-> Milímetros | Não aplicado.')
        txtInfo4.config(text='-> Data | Não aplicado.')
    elif filtro == 'mm':
        if mmMaior != 0 and mmMenor != 0:
            txtInfo3.config(text=f'-> Milímetros | De {mmMaior} até {mmMenor}')
        elif mmMaior != 0:
            txtInfo3.config(text=f'-> Milímetros | A partir de {mmMaior}')
        else:
            txtInfo3.config(text=f'-> Milímetros | Até {mmMenor}')
    elif filtro == 'data':
        dataIni = entryFiltrosDataIni.get()
        dataFim = entryFiltrosDataFim.get()

        if dataIni != '' and dataFim != '':
            txtInfo4.config(text=f'-> Data | De {dataIni} a {dataFim}')
        elif dataIni != '':
            txtInfo4.config(text=f'-> Data | A partir de {dataIni}')
        else:
            txtInfo4.config(text=f'-> Data | Até {dataFim}')
    elif filtro == 'ambos':
        if mmMaior != 0 and mmMenor != 0:
            txtInfo3.config(text=f'-> Milímetros | De {mmMaior} até {mmMenor}')
        elif mmMaior != 0:
            txtInfo3.config(text=f'-> Milímetros | A partir de {mmMaior}')
        else:
            txtInfo3.config(text=f'-> Milímetros | Até {mmMenor}')

        dataIni = entryFiltrosDataIni.get()
        dataFim = entryFiltrosDataFim.get()

        if dataIni != '' and dataFim != '':
            txtInfo4.config(text=f'-> Data | De {dataIni} a {dataFim}')
        elif dataIni != '':
            txtInfo4.config(text=f'-> Data | A partir de {dataIni}')
        else:
            txtInfo4.config(text=f'-> Data | Até {dataFim}')

    txtInfo5 = tk.Label(frameResultL, text=f'Maior mm = {mmMax}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo5.grid(row=4, column=0, padx=(5), pady=(8,0), sticky='nw')
    txtInfo6 = tk.Label(frameResultL, text=f'Menor mm = {mmMin}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo6.grid(row=5, column=0, padx=(5), pady=(0,8), sticky='nw')
    txtInfo7 = tk.Label(frameResultL, text=f'Quantidade de dados = {qtdDados}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo7.grid(row=6, column=0, padx=(5), pady=(8,100), sticky='nw')

    txtInfo8 = tk.Label(frameResultL, text='Resultado do Mann Kendall:', bg='#120702', fg='#E1F4E3', font=('Arial', 24, 'underline'))
    txtInfo8.grid(row=10, column=0, padx=(5), pady=(100,0), sticky='sw')
    txtInfo9 = tk.Label(frameResultL, text='h = ', bg='#120702', fg='#E1F4E3', font=('Arial', 20, 'bold'))
    txtInfo9.grid(row=11, column=0, padx=(5), pady=(0,0), sticky='sw')
    if resultado.h == True:
        txtInfo9.config(text='h = 1 (Existe tendência significativa)')
    else:
        txtInfo9.config(text='h = 0 (NÃO existe tendência significativa)')
    txtInfo10 = tk.Label(frameResultL, text='Trend = ', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo10.grid(row=12, column=0, padx=(5), pady=(0,0), sticky='sw')
    if resultado.trend == 'increasing':
        txtInfo10.config(text='Tendência = Crescente')
    elif resultado.trend == 'decreasing':
        txtInfo10.config(text='Tendência = Decrescente')
    else:
        txtInfo10.config(text='Tendência = Nenhum')
    txtInfo11 = tk.Label(frameResultL, text=f'p = {resultado.p}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo11.grid(row=13, column=0, padx=(5), pady=(0,0), sticky='sw')
    significancia = round(100 - (resultado.p * 100), 2)
    txtInfo12 = tk.Label(frameResultL, text=f'Nível de significância (p) = {significancia}%', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo12.grid(row=14, column=0, padx=(5), pady=(0,0), sticky='sw')
    txtInfo13 = tk.Label(frameResultL, text=f'z = {resultado.z}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo13.grid(row=15, column=0, padx=(5), pady=(0,0), sticky='sw')
    txtInfo14 = tk.Label(frameResultL, text=f'Tau = {resultado.Tau}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo14.grid(row=16, column=0, padx=(5), pady=(0,0), sticky='sw')
    txtInfo15 = tk.Label(frameResultL, text=f's = {resultado.s}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo15.grid(row=17, column=0, padx=(5), pady=(0,0), sticky='sw')
    txtInfo16 = tk.Label(frameResultL, text=f'Var s = {resultado.var_s}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo16.grid(row=18, column=0, padx=(5), pady=(0,0), sticky='sw')
    txtInfo17 = tk.Label(frameResultL, text=f'Slope = {resultado.slope}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo17.grid(row=19, column=0, padx=(5), pady=(0,0), sticky='sw')
    txtInfo18 = tk.Label(frameResultL, text=f'Intercept = {resultado.intercept}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo18.grid(row=20, column=0, padx=(5), pady=(0,0), sticky='sw')

    if filtro != 'sem':
        janFiltros.destroy()


# Janela principal -------------------------------------------------------

# janela
janMenu = tk.Tk()
janMenu.title('RainLine | por Múcio Moura | ' + version)
janMenu.geometry('720x540')
janMenu.configure(bg='#120702')
janMenu.minsize(720, 540)


# top
frameTop = tk.Frame(janMenu, bg='#250E04')
frameTop.pack(side=tk.TOP, fill=tk.X)
txtTop = tk.Label(frameTop, text='RainLine', bg='#250E04', fg='#E1F4E3', font=('Arial', 40, 'bold'))
txtTop.pack(pady=(20,0))
txtTop2 = tk.Label(frameTop, text='Calculadora de tendência de precipitação', bg='#250E04', fg='#E1F4E3', font=('Arial', 15))
txtTop2.pack(pady=(0,20))


# selecao de planilha
if multiSheet:
    global planSelected
    txtMultiSheet = tk.Label(janMenu, text='Foi identificado mais de uma planilha.\nSelecione a planilha desejada:', bg='#120702', fg='#E1F4E3', font=('Arial', 12))
    txtMultiSheet.pack(side=tk.TOP, pady=(0,0))
    planSelected = tk.StringVar()
    planSelected.set(planNome[0])
    planOptions = tk.OptionMenu(janMenu, planSelected, *planNome)
    planOptions.config(bg='#EFF9F0', fg='#120702', font=('Arial', 10), width=20, height=1, activebackground='#89D28F', border=0)
    planOptions.pack(side=tk.TOP, pady=(0,5))


# botoes
txtBotoes = tk.Label(janMenu, text='Filtros:', bg='#120702', fg='#E1F4E3', font=('Arial', 15))
txtBotoes.pack(side=tk.TOP, pady=(30,0))
btGeral = tk.Button(janMenu, text='Sem filtros', bg='#FF6219', fg='#120702', font=('Arial', 20), width=15, height=1, activebackground='#89D28F', border=0, command=lambda: escolhaFiltro('sem'))
btGeral.pack(side=tk.TOP, pady=(0,5))
btMm = tk.Button(janMenu, text='Milímetros', bg='#FF6219', fg='#120702', font=('Arial', 20), width=15, height=1, activebackground='#89D28F', border=0, command=lambda: escolhaFiltro('mm'))
btMm.pack(side=tk.TOP, pady=(0,5))
btData = tk.Button(janMenu, text='Data', bg='#FF6219', fg='#120702', font=('Arial', 20), width=15, height=1, activebackground='#89D28F', border=0, command=lambda: escolhaFiltro('data'))
btData.pack(side=tk.TOP, pady=(0,5))
btAmbos = tk.Button(janMenu, text='Data e milímetros', bg='#FF6219', fg='#120702', font=('Arial', 20), width=15, height=1, activebackground='#89D28F', border=0, command=lambda: escolhaFiltro('ambos'))
btAmbos.pack(side=tk.TOP, pady=(0,5))


# rodape
frameRodape = tk.Frame(janMenu, bg='#250E04')
frameRodape.pack(side=tk.BOTTOM, fill=tk.X)

check = tk.PhotoImage(file='assets/check16.png')
uncheck = tk.PhotoImage(file='assets/uncheck16.png')
imgFileCheck = tk.Label(frameRodape, image=None, bg='#250E04')
imgFileCheck.pack(side=tk.LEFT, pady=1)
txtFileCheck = tk.Label(frameRodape, text=None, bg='#250E04', fg='#E1F4E3', font=('Arial', 10))
txtFileCheck.pack(side=tk.LEFT, pady=1)

if fileVer:
    imgFileCheck.config(image=check)
    txtFileCheck.config(text='Dados carregados com sucesso. ' + str(planNum) + ' planilha(s) identificada(s).', font=('Arial', 10))
else:
    imgFileCheck.config(image=uncheck)
    txtFileCheck.config(text='Erro ao carregar dados.', font=('Arial', 10, 'bold'))
    btGeral.config(state='disabled', bg='#250E04')
    btMm.config(state='disabled', bg='#250E04')
    btData.config(state='disabled', bg='#250E04')
    btAmbos.config(state='disabled', bg='#250E04')
    mb.showerror('Erro ao carregar dados!', message='Verifique se o arquivo está dentro da pasta "dados".\nVerifique se o arquivo está nomeado exatamente como "dados".')
    

txtVersion = tk.Label(frameRodape, text=version, bg='#250E04', fg='#E1F4E3', font=('Arial', 10, 'bold'))
txtVersion.pack(side=tk.RIGHT, pady=1)

janMenu.mainloop()