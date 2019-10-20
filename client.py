import socket
host=socket.gethostname()
port=9000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
st=""
while True:
    choice=input("Enter 1 if you wish to set or 2 to get the value\n")
    if(choice=="1"):
        key=input("Enter the kay to be inserted\n")
        value=input("Enter the value to be inserted\n")
        st="set"+" "+str(key)+" "+str(len(value))+"\r\n"+str(value)+"\r\n"
        print("Data sent to server is",st)
        s.send(st.encode())
        data=s.recv(2400)
        print("From server :",data.decode())
    elif(choice=="2"):
        key=input("Enter the kay \n")
        st="get"+" "+key
        s.send(st.encode())
        data=s.recv(2400)
        print("From server :",data.decode())
    else:
        break
s.close()

