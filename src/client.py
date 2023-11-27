import socket, threading, json


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
# print(client)
# <socket.socket fd=1160, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0,
# laddr=('127.0.0.1', 53517), raddr=('127.0.0.1', 9999)
nickname = input("Choose your nickname: ")

login_list = []
room_list = []
room_info = {}

def json_message(code, data):
    return json.dumps({'code': code, 'data': data}, ensure_ascii=False)

def receive():
    while True:
        try:
            message = json.loads(client.recv(1024).decode('utf-8'))

            if message == "":
                raise Exception("message 0")

            if message['code'] == 0: # broadcast 함수를 통한 전체공지
                print("전체> ", message['data'])

            elif message['code'] == 1: # 서버에서 닉네임 요청
                message = json_message(1, nickname)
                client.send(message.encode('utf-8'))
            elif message['code'] == 2: # 서버에서 룸리스트 보내줌
                room_list = message['data']['room_list']
                print('room_list', room_list)
            elif message['code'] == 3: # 서버에서 로그인리스트 보내줌
                login_list = message['data']['login_list']
                print('login_list', login_list)

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
        print('what you wrote:', code, message)
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
