import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import ui_main, ui_login, ui_make_room, ui_password, ui_room, ui_nickname


# TODO: 모든 카멜 케이스 -> 스네이크 케이스로 변환
# TODO: Room 클래스 생성하고 그에 맞는 구현 ㄱㄱ

# 테스트를 위해 임의로 만든 유저 클래스
class User:
    def __init__(self):
        self.nickname = "default"
        self.port = "default"

    def set_nickname(self, nickname):
        self.nickname = nickname

    def set_port(self, port):
        self.port = port


class Room:
    def __init__(self):
        self.title = "default"
        self.password = ""

    def set_title(self, title):
        self.title = title

    def set_password(self, password):
        self.password = password


class LoginWindow(QMainWindow, ui_login.Ui_login_window):

    def __init__(self, login_user):
        super().__init__()
        self.setupUi(self)
        self.login_user = login_user

    # 로그인
    def show_main_window(self):
        self.close()
        self.login_user.set_nickname(self.login_nickname_lineEdit.text())
        self.second_window = MainWindow(self.login_user)
        self.second_window.show()


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, login_user):
        super().__init__()
        self.setupUi(self)
        self.login_user = login_user
        self.nickname_label.setText(login_user.nickname)
        self.port_number_label.setText("#" + str(login_user.port))

    def setNickname(self):
        self.setDisabled(True)
        self.second_window = NicknameDialog(self.login_user)
        self.second_window.exec()
        self.setDisabled(False)
        self.nickname_label.setText(self.login_user.nickname)

    def showMakeRoomWindow(self):
        self.setDisabled(True)
        self.second_window = MakeRoomDialog(self.login_user)
        self.second_window.exec()
        self.setDisabled(False)

    # 로비에 메시지 전송
    def sendMessage(self):
        self.chatting_textBrowser.append(f"<b>[{self.login_user.nickname}#{self.login_user.port}]</b> "
                                         + self.message_lineEdit.text())
        self.message_lineEdit.clear()

    # 로그아웃
    def showLoginWindow(self):
        self.close()
        self.second_window = LoginWindow(self.login_user)
        self.second_window.show()


class NicknameDialog(QDialog, ui_nickname.Ui_Dialog):
    def __init__(self, login_user):
        super().__init__()
        self.setupUi(self)
        self.login_user = login_user

    def checkNickname(self):
        # 새로운 닉네임 저장
        self.login_user.set_nickname(self.new_nickname_lineEdit.text())
        self.new_nickname_lineEdit.clear()

        self.close()

    def closeDialog(self):
        self.close()


class MakeRoomDialog(QDialog, ui_make_room.Ui_make_room_Dialog):
    def __init__(self, login_user):
        super().__init__()
        self.setupUi(self)
        self.login_user = login_user
        self.current_room = Room()

    def showRoomWindow(self):
        QApplication.closeAllWindows()
        self.current_room.set_title(self.room_title_lineEdit.text())
        self.current_room.set_password(self.password_lineEdit.text())
        self.second_window = RoomWindow(self.login_user, self.current_room)
        self.second_window.show()


class PasswordDialog(QDialog, ui_password.Ui_Dialog):
    def __init__(self, login_user):
        super().__init__()
        self.setupUi(self)
        self.login_user = login_user

    def checkPassword(self):
        pass

    def closeDialog(self):
        self.close()


class RoomWindow(QMainWindow, ui_room.Ui_MainWindow):

    def __init__(self, login_user, current_room):
        super().__init__()
        self.setupUi(self)
        self.login_user = login_user
        self.current_room = current_room
        self.room_title_label.setText(current_room.title)

    def sendMessage(self):
        self.chatting_textBrowser.append(f"<b>[{self.login_user.nickname}#{self.login_user.port}]</b> "
                                         + self.message_lineEdit.text())
        self.message_lineEdit.clear()

    def exitRoom(self):
        self.close()
        self.second_window = MainWindow(self.login_user)
        self.second_window.show()


if __name__ == "__main__":
    user = User()
    user.set_port(1234)

    app = QApplication(sys.argv)
    myWindow = LoginWindow(user)
    myWindow.show()
    app.exec_()
