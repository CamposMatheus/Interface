

import sys                                      #importa biblioteca sys
import serial                                   #necessário para importar a biblioteca pyserial
from PyQt5.QtCore import QThread, pyqtSignal    #importa biblioteca PyQt5
import math                                     #impota biblioteca math
import pyqtgraph as pg                          #importa biblioteca pyqtgraph


ser = serial.Serial('COM2', 500000)             #define "COM2" para comunicação serial e baud rate de 500000 bps
VTH=0                                           #variável para armazenar tensão do termistor
VADC=0                                          #variável para armazenar tensão do ADC


global controle                                 #variável para controlar se começa a aquisição de temperatura
global temperatura                              #variável para armazenar a temperatura
controle = 'P'                                  #atribui "P" para que não se inicie automaticamente a aquisição


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):                          #classe para interface e tratamento dos sinais
    def setupUi(self, Form):
        Form.setObjectName("Form")              #seta nome do objeto
        Form.resize(1220, 592)                  #configurações da interface
        font = QtGui.QFont()
        font.setPointSize(24)
        Form.setFont(font)
        Form.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.pushButton = QtWidgets.QPushButton(Form)                   #cria push button responsável por pausar a aquisição e define configurações do botão
        self.pushButton.setGeometry(QtCore.QRect(418, 481, 80, 80))
        self.pushButton.setText("")
        self.pushButton.clicked.connect(self.evento2)                   #conecta o click do botão pause com o método "evento2"
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/Matheus Campos/Desktop/pausaa.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)  #define a imagem que ira aparecer no botão pause
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(50, 50))
        self.pushButton.setObjectName("pushButton")


        self.lcd_Tgrade = QtWidgets.QLCDNumber(Form)                    #cria o lcd que ira mostrar a temperatura da grade e configura o lcd
        self.lcd_Tgrade.setEnabled(True)
        self.lcd_Tgrade.setGeometry(QtCore.QRect(650, 20, 161, 51))
        self.lcd_Tgrade.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcd_Tgrade.setSmallDecimalPoint(False)
        self.lcd_Tgrade.setNumDigits(5)
        self.lcd_Tgrade.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_Tgrade.setProperty("value", 00000)
        self.lcd_Tgrade.setProperty("intValue", 00000)
        self.lcd_Tgrade.setObjectName("lcd_Tgrade")
        self.Tgrade = QtWidgets.QLabel(Form)
        self.Tgrade.setGeometry(QtCore.QRect(20, 8, 641, 61))

        font = QtGui.QFont()
        font.setPointSize(36)
        self.Tgrade.setFont(font)
        self.Tgrade.setLineWidth(1)
        self.Tgrade.setMidLineWidth(1)
        self.Tgrade.setTextFormat(QtCore.Qt.PlainText)
        self.Tgrade.setObjectName("Tgrade")


        pg.setConfigOptions(antialias=True)         #configurações para o gráfico
        self.tabWidget = pg.PlotWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(20, 70, 691, 371))
        self.tabWidget.setRange(yRange=[0, 3], xRange=[0,0.6 ])
        self.curve = self.tabWidget.plot(pen='r')




        self.Inicia = QtWidgets.QPushButton(Form)               #cria push button responsável por iniciar a aquisição e define configurações do botão
        self.Inicia.setGeometry(QtCore.QRect(323, 481, 80, 80))
        self.Inicia.setText("")
        self.Inicia.clicked.connect(self.evento)                #conecta o click do botão pause com o método "evento"

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/Matheus Campos/Desktop/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)     #define a imagem que ira aparecer no botão play
        self.Inicia.setIcon(icon1)
        self.Inicia.setIconSize(QtCore.QSize(50, 50))
        self.Inicia.setCheckable(False)
        self.Inicia.setObjectName("Inicia")

        self.Vtermistor = QtWidgets.QLabel(Form)                            #cria label para texto e configura o label
        self.Vtermistor.setGeometry(QtCore.QRect(830, 80, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Vtermistor.setFont(font)
        self.Vtermistor.setObjectName("Vtermistor")

        self.Vfbg = QtWidgets.QLabel(Form)                                  #cria label para texto e configura o label
        self.Vfbg.setGeometry(QtCore.QRect(831, 360, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Vfbg.setFont(font)
        self.Vfbg.setObjectName("Vfbg")

        self.lcd_Vtermistor = QtWidgets.QLCDNumber(Form)                    #cria o lcd que ira mostrar a tensão do termistor e configura o lcd
        self.lcd_Vtermistor.setGeometry(QtCore.QRect(900, 110, 81, 41))
        self.lcd_Vtermistor.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_Vtermistor.setProperty("value", 00000)
        self.lcd_Vtermistor.setObjectName("lcd_Vtermistor")

        self.lcd_Vfbg = QtWidgets.QLCDNumber(Form)                          #cria o lcd que ira mostrar a tensão do termistor e configura o lcd
        self.lcd_Vfbg.setGeometry(QtCore.QRect(900, 400, 81, 41))
        self.lcd_Vfbg.setProperty("value", 00000)
        self.lcd_Vfbg.setObjectName("lcd_Vfbg")


        self.Ttermistor = QtWidgets.QLabel(Form)                            #cria label para texto e configura o label
        self.Ttermistor.setGeometry(QtCore.QRect(831, 170, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Ttermistor.setFont(font)
        self.Ttermistor.setObjectName("Ttermistor")
        self.lcd_Ttermistor = QtWidgets.QLCDNumber(Form)
        self.lcd_Ttermistor.setGeometry(QtCore.QRect(900, 200, 81, 41))
        self.lcd_Ttermistor.setProperty("value", 00000)
        self.lcd_Ttermistor.setProperty("intValue", 00000)
        self.lcd_Ttermistor.setObjectName("lcd_Ttermistor")


        self.LambidaLaser = QtWidgets.QLabel(Form)                           #cria label para texto e configura o label
        self.LambidaLaser.setGeometry(QtCore.QRect(831, 270, 321, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LambidaLaser.setFont(font)
        self.LambidaLaser.setObjectName("LambidaLaser")

        self.lcd_LambidaLaser = QtWidgets.QLCDNumber(Form)                  #cria o lcd que ira mostrar a comprimento de onda do laser e configura o lcd
        self.lcd_LambidaLaser.setGeometry(QtCore.QRect(900, 300, 171, 41))
        self.lcd_LambidaLaser.setNumDigits(10)
        self.lcd_LambidaLaser.setProperty("value", 000000)
        self.lcd_LambidaLaser.setObjectName("lcd_LambidaLaser")


        self.LambdaBragg = QtWidgets.QLabel(Form)                           #cria label para texto e configura o label
        self.LambdaBragg.setGeometry(QtCore.QRect(830, 470, 361, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LambdaBragg.setFont(font)
        self.LambdaBragg.setObjectName("LambdaBragg")


        self.lcd_LambdaBragg = QtWidgets.QLCDNumber(Form)                   #cria o lcd que ira mostrar a comprimento de onda do laser e configura o lcd
        self.lcd_LambdaBragg.setGeometry(QtCore.QRect(900, 500, 81, 41))
        self.lcd_LambdaBragg.setProperty("value", 00000.0)
        self.lcd_LambdaBragg.setObjectName("lcd_LambdaBragg")
        self.pushButton.raise_()
        self.Tgrade.raise_()
        self.lcd_Tgrade.raise_()
        self.Inicia.raise_()
        self.Vtermistor.raise_()
        self.Vfbg.raise_()
        self.lcd_Vtermistor.raise_()
        self.lcd_Vfbg.raise_()
        self.Ttermistor.raise_()
        self.lcd_Ttermistor.raise_()
        self.LambidaLaser.raise_()
        self.lcd_LambidaLaser.raise_()
        self.LambdaBragg.raise_()
        self.lcd_LambdaBragg.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))                             #define os textos que vão aparecer nos labels criados anteriormente
        self.Tgrade.setText(_translate("Form", "Temperatura Interrogada(°C):"))
        self.Vtermistor.setText(_translate("Form", "Tensão do termistor(V):"))
        self.Vfbg.setText(_translate("Form", "Tensão amostrada na grade(V):"))
        self.Ttermistor.setText(_translate("Form", "Temperatura do Termistor(°C): "))
        self.LambidaLaser.setText(_translate("Form", "Comprimento de onda Laser(nm):"))
        self.LambdaBragg.setText(_translate("Form", "Comprimento de onda refletido(nm):"))


    def update(self, tempLaser):                    #metodo ouvinte do sinal trigger e que atualiza os valores dos displays lcd
        self.lcd_Ttermistor.display(tempLaser)
        self.lcd_Vtermistor.display(VTH)
        self.lcd_Vfbg.display(VFBG)
        self.lcd_LambidaLaser.display(lambidaLaser)
        self.lcd_Tgrade.display(temperaturaDisplay)
        self.curve.setData(vetorTH, vetorFBG)




    def evento(self):                               #método "evento" chamado quando o botão play é pressionado
        global controle
        if controle !='I':                          #testa 'controle' para que a thread não seja reiniciada caso 'play' seja apertado duas vezes
            self.thread_loop = Leitura()            #inicia thread
            self.thread_loop.start()                #inicia thread
            controle='I'                            #atribui "I" a variável de controle
            self.thread_loop.trigger.connect(self.update)                  #define a função update como ouvinte do sinal trigger, deve ser chamado
                                                                           #depois da inicialização do objeto Leitura()



    def evento2(self):                              #método "evento2" chamado quando o botão pause é pressionado
        global controle
        global controle
        controle='P'                                #escreve "P" na variável de controle
        ser.write(b'P')                             #transmite "P" para o microcontrolador para interromper a aquisição





class Leitura(QThread):
    #cria classe Leitura
    trigger = pyqtSignal(float)                     #sinal trigger
    temperaturaLaser=0.0                            #atributo da classe



    def run(self):                                  #método run

        global controle, VFBG, VTH, lambidaLaser, temperaturaGrade, lambidaBrag, temperaturaDisplay,temperaturaGradeAnterior, vetorFBG,vetorTH
        vetorFBG=[]                                 #vetor para armazenar os valores da tensão FBG
        vetorTH=[]                                  #vetor para armazenar os valores da tensão do termistor
        flag1=False                                 #flags auxiliares
        flag2=False

        temperaturaGrade=0                          #inicializa temperatura da grade
        var=0
        temperaturaDisplay=0                        #inicializa temperatura da grade
        temperaturaGradeAnterior=0                  #inicializa temperatura da grade

        while (controle=='I'):                      #laço de controle para aquisição dos valores da aquisição
            ser.write(b'I')

            TH1 = list(ser.read(1))                 #recebe valores pela comunicação serial
            TH2 = list(ser.read(1))
            TH3 = list(ser.read(1))

            ADC1 = list(ser.read(1))
            ADC2 = list(ser.read(1))
            ADC3 = list(ser.read(1))

            for i in range(256):                    #converte valores recebidos em inteiros
                if i in TH1:
                    valor0 = i
            for i in range(256):
                if i in TH2:
                    valor1 = i
            for i in range(256):
                if i in TH3:
                    valor2 = i

            for i in range(256):
                if i in ADC1:
                    valor3 = i
            for i in range(256):
                if i in ADC2:
                    valor4 = i
            for i in range(256):
                if i in ADC3:
                    valor5 = i

            TH = ((valor0 << 16) | (valor1 << 8) | (valor2))        #junta os valores recebidos em uma única variável
            ADC = ((valor3 << 16) | (valor4 << 8) | (valor5))       #junta os valores recebidos em uma única variável

            VTH = (TH / 8388607) * 2.5                              #converte valores de TH em tensão
            VFBG = (ADC / 8388607) * 2.5                            #converte valores de TH em tensão

            RTH=15000*((1.25-VTH)/VTH)                              #encontra valor de resistência associado ao valor de VTH encontrado

            self.temperaturaLaser=(1/((1/(25+273.15))+(1/(3528)*math.log(RTH/15000))))-273.15   #define temperatura do laser
            lambidaLaser=(0.092669*self.temperaturaLaser)+(1547.859392)                         #define ocmprimento de onda do laser

            if VFBG > 2.44 and VTH > var:
                var = VTH


            if VFBG>1.25 and not flag1:                             #verifica se inicia a gravar os valores de VFB no vetor
                flag1=True
                vetorTH.clear()                                     #limpa " vetorTH"
                vetorFBG.clear()                                    #limpa " vetorFBG"

            if VFBG<1.25 and flag1:                                 #verifica se a gravação deve parar
                flag2=True
                flag1=False


            if flag1:                                               #armazena valores de tensão "VFBG" no "vetorFBG"
                vetorFBG.append (VFBG)
                vetorTH.append(VTH)                                 #armazena valores de tensão "VTH" no "vetorTH"
            if flag2:
                flag2=False
                maior=vetorFBG[0]
                posicao = 0
                for i in range(len(vetorFBG)):                      #verifica maior valore de tensão "VFBG" salvo e armazena
                    atual=vetorFBG[i]
                    if atual>maior:
                        maior=atual
                        posicao = i


                VTHmaxima=vetorTH[posicao]                          #define valores de comprimento de onda do laser, comprimento de onda de brag,
                                                                    #temperatura da grade e temperatura que será mostrada no display
                RTHmaximo = 15000 * ((1.25 - VTHmaxima) / VTHmaxima)
                temperaturaLasermaxima = (1 / ((1 / (25 + 273.15)) + (1 / (3528) * math.log(RTHmaximo / 15000)))) - 273.15
                lambidaBrag = (0.092669 *temperaturaLasermaxima) + (1547.859392)
                temperaturaGrade=27+(0.092669/(1550*6.7/1000000))*(temperaturaLasermaxima-22.1703662655)

                temperaturaDisplay=(temperaturaGrade+temperaturaGradeAnterior)/2            #código que executa o método MID
                temperaturaGradeAnterior=temperaturaGrade
                flag1=False


            self.trigger.emit(self.temperaturaLaser)              #emite um sinal trigger e passa temeperatura com argumento para os ouvintes, "self.temperatura" pq é um atributo da classe


if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)          #instancia da clase QApplication
    window=QtWidgets.QMainWindow()
    main_window = Ui_Form()
    main_window.setupUi(window)
    window.show()
    sys.exit(application.exec_())                           #loop para mostrar a janela e fechar corretamente









