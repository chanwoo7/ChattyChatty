import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
import ui_main, ui_login, ui_make_room, ui_password, ui_room, ui_server


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # main = ui_main.Ui_MainWindow()
        # main.setupUi(self)
        self.setupUi(self)

    def setNickname(self):
        pass

    def showMakeRoomWindow(self):
        pass

    def sendMessage(self):
        pass


class LoginWindow(QMainWindow, ui_login.Ui_login_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def showRoomWindow(self):
        pass


class MakeRoomWidget(QWidget, ui_make_room.Ui_make_room_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def showRoomWindow(self):
        pass


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
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # myWindow = MainWindow()
    # myWindow = LoginWindow()
    # myWindow = MakeRoomWidget()
    myWindow = PasswordDialog()
    # myWindow = RoomWindow()
    myWindow.show()
    app.exec_()