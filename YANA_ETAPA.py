# -------------------------- by Pablo Buestan Andrade --------------------------
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from time import gmtime, strftime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import threading
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
import sys
import time
import datetime
import telepot
import icon
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open, \
    include_callback_query_chat_id, per_inline_from_id
# -------------------------------------------------------------------------------
# ----------------------------- GLOBAL VARIABLE ---------------------------------
apikey = 'BlAZtgFKew_U54Kc5GmDiLdXEwp5eLJy_PVtt6OehkIw'  # WATSON ASSISTANT
urlserver = 'https://api.us-south.assistant.watson.cloud.ibm.com'  # DALLAS SERVER
assist_id = 'ac90401a-e0a6-4bc8-abf2-bc1494e50afb'  # CHATBOTEC-COVID19
telepotkey = '1382401252:AAHOIlBWEx7rpDrWsHbonCjxm9SBKgyPUZY' # CHATBOT PRUEBAS
dict_users_active = {} 
# -------------------------------------------------------------------------------
# ----------------------------------- SETUP -------------------------------------
# ------------------------------------ IBM --------------------------------------
authenticator = IAMAuthenticator(apikey)
service = AssistantV2(
    version='2020-04-01',
    authenticator=authenticator
)
assistant_id = assist_id
class connection_wats():
    def __init__(self):
        self.session_id = 0
        self.chat_id = 0
        self.message = " "
        self.intent = 0
        self.skills = 0
        self.user_newr = 0
        self.response = 0
        self.validation = 0
        self.emerge = 0
        self.data_Patient = []
        self.now = 0
        self.time_now = 0
        self.date_now = 0
        self.values_Patient = []
        self.valuess = 0
    def send_message(self):
        self.response = service.message(
            assistant_id,
            self.session_id,
            input={
                'message_type:': 'text',
                'text': self.message,
                'options': {
                    'return_context': True
            }
            }
        ).get_result()
        print (self.response)

        if self.response["output"]["generic"][0]['response_type'] == 'text':
            message = self.response["output"]["generic"][0]["text"]
            try:
                self.skills = self.response['context']['skills']['main skill']['user_defined']
            except:
                self.skills = " "
            bot.sendMessage(self.chat_id, message)
            print (message)
        elif self.response["output"]["generic"][0]["response_type"] == 'option':
            message1 = self.response["output"]["generic"][0]['title']
            message2 = self.response["output"]["generic"][0]['options'][0]['label']
            message3 = self.response["output"]["generic"][0]['options'][1]['label']
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=message2, callback_data='1')],
                [InlineKeyboardButton(text=message3, callback_data='0')],
            ])
            bot.sendMessage(self.chat_id, message1, reply_markup=keyboard)
            print(message1)
        try:
            self.intent = self.response["output"]["intents"][0]["intent"]
        except:
            self.intent = " "
        try:
            self.user_newr = self.response["context"]["skills"]["main skill"]["user_defined"]["Datos_completos"]
        except:
            self.user_newr = " "
        try:
            self.validation = self.response["context"]["skills"]["main skill"]["user_defined"]["Sesion_terminada"]
            self.emerge = self.response["context"]["skills"]["main skill"]["user_defined"]["EMERGENCY"]
        except:
            self.validation = " "
            self.emerge = " "

        if self.intent == "bienvenido":
            database(self.chat_id)
        if self.user_newr == 1:
            self.data_Patient.append(self.chat_id)
            self.data_Patient.append(self.response["context"]["skills"]["main skill"]["user_defined"]['Nombre'])
            self.data_Patient.append(self.response["context"]["skills"]["main skill"]["user_defined"]['Numero_cedula'])
            self.data_Patient.append(self.response["context"]["skills"]["main skill"]["user_defined"]['Edad'])
            self.data_Patient.append(self.response["context"]["skills"]["main skill"]["user_defined"]['Numero_telefono'])
            self.data_Patient.append(self.response["context"]["skills"]["main skill"]["user_defined"]['Dependencia'])
            self.data_Patient.append(self.response["context"]["skills"]["main skill"]["user_defined"]['Caso_Confirmado'])
            print(self.data_Patient)
            add_Patient = "INSERT INTO ListaPacientes(Telegram_ID, Nombres, CI, Edad, Telefono, Dependencia, Caso_Confirmado)VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(add_Patient, self.data_Patient)
            conexion.commit()
            addTable = "CREATE TABLE IF NOT EXISTS `%i`" % self.chat_id + "(Fecha VARCHAR (10), Hora VARCHAR (10), Emergencia VARCHAR (10), Temperatura VARCHAR (10), Fiebre VARCHAR (10), Tos VARCHAR (10), Confusion_o_delirio VARCHAR (10), Perdida_de_olfato_o_gusto VARCHAR (10), Diarrea VARCHAR (10), Vomito VARCHAR (10), Congestion_nasal VARCHAR (10), Cansancio VARCHAR (10),  Dolor_de_cabeza VARCHAR (10), Dolor_de_cuerpo VARCHAR (10), Conjuntivitis VARCHAR (10),  Erupciones_cutaneas VARCHAR (10),Tomo_antiviral VARCHAR (10), Acudio_medico VARCHAR (10), Contacto_personas VARCHAR (10), Realizo_viaje VARCHAR (10), Visito_persona VARCHAR (10), Hospeda_persona VARCHAR (10))"
            cursor.execute(addTable)
        if self.validation == 1 and self.emerge == 0:
            self.now = datetime.datetime.now()
            self.fecha = self.now.strftime("%x")
            self.hora = self.now.strftime("%X")
            self.values_Patient.append(self.fecha)
            self.values_Patient.append(self.hora)
            self.valuess = self.response["context"]["skills"]["main skill"]["user_defined"]
            self.valuess.pop("Sesion_terminada")
            self.valuess.pop("Estado")
            self.valuess.pop("Datos_completos")
            try:
                self.valuess.pop("Nombre")
                self.valuess.pop("Numero_cedula")
                self.valuess.pop("Edad")
                self.valuess.pop("Numero_telefono")
                self.valuess.pop("Dependencia")
                self.valuess.pop("Caso_Confirmado")
            except:
                pass
            self.valuess = list(self.valuess.values())
            for element in self.valuess:
                if element == 0:
                    element = "No"
                elif element == 1:
                    element = "Si"
                self.values_Patient.append(element)
            print(self.values_Patient)
            add_Patient = "INSERT INTO `%i`" % self.chat_id + "(Fecha, Hora, Emergencia, Temperatura, Fiebre, Tos, Confusion_o_delirio, Perdida_de_olfato_o_gusto, Diarrea, Vomito, Congestion_nasal, Cansancio, Dolor_de_cabeza, Dolor_de_cuerpo, Conjuntivitis,  Erupciones_cutaneas, Tomo_antiviral, Acudio_medico, Contacto_personas, Realizo_viaje, Visito_persona, Hospeda_persona)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(add_Patient, self.values_Patient)
            conexion.commit()
            reset_var()
        elif self.validation == 1 and self.emerge == 1:
            # ----------------------------- 
            #Alerta Médico
            search_Patient = "SELECT * FROM ListaPacientes WHERE Telegram_ID = \'%s\' " % self.chat_id
            cursor.execute(search_Patient)
            patient = cursor.fetchall()
            bot.sendMessage (1381039879, "Estimado Dr. Jimmy Arias: \n\nPor favor contactarse de caracter URGENTE con el/la funcionario/a: \n" + patient[0][2] + ".\nEl numero de contacto es el: " + patient [0][5] +". \n\nPresenta una sintomatología GRAVE. Actuar de inmediato. Saludos.")
            bot.sendMessage (1307576737, "Estimado Ing. Giovanny Quinde: \n\nPor favor contactarse de caracter URGENTE con el/la funcionario/a: \n" + patient[0][2] + ".\nEl numero de contacto es el: " + patient [0][5] +". \n\nPresenta una sintomatología GRAVE. Actuar de inmediato. Saludos.")
            # -----------------------------
            self.now = datetime.datetime.now()
            self.fecha = self.now.strftime("%x")
            self.hora = self.now.strftime("%X")
            self.values_Patient.append(self.fecha)
            self.values_Patient.append(self.hora)
            self.valuess = self.response["context"]["skills"]["main skill"]["user_defined"]
            self.valuess.pop("Sesion_terminada")
            self.valuess.pop("Estado")
            self.valuess.pop("Datos_completos")
            try:
                self.valuess.pop("Nombre")
                self.valuess.pop("Numero_cedula")
                self.valuess.pop("Edad")
                self.valuess.pop("Numero_telefono")
                self.valuess.pop("Dependencia")
                self.valuess.pop("Caso_Confirmado")
            except:
                pass
            self.valuess = list(self.valuess.values())
            for element in self.valuess:
                if element == 0:
                    element = "No"
                elif element == 1:
                    element = "Si"
                self.values_Patient.append(element)
            print ("Guardando datos")
            print (self.values_Patient)
            add_Patient = "INSERT INTO `%i`" % self.chat_id + "(Fecha, Hora, Emergencia, Temperatura, Fiebre, Tos, Confusion_o_delirio, Perdida_de_olfato_o_gusto, Diarrea, Vomito, Congestion_nasal, Cansancio, Dolor_de_cabeza, Dolor_de_cuerpo, Conjuntivitis,  Erupciones_cutaneas, Tomo_antiviral, Acudio_medico, Contacto_personas, Realizo_viaje, Visito_persona, Hospeda_persona)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(add_Patient, self.values_Patient)
            except:
                for i in range(19):
                  self.values_Patient.append("Sin dato")
                try:
                    cursor.execute(add_Patient, self.values_Patient)
                except:
                    pass
            conexion.commit()
            reset_var()

# ------------------------------------ TELEGRAM --------------------------------------
class conversation(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(conversation, self).__init__(*args, **kwargs)
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            command = msg['text']
            print("El usuario "+ str(chat_id) + " escribio: "+ command)
            if command == "Hola" or command == "/start" or command == "hola" or command == "ola" or command == "Ola" or command == "Hoola" or command == "HOLA" or command == "hoola" :
                reset_var()
                session_id = service.create_session(assistant_id=assistant_id).get_result()['session_id']
                user = connection_wats()
                dict_users_active[chat_id] = [session_id, user]
            if command == "Reset" or command == "reset":
                reset_var()
        elif content_type == 'location':
            latitude_user = msg['location']['latitude']
            longitude_user = msg['location']['longitude']
            print(latitude_user)
            print(longitude_user)
        if chat_id in dict_users_active:
            dict_users_active[chat_id][1].session_id = dict_users_active[chat_id][0]
            dict_users_active[chat_id][1].chat_id = chat_id
            dict_users_active[chat_id][1].message = command
            dict_users_active[chat_id][1].send_message()
    def on_callback_query(self, msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        bot.answerCallbackQuery(query_id, text='¡Ok!')
        if chat_id in dict_users_active:
            dict_users_active[chat_id][1].session_id = dict_users_active[chat_id][0]
            dict_users_active[chat_id][1].chat_id = chat_id
            dict_users_active[chat_id][1].message = query_data
            dict_users_active[chat_id][1].send_message()
bot = telepot.DelegatorBot(telepotkey, [
    include_callback_query_chat_id(
            pave_event_space())(
            per_chat_id(), create_open, conversation, timeout=600),
])
MessageLoop(bot).run_as_thread()
# ------------------------------------ OTHERS --------------------------------------
resultados = 0
def reset_var():
    print("Reset variables")
    global dbConnect
    global conexion
    global cursor
    global resultados

    dbConnect = {
        'host': 'localhost',
        'user': 'root',
        'password': 'MyNewPass',
        'database': 'pacientes_COVID19',
        'auth_plugin': 'mysql_native_password'
    }
    conexion = mysql.connector.connect(**dbConnect)
    cursor = conexion.cursor()
    sql = "select * from ListaPacientes"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    print(resultados)

reset_var()

def database(chat_id):
    search_Patient = "SELECT * FROM ListaPacientes WHERE Telegram_ID = \'%s\' " % chat_id
    cursor.execute(search_Patient)
    patient = cursor.fetchall()
    if patient:
        dict_users_active[chat_id][1].message = "True"
        dict_users_active[chat_id][1].send_message()
    else:
        dict_users_active[chat_id][1].message = "False"
        dict_users_active[chat_id][1].send_message()

def reminders():
    global resultados
    format = "%a %b %d %H:%M:%S %Y"
    today = datetime.datetime.today()
    day_today = today.strftime(format)
    day_today = day_today.split()
    if day_today[0] == "Mon":
        st_date = time.strftime("%X")
        if st_date == "09:00:00" or st_date == "09:30:00":
            for i in resultados:
                namep = (i)[2]
                namep = namep.split()
                namep = namep[0]
                messagep = ("Buenos días " + namep + ", que tengas un excelente inicio de semana. \n\nSe ha propuesto desde la Jefatura de Seguridad y Salud Ocupacional que todos los días lunes se comuniquen conmigo los funcionarios para realizar una evaluación sintomatológica. \n\nPara el correcto funcionamiento del programa, inicia enviando la palabra 'Hola'; si ya llenaste la información el dia de hoy, ignora este mensaje.\nMuchas gracias.\n\nYANA - UCACUE")
                telegrp = (i)[1]
                print(telegrp, messagep)
                try:
                  bot.sendMessage(telegrp, messagep)
                except:
                  pass  
        time.sleep(1)

# --------------------------------- MAIN LOOP -----------------------------------
init_start = 0
def main_program():
    global init_start
    print("Init")
    reset_var()
    while init_start == 1:
        reminders()

# ------------------------ GRAPHICAL USER INTERFACE -----------------------------
def start_assist():
    global init_start
    init_start = 1
    t = threading.Thread(target=main_program)
    t.start()

def stop_assist():
    global init_start
    init_start = 0

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(400, 205)
        MainWindow.setMinimumSize(QtCore.QSize(400, 205))
        MainWindow.setMaximumSize(QtCore.QSize(400, 205))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 120, 100, 25))
        self.pushButton.setMinimumSize(QtCore.QSize(100, 25))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 25))
        self.pushButton.clicked.connect(self.on_click)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 120, 100, 25))
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 25))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 25))
        self.pushButton_2.clicked.connect(self.off_click)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(87, 10, 303, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 70, 383, 16))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setMidLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(10, 0, 383, 20))
        self.line_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_6.setMidLineWidth(1)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setObjectName("line_6")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setWindowModality(QtCore.Qt.NonModal)
        self.line.setGeometry(QtCore.QRect(380, 10, 20, 161))
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(0, 10, 20, 161))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_3.setMidLineWidth(1)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(80, 10, 15, 68))
        self.line_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_4.setMidLineWidth(1)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 381, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(10, 160, 383, 20))
        self.line_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_7.setMidLineWidth(1)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setObjectName("line_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(175, 110, 50, 50))
        self.pushButton_3.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_3.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_3.setStyleSheet("background-color: rgb(156, 0, 2);\n"
"border-radius: 25px\n"
"")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 170, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(6)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(87, 30, 303, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(87, 50, 303, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setGeometry(QtCore.QRect(10, 90, 383, 20))
        self.line_8.setStyleSheet("color: rgb(255, 255, 255);")
        self.line_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_8.setMidLineWidth(1)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setObjectName("line_8")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(14, 19, 71, 51))
        self.label_6.setStyleSheet("")
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("logo2.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "- YANA - Asistente COVID-19 V.1"))
        self.pushButton.setText(_translate("MainWindow", "Iniciar Asistente"))
        self.pushButton_2.setText(_translate("MainWindow", "Detener Asistente"))
        self.label.setText(_translate("MainWindow", "UNIVERSIDAD CATÓLICA DE CUENCA"))
        self.label_4.setText(_translate("MainWindow", "- YANA -"))
        self.label_5.setText(_translate("MainWindow", "Ing. Pablo Buestán Andrade MSc"))
        self.label_2.setText(_translate("MainWindow", "CIITT"))
        self.label_3.setText(_translate("MainWindow", "LABORATORIO DE SIMULACIÓN EN TIEMPO REAL"))

    def on_click(self):
        print ("boton on")
        start_assist()
        self.pushButton_3.setStyleSheet("background-color: rgb(0, 138, 34);border-radius: 25px")

    def off_click(self):    
        print ("boton off")
        stop_assist()
        self.pushButton_3.setStyleSheet("background-color: rgb(156, 0, 2);border-radius: 25px")

app = QApplication([])
window = QMainWindow()
main_window = Ui_MainWindow()
main_window.setupUi(window)
window.show()
app.exec_()
# -------------------------------------------------------------------------------
