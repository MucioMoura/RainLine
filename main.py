import tkinter as tk
import tkinter.messagebox as mb
import pymannkendall as mk
import pandas as pd
from matplotlib.figure import Figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas


# VERSÃO -----------------------------------------------------------------
version = '0.0.1-proto'

# Local do arquivo de dados ----------------------------------------------
filePath = 'dados/dados.xlsx'
# Carregar dados
try:
    global dados
    dados = pd.read_excel(filePath, engine='openpyxl')
    dados.columns = ['data', 'mm']
    dados['data'] = pd.to_datetime(dados['data'])
    dados['dias'] = (dados['data'] - dados['data'].min()).dt.days
    dados['anos'] = dados['data'].dt.year

    planNome = pd.ExcelFile(filePath).sheet_names
    planNum = len(planNome)
    if planNum > 1:
        multiSheet = True

    fileVer = True
except:
    fileVer = False
    multiSheet = False

def escolhaFiltro(tipo):
    global filtro
    filtro = tipo
    if filtro == 'sem':
        filtrarDados()
    else:
        definirFiltros()


def definirFiltros():
    def enablerBtFiltrosMm(checkMaior, checkMenor):
        if checkMaior.get() == 1 or checkMenor.get() == 1:
            btFiltrosMm.config(state='normal')
        else:
            btFiltrosMm.config(state='disabled')

    janFiltros = tk.Toplevel()
    janFiltros.geometry('360x200')
    janFiltros.configure(bg='#120702')
    janFiltros.maxsize(360, 200)
    janFiltros.minsize(360, 200)

    if filtro == 'mm':
        global checkMaior, checkMenor
        global entryFiltrosMmMaior, entryFiltrosMmMenor
        checkMaior = tk.IntVar()
        checkMenor = tk.IntVar()
        janFiltros.title('Filtro de milímetros')
        txtFiltrosMm = tk.Label(janFiltros, text='Maior que ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosMm.grid(row=0, column=0, padx=(80,0), pady=(40,0))
        entryFiltrosMmMaior = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=5)
        entryFiltrosMmMaior.grid(row=0, column=1, padx=0, pady=(40,0))
        checkFiltrosMm = tk.Checkbutton(janFiltros, variable=checkMaior, bg='#120702', font=('Arial', 16), command=lambda:enablerBtFiltrosMm(checkMaior, checkMenor))
        checkFiltrosMm.grid(row=0, column=2, padx=0, pady=(40,0))
        
        txtFiltrosMm2 = tk.Label(janFiltros, text='Menor que ', bg='#120702', fg='#E1F4E3', font=('Arial', 16))
        txtFiltrosMm2.grid(row=1, column=0, padx=(80,0))
        entryFiltrosMmMenor = tk.Entry(janFiltros, bg='#EFF9F0', fg='#120702', font=('Arial', 16), width=5)
        entryFiltrosMmMenor.grid(row=1, column=1, padx=0)
        checkFiltrosMm2 = tk.Checkbutton(janFiltros, variable=checkMenor, bg='#120702', font=('Arial', 16), command=lambda:enablerBtFiltrosMm(checkMaior, checkMenor))
        checkFiltrosMm2.grid(row=1, column=2, padx=0)

        btFiltrosMm = tk.Button(janFiltros, text='Aplicar', bg='#FF6219', fg='#120702', font=('Arial', 16), width=10, height=1, activebackground='#89D28F', border=0, state='disabled', command=lambda:filtrarDados())
        btFiltrosMm.grid(row=2, column=0, columnspan=3, padx=(200,0), pady=(20,0))


def filtrarDados():
    global dadosFiltrados, resultado

    if filtro == 'sem':
        dadosFiltrados = dados
    elif filtro == 'mm':
        if checkMaior.get() == 1 and checkMenor.get() == 1:
            dadosFiltrados = dados[dados['mm'] > float(entryFiltrosMmMaior.get())]
            dadosFiltrados = dadosFiltrados[dadosFiltrados['mm'] < float(entryFiltrosMmMenor.get())]
        elif checkMaior.get() == 1:
            dadosFiltrados = dados[dados['mm'] > float(entryFiltrosMmMaior.get())]
        else:
            dadosFiltrados = dados[dados['mm'] < float(entryFiltrosMmMenor.get())]

    resultado = mk.original_test(dadosFiltrados['mm'])
    telaResultado()

def telaResultado():
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
    graf = fig(figsize=(5, 4), dpi=100)
    plot = graf.add_subplot(111)
    plot.plot(dadosFiltrados['data'], dadosFiltrados['mm'], label='Dados', color='black', lw=0.80, marker='o', ms=2, alpha=0.5)
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
    txtInfo = tk.Label(frameResultL, text=f'Dados de {dadosFiltrados['anos'].min()} a {dadosFiltrados['anos'].max()}', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo.grid(row=0, column=0, padx=(5), pady=(5), sticky='nw')
    txtInfo2 = tk.Label(frameResultL, text='Filtros:', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo2.grid(row=1, column=0, padx=(5), pady=(5), sticky='nw')
    txtInfo3 = tk.Label(frameResultL, text='-> Milímetros | Não aplicado.', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo3.grid(row=2, column=0, padx=(5), pady=(5), sticky='nw')
    txtInfo4 = tk.Label(frameResultL, text='-> Data | Não aplicado.', bg='#120702', fg='#E1F4E3', font=('Arial', 20))
    txtInfo4.grid(row=3, column=0, padx=(5), pady=(5), sticky='nw')
    
    if filtro == 'sem':
        txtInfo3.config(text='-> Milímetros | Não aplicado.')
        txtInfo4.config(text='-> Data | Não aplicado.')
        print(f'if de sem ({filtro})')
    elif filtro == 'mm':
        if checkMaior.get() == 1 and checkMenor.get() == 1:
            print(f'if de mm ({filtro})')
            txtInfo3.config(text=f'-> Milímetros | Maior que {float(entryFiltrosMmMaior.get())} | Menor que {float(entryFiltrosMmMenor.get())}')
        elif checkMaior.get() == 1:
            txtInfo3.config(text=f'-> Milímetros | Maior que {float(entryFiltrosMmMaior.get())}')
        else:
            txtInfo3.config(text=f'-> Milímetros | Menor que {float(entryFiltrosMmMenor.get())}')

    
    


# Janela principal -------------------------------------------------------

# janela
janMenu = tk.Tk()
janMenu.title('Calculadora de tendência de chuva | por Múcio Moura | ' + version)
janMenu.geometry('720x540')
janMenu.configure(bg='#120702')
janMenu.minsize(720, 540)


# top
frameTop = tk.Frame(janMenu, bg='#250E04')
frameTop.pack(side=tk.TOP, fill=tk.X)
txtTop = tk.Label(frameTop, text='Calculadora de tendência de chuva', bg='#250E04', fg='#E1F4E3', font=('Arial', 30, 'bold'))
txtTop.pack(pady=(20))


# selecao de planilha
if multiSheet:
    txtMultiSheet = tk.Label(janMenu, text='Foi identificado mais de uma planilha.\nSelecione a planilha desejada:', bg='#120702', fg='#E1F4E3', font=('Arial', 12))
    txtMultiSheet.pack(side=tk.TOP, pady=(0,0))
    planOptions = tk.OptionMenu(janMenu, tk.StringVar(), *planNome)
    planOptions.config(bg='#EFF9F0', fg='#120702', font=('Arial', 10), width=20, height=1, activebackground='#89D28F', border=0)
    planOptions.pack(side=tk.TOP, pady=(0,5))
    planSelected = planOptions.cget('textvariable')

# PY_VAR0 caso nenhuma planilha seja selecionada

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
    

txtVersion = tk.Label(frameRodape, text=version, bg='#250E04', fg='#E1F4E3', font=('Arial', 10))
txtVersion.pack(side=tk.RIGHT, pady=1)

janMenu.mainloop()