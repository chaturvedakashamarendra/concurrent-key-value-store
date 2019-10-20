import socket
import time
host=socket.gethostname()
port=9000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
while True:
    st="set"+" "+str("m")+" "+str(2)+"\r\n"+str("hello")+"\r\n"
    start=time.process_time()
    s.send(st.encode())
    data =  s.recv(1024)
    end=time.process_time()
    print("Total response time",(end-start))
    print("From Server :" ,data.decode())
s.close()

