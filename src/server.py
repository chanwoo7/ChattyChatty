import socket, threading, json

class Client:
    def __init__(self, socket, nickname):
        self.socket = socket
        self.nickname = nickname

    # socket에 json 메시지를 만들어서 보냄
    def send_message(self, message):
        self.socket.send(message)

    # socket에서 json 메시지를 읽어서 리턴
    def recv_message(self, size):
        msg = self.socket.recv(size)
        return msg

    def __str__(self):
        return "" # TODO: json dump...stringify할때? 꼭 필요한가? 생각해보깅

host = '127.0.0.1'
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []


# 서버가 받은 메시지를 클라이언트 전체에 보내기
def broadcast(message):
    for client in clients:
        print("broadcast>", message)
        d = {'code': 1, "data": message}
        message = json.dumps(d, ensure_ascii=False)
        client.socket.send(message.encode('utf-8'))
        # TODO: exception handling..
        #  클라이언트 끊기면
        #  ConnectionResetError: [WinError 10054] 현재 연결은 원격 호스트에 의해 강제로 끊겼습니다 에러뜸
        #  클라이언트 정리해주기...


def handle(client):
    while True:
        try:
            # 클라이언트로부터 타당한 메시지를 받았는지 확인
            message = client.socket.recv(1024).decode('utf-8')

            # print(message)
            # print(type(message))
            if message == "": # 클라이언트 연결 끊어지면 raise Exception 해줘야함
                raise Exception("message 0")
            # 브로드캐스트 함수 동작
            broadcast((f"{client.nickname}:"+message))

        except Exception as e:
            print(e)
            # 클라이언트가 나갔으면 ( 로그아웃 ) 알림
            broadcast(f"{client.nickname} left!\n")
            broadcast(f"{len(clients)} people in this room!\n") # TODO: 나중에 룸 나가는곳에 써먹기
            client.socket.close()
            clients.remove(client)
            del client # 클라이언트 객체 삭제
            break


# 멀티 클라이언트를 받는 메서드
def receive():
        while True:
            client_socket, address = server.accept()
            print(f"Connected with {str(address)}")
            client_socket.send('NICKNAME'.encode('utf-8'))
            nickname = client_socket.recv(1024).decode('utf-8')

            client = Client(client_socket, nickname)
            clients.append(client)
            print(f"Nickname is {nickname}")
            broadcast(f"{nickname} joined!\n")
            broadcast(f"{len(clients)} people in this room!\n")
            client_socket.send('Connected to server!'.encode('utf-8'))
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

receive()
