import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QPushButton, QLabel
import ui_main, ui_login, ui_make_room, ui_password, ui_password_error, ui_room, ui_nickname

# logged-in user info
nickname = "default"
port = "9000"

# logged-in user's room info
# room_title = "default"
# room_password = ""

# sample data
login_list = [{"nickname": "소붕이", "port": 9000},
              {"nickname": "이하람", "port": 1234},
              {"nickname": "이찬우", "port": 9547},
              {"nickname": "에베벱", "port": 9345},
              {"nickname": "에헤라디야", "port": 1928}]

# 유의점: 비밀번호는 str으로! (그래야 0000 같이 반복되는 번호도 가능)
room_list = [{"name": "소붕이 모임", "user_count": 4, "number": 123, "password": "1234"},
             {"name": "안녕?", "user_count": 5, "number": 122, "password": "9876"},
             {"name": "밥밥디라라", "user_count": 7, "number": 253, "password": "0000"}]
room_info = {"name": "소붕이 모임", "user_count": 4, "number": 123, "password": 1234,
             "clients": [{"nickname": "소붕이", "port": 9000},
                         {"nickname": "이하람", "port": 1234},
                         {"nickname": "이찬우", "port": 9547},
                         {"nickname": "에베벱", "port": 9345}]}


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

        self.update_all_user_list()
        self.update_room_list()

    # 닉네임 변경 (NicknameDialog 띄움)
    def edit_nickname(self):
        self.setDisabled(True)
        self.second_window = NicknameDialog()
        self.second_window.exec()
        self.setDisabled(False)
        global nickname
        self.nickname_label.setText(nickname)

    # 방 만들기 창 띄움 (MakeRoomDialog 띄움)
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

    # 방 비밀번호 입력 창 띄움 (PasswordDialog 띄움)
    def show_password_dialog(self, password):
        self.setDisabled(True)
        self.second_window = PasswordDialog(password)
        self.second_window.exec()
        self.setDisabled(False)

    # 전역변수에서 데이터 불러옴
    def update_all_user_list(self):
        global login_list
        for user in login_list:
            self.all_users_listWidget.addItem(user["nickname"] + "#" + str(user["port"]))

    # 전역변수에서 데이터 불러옴
    def update_room_list(self):
        global room_list
        self.room_list_tableWidget.setRowCount(len(room_list))
        self.room_list_tableWidget.setColumnCount(3)
        self.room_list_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.room_list_tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("No."))
        self.room_list_tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("방 제목"))
        self.room_list_tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("인원수"))

        self.room_list_tableWidget.setColumnWidth(1, 729)

        for i in range(len(room_list)):
            # locals()['name_button_' + str(i)] = QPushButton()  # 변수를 여러 개 생성해서 해보고자 했으나 -> 실패
            self.name_button = QPushButton()
            self.name_button.setText(room_list[i]["name"])

            # FIXME: 버튼 커넥팅이 따로 되지 않고, 동일한 parameter를 매개변수로 받는 함수로 연결되는 문제
            password = room_list[i]["password"]
            self.name_button.clicked.connect(lambda: self.show_password_dialog(password))

            user_count_item = QTableWidgetItem(str(room_list[i]["user_count"]))
            user_count_item.setTextAlignment(Qt.AlignCenter)
            number_item = QTableWidgetItem(str(room_list[i]["number"]))
            number_item.setTextAlignment(Qt.AlignCenter)

            self.room_list_tableWidget.setItem(i, 0, number_item)
            self.room_list_tableWidget.setCellWidget(i, 1, self.name_button)
            self.room_list_tableWidget.setItem(i, 2, user_count_item)

        # 가장 최근에 생성된 방(방 번호가 높은 방)부터 표시되도록
        self.room_list_tableWidget.sortByColumn(0, Qt.DescendingOrder)


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
    def __init__(self, password):
        super().__init__()
        self.setupUi(self)
        self.password = password

    # 비밀번호가 맞는지 확인
    def check_password(self):
        # -----------------테스트용, 삭제예정-----------------
        print(self.password)
        print(self.password_lineEdit.text())
        # ----------------------------------------------------

        # 비밀번호가 맞을 경우
        if str(self.password) == self.password_lineEdit.text():
            QApplication.closeAllWindows()
            self.second_window = RoomWindow()
            self.second_window.show()
        # 비밀번호가 틀릴 경우
        else:
            self.setDisabled(True)
            self.second_window = PasswordErrorDialog()
            self.second_window.exec()
            self.setDisabled(False)

    def close_dialog(self):
        self.close()


class PasswordErrorDialog(QDialog, ui_password_error.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def close_dialog(self):
        self.close()


class RoomWindow(QMainWindow, ui_room.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ------- 방 생성하기를 통해 RoomWindow에 진입했을 때 사용했던 코드 -------
        # global room_title
        # self.room_title_label.setText(room_title)
        # -------------------------------------------------------------------------
        self.update_room_info()

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

    # 전역변수에서 데이터 불러옴
    def update_room_info(self):
        global room_info

        # 방 제목 설정
        self.room_title_label.setText(room_info["name"])

        # 참여자 수 설정
        self.user_count_label.setText("(" + str(room_info["user_count"]) + "명 참여 중)")

        # 참여자 테이블 설정
        self.participants_tableWidget.setRowCount(2)
        self.participants_tableWidget.setColumnCount(len(room_info["clients"]))
        self.participants_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.participants_tableWidget.setRowHeight(0, 178)
        self.participants_tableWidget.setStyleSheet("background-color: #484848;")

        for i in range(len(room_info["clients"])):
            self.participants_tableWidget.setColumnWidth(i, 162)
            self.participants_tableWidget.setCellWidget(0, i, ImgWidget("../resource/profile.png"))
            name_label = QLabel(room_info["clients"][i]["nickname"] + "#" + str(room_info["clients"][i]["port"]))
            name_label.setAlignment(QtCore.Qt.AlignCenter)
            name_label.setStyleSheet("QLabel{font-size: 15pt;}")
            self.participants_tableWidget.setCellWidget(1, i, name_label)

        self.participants_tableWidget.setCellWidget(0, 0, ImgWidget("../resource/profile.png"))


class ImgWidget(QtWidgets.QLabel):
    def __init__(self, imagePath, parent=None):
        super(ImgWidget, self).__init__(parent)

        pic = QtGui.QPixmap(imagePath).scaled(150, 150)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPixmap(pic)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    app.exec_()
