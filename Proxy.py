from socket import *
import sys
if len(sys.argv) <= 0:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerPort = 8888
tcpSerSock.bind(('127.0.0.1',tcpSerPort))
tcpSerSock.listen(1)
while 1:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode( )
    if message.split()[1]==None:
        continue
    if message.split()[1]!='/www.google.com':
        continue
    if message.split()[1]=='/favicon.ico':
        continue
    print(message)
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        for i in range(0,len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        tcpCliSock.send("\r\n".encode())
        tcpCliSock.close()
        f.close()
        print('Read from cache')
    except IOError:
        if fileExist == "false":
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                c.connect((hostn,80))
                print ('Socket connected to port 80 of the host')
                buff="GET"+' /'+" HTTP/1.1\r\n\r\n"
                c.send(buff.encode())
                recv = c.recv(15000000)
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(recv)
                print('successfully save')
                tcpCliSock.send(recv)
            except:
                print("Illegal request")
        else:
            status_line='HTTP/1.1 404 Not Found'
            connectionSocket.send(status_line.encode())
            connectionSocket.close()
    tcpCliSock.close()
tcpSerSock.close()