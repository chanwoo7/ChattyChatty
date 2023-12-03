from PyQt5.QtCore import pyqtSignal, QObject
import socket, threading, json

class CustomSignal(QObject):
    broadcast = pyqtSignal(str)
    update_login_list = pyqtSignal()
    update_room_list = pyqtSignal()
    update_room_info = pyqtSignal()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
# print(client)
# <socket.socket fd=1160, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0,
# laddr=('127.0.0.1', 53517), raddr=('127.0.0.1', 9999)
nickname = input("Choose your nickname: ")
port=0

login_list = []
room_list = []
room_info = {}

custom_signal=CustomSignal()

def json_message(code, data):
    return json.dumps({'code': code, 'data': data}, ensure_ascii=False)

def receive():
    global nickname, port, client, login_list, room_list, room_info, custom_signal
    while True:
        try:
            message = json.loads(client.recv(1024).decode('utf-8'))

            if message == "":
                raise Exception("message 0")

            if message['code'] == 0: # broadcast 함수를 통한 전체 메시지
                print(message['data'])
                custom_signal.broadcast.emit(message['data'])

            elif message['code'] == 1: # 서버에서 닉네임 요청
                port = message['data']
                message = json_message(1, nickname)
                client.send(message.encode('utf-8'))

            elif message['code'] == 2: # 서버에서 룸리스트 보내줌
                room_list = message['data']['room_list']
                print('room_list', room_list)
                custom_signal.update_room_list.emit()

            elif message['code'] == 3: # 서버에서 로그인리스트 보내줌
                login_list = message['data']['login_list']
                print('login_list', login_list)
                custom_signal.update_login_list.emit()

            elif message['code'] == 6: # room chat!

            elif message['code'] == 8: # 서버에서 room_info 보내줌
                room_info = message['data']['room_info']
                print('room_info', room_info)
                custom_signal.update_room_info.emit()

            else:
                print(message)

        except Exception as e:
            print("An error occured!", e)
            client.close()
            break


def write():
    while True:
        code = f'{input("code:")}'
        message = f'{input("message:")}'
        # print('what you wrote:', code, message)
        message = json_message(int(code), message)

        if message=="exit":
            break

        client.send(message.encode('utf-8'))


# 멀티 클라이언트용 쓰레드
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 메시지 보내기
write_thread = threading.Thread(target=write)
write_thread.start()
