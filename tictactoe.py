from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject
import numpy
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QApplication, QHBoxLayout
import pickle
import random
from bot_player import *
USE_AI = True

class resetButton(QtWidgets.QToolButton):
    def __init__(self, UI, Frame, *_args):
        super().__init__(Frame)
        self.UI = UI
        self.clicked.connect(self.action)

    def action(self):
        self.UI.reset()
        self.UI.show_turn()

class loadButton(QtWidgets.QToolButton):
    def __init__(self, UI, Frame, *_args):
        super().__init__(Frame)
        self.UI = UI
        self.clicked.connect(self.action)

    def action(self):
        with open("state.pkl", "rb") as pf:
            self.UI.text_vals = pickle.load(pf)
        self.UI.load_state()
        print("Loaded")
        self.UI.show_turn()


class saveButton(QtWidgets.QToolButton):
    def __init__(self, UI, Frame, *_args):
        super().__init__(Frame)
        self.UI = UI
        self.clicked.connect(self.action)

    def action(self):
        with open("state.pkl", "wb+") as pf:
            pickle.dump(self.UI.text_vals, pf)
        print("Saved")
        self.UI.show_turn()


class myButton(QtWidgets.QPushButton):
    def __init__(self, UI, Frame, *__args):
        super().__init__(Frame)
        self.setStyleSheet("background:grey")
        self.UI = UI
        self.clicked.connect(self.action)

    def action(self):
        if self.text() == "---":
            if self.UI.turn == True:
                self.setText("X")
            else:
                self.setText("O")
            self.UI.left_num+=1
            self.UI.clicker()
        else:
            print("Already set")
        self.UI.show_turn()


class Ui_Frame(object):
    DONE = False
    turn = True
    left_num = 0
    players = ["X", "O"]
    text_vals = [["---","---","---"] for x in range(3)]

    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(476, 409)
        Frame.setMinimumSize(QtCore.QSize(476, 409))
        Frame.setMaximumSize(QtCore.QSize(476, 500))
        self.space = myButton(self, Frame)
        self.space.setGeometry(QtCore.QRect(40, 100, 121, 91))

        self.space.setObjectName("pushButton")
        self.space_2 = myButton(self,Frame)
        self.space_2.setGeometry(QtCore.QRect(180, 100, 121, 91))

        self.space_2.setObjectName("pushButton_2")
        self.space_3 = myButton(self,Frame)
        self.space_3.setGeometry(QtCore.QRect(320, 100, 121, 91))
        self.space_3.setObjectName("pushButton_3")

        self.space_4 = myButton(self,Frame)
        self.space_4.setGeometry(QtCore.QRect(40, 210, 121, 91))
        self.space_4.setObjectName("pushButton_4")

        self.space_5 = myButton(self,Frame)
        self.space_5.setGeometry(QtCore.QRect(180, 210, 121, 91))
        self.space_5.setObjectName("pushButton_5")

        self.space_6 = myButton(self,Frame)
        self.space_6.setGeometry(QtCore.QRect(320, 210, 121, 91))
        self.space_6.setObjectName("pushButton_6")

        self.space_7 = myButton(self,Frame)
        self.space_7.setGeometry(QtCore.QRect(40, 320, 121, 91))

        self.space_7.setObjectName("pushButton_7")
        self.space_8 = myButton(self,Frame)
        self.space_8.setGeometry(QtCore.QRect(180, 320, 121, 91))

        self.space_8.setObjectName("pushButton_8")
        self.space_9 = myButton(self,Frame)
        self.space_9.setGeometry(QtCore.QRect(320, 320, 121, 91))
        self.space_9.setObjectName("pushButton_9")

        self.buttons = [self.space, self.space_2, self.space_3, self.space_4 , self.space_5, self.space_6, self.space_7, self.space_8, self.space_9]

        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(200, 30, 100, 30))

        self.save = saveButton(self, Frame)
        self.save.setText("Save")
        self.load = loadButton(self, Frame)
        self.load.setText("Load")

        self.reset_button = resetButton(self, Frame)
        self.reset_button.setText("Reset")
        self.save.move(10,10)
        self.load.move(50,10)
        self.reset_button.move(90,10)

        self.label2 = QtWidgets.QLabel(Frame)
        self.label2.setGeometry(QtCore.QRect(350, 30, 81, 16))
        self.label.setObjectName("label")

        self.label2.setText("Go -> ")
        self.label2.setStyleSheet('font:  16pt "Chalkboard"; color:#f70000')

        self.xLabel = QtWidgets.QLabel(Frame)
        xpix = QPixmap("Resources/x.png")
        self.xLabel.setPixmap(xpix.scaledToHeight(50))
        self.xLabel.move(400, 15)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)
        self.board = [[self.space, self.space_2, self.space_3], [self.space_4 , self.space_5, self.space_6], [self.space_7, self.space_8, self.space_9]]

    def clicker(self):
        board_vals = []
        for x in self.board:
            vals = []
            for button in x:
                vals.append(button.text())
            board_vals.append(vals)
        self.turn = not self.turn
        if self.left_num >= len(self.buttons):
            self.showdialog("TIE!!", "CATS GAME\n(No More Spaces Available)")
        else:
            self.check_board(board_vals)
        self.text_vals = board_vals


    def check(self, result, location, num):
        if len(set(result))==1 and result[0] != "---":
            self.showdialog(f'Player {result[0]} has won the game.',f'{location} {num}')
            self.DONE = True
            return True


    def check_board(self, vals):
        diag1 = []
        diag2 = []
        diag1_buttons = []
        diag2_buttons = []
        for i in range(3):
            row = []
            col = []
            diag1.append(vals[i][i])
            diag2.append(vals[2-i][i])
            for j in range(3):
                row.append(vals[i][j])
                col.append(vals[j][i])
            if self.check(row, "ROW", i+1) or self.check(col, "COLUMN", i+1):
                return True
        if self.check(diag1, "DIAGONAL", 1) or self.check(diag2, "DIAGONAL", 2):
            return True
        return False

    def showdialog(self, s, sd):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(s)
        msg.setInformativeText("Play Again?")
        msg.setWindowTitle("Play Again?")
        msg.setDetailedText("Winner on: "+sd)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()

    def reset(self):
        self.DONE = False
        self.left_num=0
        for x in self.buttons:
            x.setText("---")
        self.turn=True
        self.show_turn()

    def msgbtn(self, i):
        if i.text() == "OK":
            self.reset()
        else:
            QApplication.quit()

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.space.setText(_translate("Frame", "---"))
        self.space_2.setText(_translate("Frame", "---"))
        self.space_3.setText(_translate("Frame", "---"))
        self.space_4.setText(_translate("Frame", "---"))
        self.space_5.setText(_translate("Frame", "---"))
        self.space_6.setText(_translate("Frame", "---"))
        self.space_7.setText(_translate("Frame", "---"))
        self.space_8.setText(_translate("Frame", "---"))
        self.space_9.setText(_translate("Frame", "---"))
        self.label.setText(_translate("Frame", "Tic-Tac-Toe"))
        self.label.setStyleSheet('font:  20pt "Chalkboard"; color:#f70000')

    def load_state(self):
        self.left_num=0
        for i in range(3):
            for j in range(3):
                self.board[i][j].setText(self.text_vals[i][j])
                if self.text_vals[i][j] != "---":
                    self.left_num+=1
        self.show_turn()
        self.check_board(self.text_vals)

    def reload_board(self):
        board_vals = []
        for x in self.board:
            vals = []
            for button in x:
                vals.append(button.text())
            board_vals.append(vals)
        self.text_vals = board_vals

    def bot_move(self):
        self.reload_board()
        board = get_board(self.text_vals)
        depth = 9-self.left_num
        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = minimax(board, depth, COMP)
            x, y = move[0], move[1]
        print(f"{x},{y}")
        self.board[x][y].click()

    def show_turn(self):
        npa = numpy.array(self.text_vals).flatten()
        xc = list(npa).count("X")
        oc = list(npa).count("O")
        if self.left_num ==0:
            self.turn=True
        elif oc>=xc:
            self.turn = True
        elif xc>oc:
            self.turn = False

        if self.turn or self.left_num==0:
            xpix = QPixmap("Resources/x.png")
            if USE_AI:
                self.text_vals = [["---", "---", "---"] for x in range(3)]
                self.bot_move()
        else:
            xpix = QPixmap("Resources/o.png")
        self.xLabel.setPixmap(xpix.scaledToHeight(50))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    ui.show_turn()
    sys.exit(app.exec_())
