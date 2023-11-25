import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
import ui_main, ui_login, ui_make_room, ui_password, ui_room

# 로그인 - 메인 - 방만들기 - 방 간의 전환 구현 완료

class MainWindow(QMainWindow, ui_main.Ui_MainWindow):

    # close_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setNickname(self):
        pass

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


class MakeRoomWidget(QDialog, ui_make_room.Ui_make_room_widget):
    # ui_make_room -> 기존 QWidget에서 QDialog로 바꾸기

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
        pass


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