# -*- coding: UTF-8 -*-

import socket
import time
import threading

m_Vars = {
    "bufLen" : 1024 * 100,
    "defaultServerIp" : "192.168.20.9",
    "defaultServerPort" : 8682,
    "defaultTestUrl" : "rtsp://192.168.20.9:8682/live=402894895ad2b27e015ad791a8e40014&token=f45917fdb48e0513ffd6ed7e9082b2c1",
    "defaultUserAgent" : "Rtsp Player",
    "GUID":"00000000-0000-0000-0000-000000000000"
}

def genmsg_OPTIONS(GUID ,url,seq,userAgent):
    
    
    msgRet = "OPTIONS " + url + " RTSP/1.0\r\n"
    msgRet += "ClientID: RTSP Player\r\n"
    msgRet += "GUID:" + GUID+ "\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "\r\n"
    return msgRet

def genmsg_DESCRIBE(url,seq,userAgent):
    msgRet = "DESCRIBE " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Accept: application/sdp\r\n"
    msgRet += "\r\n"
    return msgRet

def genmsg_SETUP(url,seq,userAgent):
    msgRet = "SETUP " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Transport: RTP/AVP/TCP;mode=play\r\n"   
    msgRet += "\r\n"
    return msgRet

def genmsg_PLAY(url,seq,userAgent,sessionId):
    msgRet = "PLAY " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Session: " + sessionId + "\r\n"
    msgRet += "\r\n"
    return msgRet

def decodeMsg(strContent):
    tostr = strContent.decode("gb2312")
    mapRetInf = {}        
    for m in [elem for elem in tostr.split("\n") if len(elem) > 1][2:-1]:
        #print str
        tmp2 = m.split(":")
        mapRetInf[tmp2[0]]=tmp2[1][:-1]       
    return mapRetInf
    

def start():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((m_Vars["defaultServerIp"],m_Vars["defaultServerPort"]))    
    seq  = 1
    
    str0 =  genmsg_OPTIONS(m_Vars["GUID"],m_Vars["defaultTestUrl"],seq,m_Vars["defaultUserAgent"])
    #print (str0)
    
    s.send(str0.encode(encoding='utf_8', errors='strict'))
    print (s.recv(m_Vars["bufLen"]))
    seq = seq + 1
    
    str1 = genmsg_DESCRIBE(m_Vars["defaultTestUrl"],seq,m_Vars["defaultUserAgent"])
    s.send(str1.encode(encoding='utf_8', errors='strict'))
    msg1 = s.recv(m_Vars["bufLen"])
    print (msg1 )   
    seq = seq + 1
    str2 = genmsg_SETUP(m_Vars["defaultTestUrl"],seq,m_Vars["defaultUserAgent"])
    #print(str2)
    s.send(str2.encode(encoding='utf_8', errors='strict'))
    
    msg2 = s.recv(m_Vars["bufLen"])
    print (msg2)    
    seq = seq + 1
    
    
    sessionId = decodeMsg(msg2)['Session']
    #print("sessionId" + sessionId)
    

    str3 = genmsg_PLAY(m_Vars["defaultTestUrl"] + "/",seq,m_Vars["defaultUserAgent"],sessionId)
    s.send(str3.encode(encoding='utf_8', errors='strict'))
    msg3 = s.recv(m_Vars["bufLen"])
    print (msg3)    
    seq = seq + 1
    
    print("start play .........")
    
    
    
    while True :
        
        msgRcv = s.recv(m_Vars["bufLen"])
        if None == len(msgRcv) : break
        #print (len(msgRcv))
        time.sleep(5)

    s.close()
    
class testThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("开始线程： "+self.name)
        start()
        print("结束线程： "+self.name)
 
total_num = input("input test num: ")
num =1 
while num <= int(total_num):
    thread = testThread(num,"testThreads_"+str(num))
    thread.start()
    time.sleep(0.5)
    num += 1
