from PyQt5 import uic, QtWidgets

app = QtWidgets.QApplication([])
screen = uic.loadUi("main_ux.ui")


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
        return [l1, l2, l3]

def deposito_variavis():
    Q = screen.vazao.text()#Vazão
    c_t = screen.comprimento.text()#Comprimento total da tubulação
    d_p = screen.perda.text()#Perda de pressão admissivel
    p = screen.pressao.text()  #Pressão de trabalho  
    okey = calculo_pagina_1(Q,c_t,d_p,p)
    okey.calcular()
    screen.label.setText(f'O Diametro interno é: {round(okey.calcular()[0],2)}mm')
    return [Q, c_t, d_p, p, okey.calcular()[0],okey.calcular()[1], okey.calcular()[2]]

def arquivar():
    Q = deposito_variavis()[0]
    c_t = deposito_variavis()[1]
    d_p = deposito_variavis()[2]
    p = deposito_variavis()[3]
    d = str(round(deposito_variavis()[4],4))
    l1 = str(round(deposito_variavis()[5],4))
    l2 = str(round(deposito_variavis()[6],4))

    linha_01 = f"d=10[nroot!5?! !1.663785*10^-3* {Q} ^1.85* {c_t}? over ! {d_p} * {p} ? ? ] NEWLINE "
    linha_02 = f"d=10[nroot!5?! !{l1,4}? over !{l2}?? ] NEWLINE "
    linha_03 = f"d= {d} mm NEWLINE "
    arquivo_office = linha_01.replace("!","{").replace("?","}") + linha_02.replace("!","{").replace("?","}") + linha_03
    return [arquivo_office]


def salvar():
    arquivo = QtWidgets.QFileDialog.getSaveFileName()[0]
    guardando = arquivar()[0]
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
        screen.vazao.setText("Q")
        screen.comprimento.setText("Lt")
        screen.lineEdit_3.setText("delta P")
        screen.lineEdit_4.setText("P")
        screen.label.setText(f'O Diametro interno é:')



def screen_offs():
    screen.tela_1.close()
    screen.tela_2.close()


screen_offs()
screen.comboBox.addItems(["Escolha uma tela","Diametro interno da tubulação", "tela 2"])
screen.bt_01.clicked.connect(option_select)
screen.bt_02.clicked.connect(deposito_variavis)
screen.actionSalvar.triggered.connect(salvar)

screen.show()
app.exec()