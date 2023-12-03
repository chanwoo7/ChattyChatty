import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QDialog
import ui_server
import socket, threading, json

class Client:
    def __init__(self, socket, nickname, port):
        self.socket = socket
        self.nickname = nickname
        self.port = port
    def __iter__(self): # dict로  변환하는 함수
        yield 'nickname', self.nickname
        yield 'port', self.port

class Room:
    number = 0
    name = ""
    clients = []
    password = ""

    # 정원?
    def __init__(self, name, password):
        global ROOM_NUMBER
        ROOM_NUMBER += 1
        self.number = ROOM_NUMBER
        self.name = name
        self.password = password

    def __iter__(self):
        yield 'number', self.number
        yield 'name', self.name
        yield 'password', self.password
        yield 'user_count', len(self.clients)

    def join(self, client):
        self.clients.append(client)  # 객체 추가
        # 정원? -> 여기서 관리 필요

    def exit(self, client):
        self.clients.remove(client)

class CustomSignal(QObject):
    updateLog = pyqtSignal(str)


class ServerDialog(QDialog, ui_server.Ui_server_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global custom_signal
        custom_signal.updateLog.connect(self.update_log)

    def update_log(self, msg):
        self.server_textEdit.append(msg)


def json_message(code, data):
    return json.dumps({'code': code, 'data': data}, ensure_ascii=False)

# 서버가 받은 메시지를 클라이언트 전체에 보내기
def broadcast(code, data):
    global custom_signal
    message = json_message(code, data)
    print("broadcast>", message)
    custom_signal.updateLog.emit(f"broadcast> {message}")
    for client in clients:
        try:
            client.socket.send(message.encode('utf-8'))
        except ConnectionResetError as e:
            print('broadcast', e)
            client.socket.close()
            clients.remove(client)
            broadcast_login_list()
            del client  # 클라이언트 객체 삭제


def broadcast_login_list():
    login_list = [dict(client) for client in clients]  # [(닉네임, 포트번호), ...]
    broadcast(3, {'login_list': login_list})  # 로그인 사용자목록(login_list) 업데이트

def broadcast_room_list():
    room_list = [dict(room) for room in rooms]
    broadcast(2, {'room_list': room_list})  # 방 목록 broadcast

def broadcast_room_info(room):
    room_dict = dict(room)
    room_dict['clients'] = [dict(c) for c in room.clients]
    message = json_message(8, {'room_info': room_dict})
    print("broadcast>", message)
    for client in room.clients:
        client.socket.send(message.encode('utf-8'))

def broadcast_room_chat(room, msg):
    global clients
    message = json_message(6, msg)
    for client in room.clients:
        client.socket.send(message.encode('utf-8'))


def handle(client):
    global custom_signal, clients, rooms

    while True:
        try:
            # 클라이언트로부터 타당한 메시지를 받았는지 확인
            message = json.loads(client.socket.recv(1024).decode('utf-8'))
            print(message)
            custom_signal.updateLog.emit(f"{client.nickname}#{client.port}> {message}")

            if message is None: # Todo: 클라이언트 연결 끊어지면 raise Exception 해줘야함.. 이렇게 맞나
                raise Exception("message 0")

            if message['code'] == 1: # 전체 채팅
                broadcast(0, (f"{client.nickname}#{client.port}: "+message['data']))
            elif message['code'] == 4: # change nickname
                client.nickname = message['data']
                broadcast_login_list()
                for room in rooms:
                    if client in room.clients:
                        broadcast_room_info(room)
                        break
            elif message['code'] == 5: # make_room
                name = message['data']['name']
                password = message['data']['password']
                room = Room(name, password)
                room.join(client) # 방장 방 들어가기
                rooms.append(room)
                broadcast_room_list()
                broadcast_room_info(room) # 방장(방만든client)한테 room_info 주기

            elif message['code'] == 6: # room chat !
                room_num = int(message['data']['room_num'])
                for room in rooms:
                    if room.number == room_num:
                            broadcast_room_chat(room, (f"{client.nickname}#{client.port}: " + message['data']['chat']))

            elif message['code'] == 7: # 방접속
                room_num = int(message['data']['room_num'])
                password = message['data']['password']
                if not room_num in [room.number for room in rooms]: # 방이 없음
                    pass
                else: # 방이 있음
                    for room in rooms:
                        if room.number == room_num:
                            if room.password == password: # 비밀번호 맞으면
                                room.join(client) # 방 접속
                                broadcast_room_list() # 방 목록 업데이트
                                broadcast_room_info(room) # 방 정보 업데이트
                            else: # 비밀번호 틀리면
                                pass
                            break

            elif message['code'] == 9: # exit_room
                room_num = message['data']
                if room_num in [room.number for room in rooms]: # 방이 있으면
                    for room in rooms:
                        if room.number == room_num:
                            room.exit(client) # 방 퇴장
                            if len(room.clients):
                                broadcast_room_info(room) # 방 정보 업데이트
                            else: # 아무도 방에 없으면 방 삭제
                                rooms.remove(room)
                                del room
                            broadcast_room_list()  # 방 목록 업데이트

            elif message['code'] == 10: # logout
                client.socket.close()
                clients.remove(client)
                broadcast_login_list()
                del client  # 클라이언트 객체 삭제
                break

        except Exception as e:
            print(e)
            # 클라이언트가 나갔으면 ( 로그아웃 ) 알림
            # broadcast(f"{client.nickname} left!\n")
            # broadcast(f"{len(clients)} people in this room!\n") # TODO: 나중에 룸 나가는곳..
            client.socket.close()
            clients.remove(client)
            broadcast_login_list()
            del client # 클라이언트 객체 삭제
            break

# 멀티 클라이언트를 받는 메서드
def receive():
    global custom_signal, clients, rooms
    while True:
        client_socket, address = server.accept()
        # 닉네임 요청
        client_socket.send(json_message(1, address[1]).encode('utf-8'))
        message = json.loads(client_socket.recv(1024).decode('utf-8'))
        nickname = message['data'] # 닉네임 설정

        client = Client(client_socket, nickname, address[1])
        clients.append(client)

        room_list = [dict(room) for room in rooms]
        client_socket.send(json_message(2, {'room_list': room_list}).encode('utf-8')) # 방 목록 1:1로 보내주기

        print(f"Connected with {nickname} {str(address)}")
        custom_signal.updateLog.emit(f"Connected with {nickname} {str(address)}")

        broadcast_login_list()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



ROOM_NUMBER = 0
clients = []
rooms = []
custom_signal = CustomSignal()
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    server_thread = threading.Thread(target=receive,)
    server_thread.start()

    app = QApplication(sys.argv)
    myWindow = ServerDialog()
    myWindow.show()
    app.exec_()