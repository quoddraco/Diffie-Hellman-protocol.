import socket
import random

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "192.168.56.1"
PORT = 12334
connection.connect((IP, PORT))


def gcd( a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def primitive_root( modulo):# функция для первообразования корня по модулю
    required_set = set(num for num in range(1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range(1, modulo))
        if required_set == actual_set:
            break
    return g


def proverka(n):# Функция разложения чисел на множители
    d=2
    a = []
    while d*d <= n:
        if n%d == 0:
            a.append(d)
            n //= d
        else:
            if d % 2 != 0:
                d += 2
            else:
                d+= 1
    if n>1:
        a.append(n)
    return a

def listen():# функция слушает клиента В
    while True:
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    return data

def generate():# функция для генерации ключей
    while True:  # Генерим простое число q
        p = random.randint(1,2**10)
        a = proverka(p)
        if len(a) == 1:
            a=int((p - 1) / 2)
            a = proverka(a)
            if len(a) == 1:
                 break

    g = primitive_root(p)
    print("p (открытое простое число):",p)
    print("g (первообразный корень по модулю р):", g)

    a=random.getrandbits(128)
    print("a (закртытый ключ):",a)

    A=pow(g,a,p)
    print("A (открытый ключ):",A)

    mess="{}:{}:{}".format(g,p,A)# отправляем открытые ключи клиенту В
    connection.send(mess.encode('utf-8'))

    B=int(listen())
    print("B (открытый ключ клиента В):",B)

    K=pow(B,a,p)
    print("K (секретный ключ):",K)

    connection.send(str(K).encode('utf-8'))# отправляем секретный ключь клиенту В на проверку
                                           # (это нежелательно делать)
    data=listen()
    print("Ключи:",data)


print("======================================")
print("===============Клиент А===============")
# Начало программы
generate()
print("======================================")