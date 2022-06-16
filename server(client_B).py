import socket
import random

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = socket.gethostbyname(socket.gethostname())
PORT = 12334
listener.bind((IP, PORT))
listener.listen(0)
connection, address = listener.accept()

def generate():# функция для генерации ключей
    data=listen()
    data=data.split(":")
    g=int(data[0])
    p=int(data[1])
    A=int(data[2])

    b=random.getrandbits(128)
    B=pow(g,b,p)

    print("p (открытое простое число):", p)
    print("g (первообразный корень по модулю р):",g)
    print("b (закртытый ключ):",b)
    print("B (открытый ключ):",B)
    print("A (открытый ключ клиента А):",A)
    connection.send(str(B).encode('utf-8'))# отправляем открытые ключь клиенту А
    K=pow(A,b,p)
    print("K (секретный ключ):",K)
    data = int(listen())
    if data == K:# проверка ключей
        print("Ключи: TRUE!")
        connection.send("TRUE!".encode('utf-8'))
    else:
        print("Ключи: FALSE!")
        connection.send("FALSE!".encode('utf-8'))

def listen():# функция слушает клиента А
    while True:
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    return data

print("======================================")
print("===============Клиент В===============")
# Начало программы
generate()
print("======================================")