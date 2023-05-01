import sys, socket
from ServerWorker import ServerWorker
class Server:
    def main(self):
        try:
            SERVER_PORT = int(sys.argv[1])
        except:
            print (["Usage:",Server.py, Server_port])
            rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rtspSocket.bind(('', SERVER_PORT))
            print ("RTSP Listing incoming request...")
            rtspSocket.listen(5)
        while True:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept() 

            ServerWorker(clientInfo).run()

            if __name__ == "__main__":
                (Server()).main()