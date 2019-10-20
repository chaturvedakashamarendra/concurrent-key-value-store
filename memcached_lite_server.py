import socket
import os
import threading
msg=""
#Implementing multithreading
class multi_request(threading.Thread):
    def __init__(self,conn,address):
        threading.Thread.__init__(self)
        self.address=address
        self.conn=conn

    def run(self):
     try:
        while True:
            msg=""
            data=self.conn.recv(2400)
            #data in string format
            st=str(data.decode())
            l=st.splitlines()
            #storing first row of data in l1
            l1=l[0].split()
            #storing value in l2
            l2=l[1:]
            command=l1[0]
            #checking the command received is "set" or "get"
            if(command=="set"):
                exp=set(l1,l2)
                if(exp==0):
                    st="STORED\r\n"
                    self.conn.send(st.encode())
                else:
                    self.conn.send("NOT-STORED\r\n".encode())
            elif(command=="get"):
                value=""
                #l1[1] contains the key
                value,exp,msg=get_value(l1[1])
                #if the value is found
                if(exp==0 and value):
                    self.conn.send(value.encode())
                else:
                #else returns value not found
                    self.conn.send(msg.encode())
     except Exception:
        pass




def check_key(key):
  msg=""
  try:
    #if file does not exist
    if(not os.path.exists("store.txt")):
        file=open("store.txt","r+")
        st=file.read()
        file.close()
    else:
        lock.acquire()
        file=open("store.txt","r+")
        st=file.read()
        file.close()
        lock.release()
    file=open("store.txt","r+")
    st=file.read()
    file.close()
    dict={}
    l=st.splitlines()
    #storing the key - value to a dictionary
    for i in l:
        st1=i.split()
        dict[st1[0]]=st1[1]
    #retrieving the value for the passed key
    value=dict.get(key)
  except FileNotFoundError:
    #if the file is not yet created
    msg="File does not exist"
    return False,msg
  return value,msg

def set(l1,l2):
    exp=0
    key=l1[1]
    value=(''.join(l2)).strip()
    #checking if the key already exists in the file
    val,msg=check_key(key)
    #if the file does not exist
    if((not(val))):
        st1=key+" "+value
        lock.acquire()
        file=open("store.txt","a+")
        file.write(st1+"\n")
        file.close()
        lock.release()
    #if file exists or if updated value of key is passed or multiple values of same key-value is passed
    else:
        lock.acquire()
        file=open("store.txt","r+")
        st=file.read()
        file.close()
        lock.release()
        dict={}
        lock.acquire()
        l=st.splitlines()
        #storing the key - value to a dictionary
        for i in l:
            st1=i.split()
            dict[st1[0]]=st1[1]
        dict[key]=value
        s=""
        for i in dict:
            s+=i+" "+dict.get(i)+"\n"
        lock.release()
        lock.acquire()
        file=open("store.txt","w")
        file.write(s)
        file.close()
        lock.release()
    return exp

def get_value(key):
 exp=0
 st1=""
 #getting the value for the key passed

 value,msg=check_key(key)
 if(value):
        #st1 represents
        st1="VALUE"+" "+key+" "+str(len(value))+"\r\n"+value+"\n\r"+"END\n\r"
 else:
        #if the value for the key passed is not present
        if(not msg):
            msg="key not present"
        exp=1
 return st1,exp,msg




host=socket.gethostname()
port=9000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
print("server is listening")
lock=threading.Lock()

while True:
    s.listen(1)
    conn,address=s.accept()
    t=multi_request(conn,address)
    print("Connection to client:", address)
    t.start()




