from PyQt5 import uic, QtWidgets

class calculo_pagina_1:
    def __init__(self, vazao, comprimento, perda, pressao):
        self.vazao = vazao
        self.comprimento = comprimento
        self.perda = perda
        self.pressao = pressao

        if type(self.vazao) == str:
            self.vazao = float(self.vazao.replace(",","."))

        if type(self.comprimento) == str:
            self.comprimento = float(self.comprimento.replace(",","."))

        if type(self.perda) == str:
            self.perda = float(self.perda.replace(",","."))

        if type(self.pressao) == str:
            self.pressao = float(self.pressao.replace(",","."))

    def calcular(self):                               
        l1 = 10 * (((1.663785*((10)**(-3))*((self.vazao)**1.85)*self.comprimento)/(self.perda*self.pressao))**(1/5))
        l2 = (1.663785*((10)**(-3))*((self.vazao)**1.85)*self.comprimento)
        l3 = (self.perda*self.pressao)
        screen.label.setText(f'O Diametro interno é: {round(l1,2)}mm')  
        return [l1, l2, l3]

    def ofConv(self): 
        linha_01 = f"d=10[nroot!5?! !1.663785*10^-3* {self.vazao} ^1.85* {self.comprimento}? over ! {self.perda} * {self.pressao} ? ? ] NEWLINE "
        linha_02 = f"d=10[nroot!5?! !{round(self.calcular()[1], 4)}? over !{round(self.calcular()[2], 4)}?? ] NEWLINE "
        linha_03 = f"d= {round(self.calcular()[0], 2)} mm NEWLINE "
        arquivo_office = linha_01.replace("!","{").replace("?","}") + linha_02.replace("!","{").replace("?","}") + linha_03
        return [arquivo_office]

def deposito_variavis():
    Q = screen.vazao.text()             #Vazão
    c_t = screen.comprimento.text()     #Comprimento total da tubulação
    d_p = screen.perda.text()           #Perda de pressão admissivel
    p = screen.pressao.text()           #Pressão de trabalho  
    okey = calculo_pagina_1(Q,c_t,d_p,p)
    okey.calcular()  
    return [okey.ofConv()[0]]


def salvar():
    arquivo = QtWidgets.QFileDialog.getSaveFileName()[0]
    guardando = deposito_variavis()[0]
    with open (arquivo + '.txt', 'w') as a:
        a.write(guardando)


def option_select():
    text = screen.comboBox.currentText()

    if text == "Diametro interno da tubulação":
        screen.tela_1.show()
        screen.tela_2.close()

    if text == "tela 2":
        screen.tela_1.close()
        screen.tela_2.show()



def screen_offs():
    screen.tela_1.close()
    screen.tela_2.close()

app = QtWidgets.QApplication([])
screen = uic.loadUi("main_ux.ui")

screen_offs()
screen.comboBox.addItems(["Escolha uma tela","Diametro interno da tubulação", "tela 2"])

screen.bt_01.clicked.connect(option_select)
screen.bt_02.clicked.connect(deposito_variavis)

screen.actionSalvar.triggered.connect(salvar)

screen.show()
app.exec()