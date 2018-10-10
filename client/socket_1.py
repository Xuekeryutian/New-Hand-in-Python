import  socket
HOST = socket.gethostname()
PORT = 3434
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
print("connect %s :%d ok" % (HOST,PORT))
data = s.recv(1024)
print(" ’µΩ:",data)
s.close()