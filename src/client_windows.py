import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
import ui_main, ui_login, ui_make_room, ui_password, ui_room, ui_nickname


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    # close_signal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setNickname(self):
        self.setDisabled(True)
        self.secondWindow = NicknameDialog()
        self.secondWindow.exec()
        self.setDisabled(False)

    def showMakeRoomWindow(self):
        self.setDisabled(True)
        self.secondWindow = MakeRoomWidget()
        self.secondWindow.exec()
        self.setDisabled(False)

    def sendMessage(self):
        pass

    def showLoginWindow(self):
        self.close()
        self.secondWindow = LoginWindow()
        self.secondWindow.show()


class LoginWindow(QMainWindow, ui_login.Ui_login_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def showMainWindow(self):
        self.close()
        self.secondWindow = MainWindow()
        self.secondWindow.show()


class NicknameDialog(QDialog, ui_nickname.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def checkNickname(self):
        # 새로운 닉네임 저장 및 반영
        self.close()

    def closeDialog(self):
        self.close()


class MakeRoomWidget(QDialog, ui_make_room.Ui_make_room_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def showRoomWindow(self):
        QApplication.closeAllWindows()
        self.secondWindow = RoomWindow()
        self.secondWindow.show()


class PasswordDialog(QDialog, ui_password.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def checkPassword(self):
        pass

    def closeDialog(self):
        self.close()


class RoomWindow(QMainWindow, ui_room.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def sendMessage(self):
        pass

    def exitRoom(self):
        self.close()
        self.secondWindow = MainWindow()
        self.secondWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()