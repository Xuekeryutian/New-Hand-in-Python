import socket
import datetime



HOST = socket.gethostname()

PORT = 3434
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)

while True:
    conn,addr = s.accept()
    print('Client %s connected!' % str(addr))
    dt = datetime.datetime.now()
    message = "当前时间为:"+ str(dt)
    conn.send(message)
    print("sent:",message)
    conn.close()