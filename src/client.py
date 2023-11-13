import socket, threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
# print(client)
# <socket.socket fd=1160, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0,
# laddr=('127.0.0.1', 53517), raddr=('127.0.0.1', 9999)
nickname = input("Choose your nickname: ")


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "":
                raise Exception("message 0")

            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print("An error occured!", e)
            client.close()
            break


def write():
    while True:
        message = f'{input("")}'
        client.send(message.encode('utf-8'))


# 멀티 클라이언트용 쓰레드
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 메시지 보내기
write_thread = threading.Thread(target=write)
write_thread.start()
