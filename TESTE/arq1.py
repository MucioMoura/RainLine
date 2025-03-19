
global checkMaior
checkMaior = 2

class MyClass():
    global valorMain
    valorMain = 0

    def printar(cls):
        print(checkMaior + cls.valorMain)

    def setValorMain(cls, newValorMain):
        cls.valorMain = newValorMain