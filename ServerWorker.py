import random, math
import time
from random import randint
import sys, traceback, threading, socket
from VideoStream import VideoStream
from RtpPacket import RtpPacket
class ServerWorker:
    SETUP = 'SETUP'
    PLAY = 'PLAY'
    PAUSE = 'PAUSE'
    TEARDOWN = 'TEARDOWN'
    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT
    OK_200 = 0
    FILE_NOT_FOUND_404 = 1
    CON_ERR_500 = 2
    clientInfo = {}
def __init__(self, clientInfo):
    self.clientInfo = clientInfo
def run(self):
    threading.Thread(target=self.recvRtspRequest).start()
def recvRtspRequest(self):
    """Receive RTSP request from the client."""
    connSocket = self.clientInfo['rtspSocket'][0]
    while True:
        data = connSocket.recv(256) ###
        if data:
            print ('-'*60 + "\nData received:" + '-'*60)
            self.processRtspRequest(data)
def processRtspRequest(self, data):
    """Process RTSP request sent from the client."""
    request = data.split('\n')
    line1 = request[0].split(' ')
    requestType = line1[0]
    filename = line1[1]
    seq = request[1].split(' ')
    if requestType == self.SETUP:
        if self.state == self.INIT:
            print ("SETUP Request received")
        try:
            self.clientInfo['videoStream'] = VideoStream(filename)
            self.state = self.READY
        except IOError:
            self.replyRtsp(self.FILE_NOT_FOUND_404, seq[1])
            self.clientInfo['session'] = randint(100000, 999999)
            self.replyRtsp(self.OK_200, seq[0]) 
            print ("sequenceNum is " + seq[0])
            self.clientInfo['rtpPort'] = request[2].split(' ')[3]
            print ('-'*60 + "\nrtpPort is :" + self.clientInfo['rtpPort'] + "\n" + '-'*60)
            print ("filename is " + filename)
    elif requestType == self.PLAY:
        if self.state == self.READY:
            print ("-"*60 + "PLAY Request Received" + "-"*60)
            self.state = self.PLAYING
            self.clientInfo["rtpSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.replyRtsp(self.OK_200, seq[0])
            print ("-"*60 + "\nSequence Number ("+ seq[0] + ")\nReplied to client\n" + "-"*60)
            self.clientInfo['event'] = threading.Event()
            self.clientInfo['worker']= threading.Thread(target=self.sendRtp)
            self.clientInfo['worker'].start()
    elif self.state == self.PAUSE:
        print ("-"*60 + "\nRESUME Request Received\n" + "-"*60)
        self.state = self.PLAYING
    elif requestType == self.PAUSE:
        if self.state == self.PLAYING:
            print ("-"*60 + "\nPAUSE Request Received\n" + "-"*60)
            self.state = self.READY
            self.clientInfo['event'].set()
            self.replyRtsp(self.OK_200, seq[0])
    elif requestType == self.TEARDOWN:
        print ("-"*60 + "\nTEARDOWN Request Received\n" + "-"*60)
        self.clientInfo['event'].set()
        self.replyRtsp(self.OK_200, seq[0])
        self.clientInfo['rtpSocket'].close()
def sendRtp(self):
    """Send RTP packets over UDP."""
    counter = 0
    threshold = 10
    while True:
        jit = math.floor(random.uniform(-13,5.99))
        jit = jit / 1000
        self.clientInfo['event'].wait(0.05 + jit)
        jit = jit + 0.020
        if self.clientInfo['event'].isSet():
            break
            data = self.clientInfo['videoStream'].nextFrame()
            if data:
                frameNumber = self.clientInfo['videoStream'].frameNbr()
            try:
                port = int(self.clientInfo['rtpPort'])
                prb = math.floor(random.uniform(1,100))
                if prb > 5.0:
                    self.clientInfo['rtpSocket'].sendto(self.makeRtp(data, frameNumber),(self.clientInfo['rtspSocket'][1][0],port))
                    counter += 1
                    time.sleep(jit)
            except:
                print ("Connection Error")
                print ("-"*60)
                traceback.print_exc(file=sys.stdout)
                print ("-"*60)
def makeRtp(self, payload, frameNbr):
    """RTP-packetize the video data."""
    version = 2
    padding = 0
    extension = 0
    cc = 0
    marker = 0
    pt = 26 
    seqnum = frameNbr
    ssrc = 0
    rtpPacket = RtpPacket()
    rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)
    return rtpPacket.getPacket()
def replyRtsp(self, code, seq):
    """Send RTSP reply to the client."""
    if code == self.OK_200:
        reply = 'RTSP/1.0 200 OK\nCSeq: ' + seq + '\nSession: ' + str(self.clientInfo['session'])
        connSocket = self.clientInfo['rtspSocket'][0]
        connSocket.send(reply)
    elif code == self.FILE_NOT_FOUND_404:
        print ("404 NOT FOUND")
    elif code == self.CON_ERR_500:
        print ("500 CONNECTION ERROR")