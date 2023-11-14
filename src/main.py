import sys
import time
import random
import sqlite3
import word_level_list  # Файс со словами/цитатими/уровнями

from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5 import QtCore, QtWidgets, uic

# Знаю, что можно было сделать умнее и чище(Полиморфизм?!), но теперь я понимаю, что нужно продумывать структуру заранее и писать не за 4 дня перед дедлайном :) 


class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi('typing_1.0.ui', self)
        self.connection = sqlite3.connect('userStat.db')
        self.cursor = self.connection.cursor()
        self.lineEditPractice.textEdited.connect(self.startPractice)
        self.lineEditTraining.textEdited.connect(self.startTraining)
        self.setupUi()

    def setupUi(self):
        self.Button_Training.clicked.connect(self.btn_clicked)
        self.Button_Practice.clicked.connect(self.btn_clicked)
        self.Button_Profile.clicked.connect(self.btn_clicked)
        self.Button_Restart.clicked.connect(self.btn_clicked)
        self.Button_Quote.clicked.connect(self.btn_clicked)
        self.Button_Words.clicked.connect(self.btn_clicked)
        self.Button_ClearInfo.clicked.connect(self.clear_db)

        self.level_1.clicked.connect(self.lvl_select)
        self.level_2.clicked.connect(self.lvl_select)
        self.level_3.clicked.connect(self.lvl_select)
        self.level_4.clicked.connect(self.lvl_select)
        self.level_5.clicked.connect(self.lvl_select)
        self.level_6.clicked.connect(self.lvl_select)
        self.level_7.clicked.connect(self.lvl_select)
        self.level_8.clicked.connect(self.lvl_select)
        self.level_9.clicked.connect(self.lvl_select)
        self.level_10.clicked.connect(self.lvl_select)
        self.level_11.clicked.connect(self.lvl_select)
        self.level_12.clicked.connect(self.lvl_select)
        self.level_13.clicked.connect(self.lvl_select)
        self.level_14.clicked.connect(self.lvl_select)
        self.level_15.clicked.connect(self.lvl_select)
        
        self.navigation = {
            "Button_Practice": 0,
            "Button_Training": 2,
            "Button_Profile": 3,
            "Button_Restart": 4
        }

        self.modes = {
            "Practice": self.Button_Practice,
            "Training": self.Button_Training
        }

        self.Button_Profile.click()

    def clear_db(self):
        self.cursor.execute('drop table if exists UserInf')
        self.connection.commit()
        self.Button_Profile.click()

    def lvl_select(self):
        self.creationTrainingText(self.sender().objectName())
        self.stackedWidget.setCurrentIndex(1)

    def btn_clicked(self):
        self.buttons = self.sender().objectName()
        if self.buttons == "Button_Practice":
            self.creationPracticeText()
            self.stackedWidget.setCurrentIndex(self.navigation[self.buttons])
            self.lineEditPractice.clear()
            self.textBrowserPracticeEdit.clear()
            self.lineEditPractice.setEnabled(True)
            self.lineEditPractice.setFocus()
            self.mode = "Practice"
        
        elif self.buttons == "Button_Quote":
            self.creationPracticeText(quote=True)
            self.lineEditPractice.clear()
            self.textBrowserPracticeEdit.clear()
            self.lineEditPractice.setEnabled(True)
            self.lineEditPractice.setFocus()

        elif self.buttons == "Button_Words":
            self.creationPracticeText(quote=False)
            self.lineEditPractice.clear()
            self.textBrowserPracticeEdit.clear()
            self.lineEditPractice.setEnabled(True)
            self.lineEditPractice.setFocus()

        elif self.buttons == "Button_Training":
            self.stackedWidget.setCurrentIndex(self.navigation[self.buttons])
            self.textBrowserTrainingEdit.clear()
            self.lineEditTraining.clear()
            self.lineEditTraining.setEnabled(True)
            self.mode = "Training"

        elif self.buttons == "Button_Profile":
            self.stackedWidget.setCurrentIndex(self.navigation[self.buttons])

            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserInf (
            id INTEGER PRIMARY KEY,
            typing_speed INTEGER,
            time INTEGER,
            accuracy INTEGER
            )
            ''')
            if (self.cursor.execute('SELECT * FROM UserInf').fetchall()):
                completed_tests = self.cursor.execute('SELECT COUNT(*) FROM UserInf').fetchall()[0][0]
                avg_speed = self.cursor.execute('SELECT AVG(typing_speed) FROM UserInf').fetchall()[0][0]
                time_playing = self.cursor.execute('SELECT SUM(time) FROM UserInf').fetchall()[0][0]
                max_speed = self.cursor.execute('SELECT MAX(typing_speed) FROM UserInf').fetchall()[0][0]
                avg_acc = self.cursor.execute('SELECT AVG(accuracy) FROM UserInf').fetchall()[0][0]

                self.countCompletedTests.setText(f"Выполнено тестов: {completed_tests}")
                self.averageSpeed.setText(f"Средняя скорость: {round(avg_speed, 2)} ЗВМ")
                self.timeTyping.setText(f"Время печати: {time.strftime('%H:%M:%S', time.gmtime(time_playing))}")
                self.maxSpeed.setText(f"Максимальная скорость: {round(max_speed, 2)} ЗВМ")
                self.accuracy.setText(f"Средняя точность: {round(avg_acc, 2)} %")
                return
            
            self.countCompletedTests.setText(f"Выполнено тестов: {0}")
            self.averageSpeed.setText(f"Средняя скорость: {0} ЗВМ")
            self.timeTyping.setText(f"Время печати: 00:00:00")
            self.maxSpeed.setText(f"Максимальная скорость: {0} ЗВМ")
            self.accuracy.setText(f"Средняя точность: {0} %")

        elif self.buttons == "Button_Restart":
            self.modes[self.mode].click()

    def creationPracticeText(self, quote=False):
        text = list()
        if quote:
            text.extend((random.choice(word_level_list.practice_quotes)).split())
        else:
            for _ in range(20):
                text.append(random.choice(word_level_list.practice_text))

        self.ListWords = text
        self.textBrowserPracticeSolid.setText(" ".join(self.ListWords))
        self.isTestStarted = False

    def startPractice(self):
        lineText = self.lineEditPractice.text()
        browserText = self.ListWords[0]
        if not(self.isTestStarted):
            self.startTime = time.time()
            self.incorrectWords = 0
            self.countWords = len(self.ListWords)
            self.countCharacters = 1
            self.isTestStarted = True
            return

        if not(lineText):
            return 
        
        if lineText[-1] == " ":
            if lineText[:-1] == browserText:
                self.textBrowserPracticeEdit.insertHtml(f"<span style='color:rgb(152,152,146)'>{browserText} <\span>")
            else:
                self.textBrowserPracticeEdit.insertHtml(f"<span style='color:rgb(128,62,70)'>{browserText} <\span>")
                self.incorrectWords += 1
        
            self.ListWords = self.ListWords[1:]
            self.countCharacters += len(self.lineEditPractice.text())
            self.lineEditPractice.clear()

        if not(self.ListWords):
            resultTtime = time.time() - self.startTime
            accuracy = round(((self.countWords - self.incorrectWords) / self.countWords), 2) * 100
            self.lineEditPractice.setEnabled(False)
            self.cursor.execute('INSERT INTO UserInf (typing_speed, time, accuracy) VALUES (?, ?, ?)', (round((self.countCharacters / resultTtime * 60), 2), resultTtime, accuracy))
            self.connection.commit()
            self.stackedWidget.setCurrentIndex(self.navigation["Button_Restart"])
            self.labelSpeed.setText(f"Скорость: {round((self.countCharacters / resultTtime * 60), 2)} ЗВМ")
            self.labelAccuracy.setText(f"Точность: {round(accuracy, 2)} %")
            self.labelTime.setText(f"Время: {time.strftime('%H:%M:%S', time.gmtime(resultTtime))}")
            return
        
    def creationTrainingText(self, lvl, index=0):  
        if not(index):
            self.textPrime = word_level_list.levels[lvl]
            self.levelLen = len(self.textPrime)
            self.isTestStarted = False
        self.levelText = self.textPrime[index].split()
        self.textBrowserTrainingSolid.setText(" ".join(self.levelText))
        self.lineEditTraining.setFocus()

    def startTraining(self):
        lineText = self.lineEditTraining.text()
        browserText = self.levelText[0]
        if not(self.isTestStarted):
            self.startTime = time.time()
            self.incorrectWords = 0
            self.countWords = 0
            self.countCharacters = 1
            self.isTestStarted = True
            self.index = 0
            return

        if not(lineText):
            return 
        
        if lineText[-1] == " ":
            if lineText[:-1] == browserText:
                self.textBrowserTrainingEdit.insertHtml(f"<span style='color:rgb(152,152,146)'>{browserText} <\span>")
            else:
                self.textBrowserTrainingEdit.insertHtml(f"<span style='color:rgb(128,62,70)'>{browserText} <\span>")
                self.incorrectWords += 1

            self.countWords += 1
            self.levelText = self.levelText[1:]
            self.countCharacters += len(self.lineEditTraining.text())
            self.lineEditTraining.clear()

        if not(self.levelText):
            self.index += 1
            if self.index < self.levelLen:
                self.textBrowserTrainingEdit.clear()
                self.creationTrainingText(self, index=self.index)
                return
            
            resultTtime = time.time() - self.startTime
            accuracy = round(((self.countWords - self.incorrectWords) / self.countWords), 2) * 100
            self.lineEditTraining.setEnabled(False)
            self.cursor.execute('INSERT INTO UserInf (typing_speed, time, accuracy) VALUES (?, ?, ?)', (round((self.countCharacters / resultTtime * 60), 2), resultTtime, accuracy))
            self.connection.commit()
            self.stackedWidget.setCurrentIndex(self.navigation["Button_Restart"])
            self.labelSpeed.setText(f"Скорость: {round((self.countCharacters / resultTtime * 60), 2)} ЗВМ")
            self.labelAccuracy.setText(f"Точность: {round(accuracy, 2)} %")
            self.labelTime.setText(f"Время: {time.strftime('%H:%M:%S', time.gmtime(resultTtime))}")
            return


if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
