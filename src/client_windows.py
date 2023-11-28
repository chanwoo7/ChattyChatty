import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import ui_main, ui_login, ui_make_room, ui_password, ui_room, ui_nickname

# TODO: 전체 접속자 목록에 추가되도록
# TODO: 방 목록에 방 추가되도록
# TODO: 방 내부 window의 유저 목록에 접속자 추가되도록

# sample
login_list = []
room_list = []
room_info = {}

# logged-in user info
nickname = "default"
port = "9000"

# logged-in user's room info
room_title = "default"
room_password = ""


class LoginWindow(QMainWindow, ui_login.Ui_login_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 로그인 (MainWindow로 이동)
    def login(self):
        self.close()
        global nickname
        nickname = self.login_nickname_lineEdit.text()
        self.second_window = MainWindow()
        self.second_window.show()


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        global nickname, port
        self.nickname_label.setText(nickname)
        self.port_number_label.setText("#" + str(port))

    # 닉네임 변경 (NicknameDialog 띄움)
    def edit_nickname(self):
        self.setDisabled(True)
        self.second_window = NicknameDialog()
        self.second_window.exec()
        self.setDisabled(False)
        global nickname
        self.nickname_label.setText(nickname)

    # 방 만들기 창으로 이동 (MakeRoomDialog 띄움)
    def show_make_room_dialog(self):
        self.setDisabled(True)
        self.second_window = MakeRoomDialog()
        self.second_window.exec()
        self.setDisabled(False)

    # 로비에 메시지 전송
    def send_message(self):
        global nickname, port
        self.chatting_textBrowser.append(f"<b>[{nickname}#{port}]</b> " + self.message_lineEdit.text())
        self.message_lineEdit.clear()

    # 로그아웃 (LoginWindow로 이동)
    def logout(self):
        self.close()
        self.second_window = LoginWindow()
        self.second_window.show()


class NicknameDialog(QDialog, ui_nickname.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 새로운 닉네임 저장
    def save_nickname(self):
        global nickname
        nickname = self.new_nickname_lineEdit.text()
        self.new_nickname_lineEdit.clear()
        self.close()

    def close_dialog(self):
        self.close()


class MakeRoomDialog(QDialog, ui_make_room.Ui_make_room_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 방 생성 (RoomWindow로 이동)
    def make_room(self):
        QApplication.closeAllWindows()
        global room_title, room_password
        room_title = self.room_title_lineEdit.text()
        room_password = self.password_lineEdit.text()
        self.second_window = RoomWindow()
        self.second_window.show()


class PasswordDialog(QDialog, ui_password.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 비밀번호가 맞는지 확인
    def check_password(self):
        # TODO: 비밀번호가 맞는지 확인하고, 맞을/틀릴 경우 핸들링
        pass

    def close_dialog(self):
        self.close()


class RoomWindow(QMainWindow, ui_room.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global room_title
        self.room_title_label.setText(room_title)

    # 메시지 전송
    def send_message(self):
        global nickname, port
        self.chatting_textBrowser.append(f"<b>[{nickname}#{port}]</b> " + self.message_lineEdit.text())
        self.message_lineEdit.clear()

    # 방 나가기 (MainWindow로 이동)
    def exit_room(self):
        self.close()
        self.second_window = MainWindow()
        self.second_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
