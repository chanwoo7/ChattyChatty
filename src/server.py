import socket, threading, json
class Client:
    def __init__(self, socket, nickname, port):
        self.socket = socket
        self.nickname = nickname
        self.port = port

    # # socket에 json 메시지를 만들어서 보냄
    # def send_message(self, message):
    #     self.socket.send(message)
    #
    # # socket에서 json 메시지를 읽어서 리턴
    # def recv_message(self, size):
    #     msg = self.socket.recv(size)
    #     return msg
    #
    # def __str__(self):
    #     return "" # TODO: json dump...stringify할때? 꼭 필요한가? 생각해보깅
    def __iter__(self): # dict로  변환하는 함수
        yield 'nickname', self.nickname
        yield 'port', self.port

ROOM_NUMBER = 0
class Room:
    number=0
    name=""
    clients=[]
    password=""
    # 정원?
    def __init__(self, name, password):
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
        clients.append((client)) # 객체 추가
        # 정원? -> 여기서 관리 필요

    def exit(self, client):
        clients.remove(client)


host = '127.0.0.1'
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
rooms = []

def json_message(code, data):
    return json.dumps({'code': code, 'data': data}, ensure_ascii=False)

# 서버가 받은 메시지를 클라이언트 전체에 보내기
def broadcast(code, data):
    message = json_message(code, data)
    print("broadcast>", message)
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
    message = json_message(8, {'room_info': dict(room)})
    for client in room.clients:
        client.socket.send(message.encode('utf-8'))


def handle(client):
    while True:
        try:
            # 클라이언트로부터 타당한 메시지를 받았는지 확인
            message = json.loads(client.socket.recv(1024).decode('utf-8'))
            print(message)

            if message is None: # Todo: 클라이언트 연결 끊어지면 raise Exception 해줘야함.. 이렇게 맞나
                raise Exception("message 0")

            if message['code'] == 1: # FIXME: 전체 브로드캐스트 (확성기)
                # 브로드캐스트 함수 동작
                broadcast(0, (f"{client.nickname}:"+message['data']))
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
                broadcast_room_list()
                broadcast_room_info(room) # ==방장(방만든client)한테 room_info 주기
            elif message['code'] == 7: # 방접속
                room_num = int(message['data']['room_num'])
                password = message['data']['password']


                if not room_num in [room.number for room in rooms]:
                    # todo 방이 없으면 접근 실패알림 ???? 가능한가? room_info를 특이하게 줘서 실패나 퇴장인거를 알수있게 할까
                    pass
                else: # 방이 있음
                    for room in rooms:
                        if room.number == room_num:
                            if room.password == password: # 비밀번호 맞으면
                                room.join(client) # 방 접속
                                broadcast_room_list() # 방 목록 업데이트
                                broadcast_room_info(room) # 방 정보 업데이트  # todo 접근 성공 알림 ????? 일단 broadcast_room_info()로만
                                # todo ~가 입장했습니다 이거는 안댐,, 안내 문구를 같이 보내게 만들까??
                            else: # 비밀번호 틀리면
                                pass
                                # todo 접근 실패알림 ???? 이거 가능한가?
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
        while True:
            client_socket, address = server.accept()
            print(f"Connected with {str(address)}")
            # 닉네임 요청
            client_socket.send(json_message(1, address[1]).encode('utf-8'))
            message = json.loads(client_socket.recv(1024).decode('utf-8'))
            nickname = message['data'] # 닉네임 설정

            client = Client(client_socket, nickname, address[1])
            clients.append(client)

            room_list = [dict(room) for room in rooms]
            client_socket.send(json_message(2, {'room_list': room_list}).encode('utf-8')) # 방 목록 1:1로 보내주기

            broadcast_login_list()
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()


receive()
