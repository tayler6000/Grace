import threading
import os
import time
import socket
import requests

from routines import Routine

class Grace(threading.Thread):
  
  def __init__(self, messenger, UserRegistry):
    threading.Thread.__init__(self)
    self.m=messenger
    self.ur=UserRegistry
    self.name="Grace"
    self.running=True
    self.m.registerListener(self.name)
    self.keywords=[]
    
  def Listener(self):
    #print "Grace's Listener"
    mes=self.m.readMessages(self.name)
    for m in mes:
      if m['subject']=="STOP":
        self.running=False
      elif m['subject']=="addKeywords":
        self.keywords.append({'service':m['from'], 'keywords':m['message']})
        print("Added Keywords: "+str(m['message'])+" to service: "+str(m['from']))
      elif m['subject']=="MESSAGE":
        message=m['message']['message']
        user=m['message']['user']
        messageArray=message.replace("."," ")
        messageArray=messageArray.replace(","," ")
        messageArray=messageArray.replace("!"," ")
        messageArray=messageArray.replace(";"," ")
        messageArray=messageArray.replace(":"," ")
        messageArray=messageArray.replace("?"," ")
        messageArray=messageArray.upper()
        messageArray=messageArray.split(" ")
        if "PING" in messageArray:
          self.m.sendMessage(m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"Pong."})
        elif "SHUTDOWN" in messageArray:
          self.m.sendMessage(m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"Shutting down."})
          self.m.sendMessage("ALL", "Grace", "STOP", "BY ORDER OF THE JARL, STOP RIGHT THERE!")
        elif ("THANK" in messageArray and "YOU" in messageArray) or "THANKS" in messageArray:
          if "GRACE" in messageArray:
            self.m.sendMessage(m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"You're welcome, "+self.ur.getName(m['message']['service'],m['message']['user'])+"."})
          else:
            self.m.sendMessage(m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"You're welcome."})
        
        else:
          found=False
          routines=[]
          for s in self.keywords:
            words=len(s['keywords'])
            count=0
            for w in s['keywords']:
              if w in messageArray:
                count+=1
            if count>=words:
              found=True
              if s['service'] not in routines:
                routines.append(s['service'])
          if found==False:
            self.m.sendMessage(m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"Hello,  I'm Grace.  I am now a rule based A.I. as opposed to the chat bot I once was.  I can only execute commands."})
          for r in routines:
            self.m.sendMessage(r, m['from'], "MESSAGE", m['message'])
      
      elif m['subject']=="COMMAND":
        message=m['message']['message']
        user=m['message']['user']
        messageArray=message.replace(".","")
        messageArray=messageArray.replace(",","")
        messageArray=messageArray.replace("!","")
        messageArray=messageArray.replace(";","")
        messageArray=messageArray.replace(":","")
        messageArray=messageArray.upper()
        messageArray=messageArray.split(" ")
        if "SHUTDOWN" in messageArray:
          self.m.sendMessage(m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"Shutting down."})
          self.m.sendMessage("ALL", "Grace", "STOP", "BY ORDER OF THE JARL, STOP RIGHT THERE!")
        elif "PING" in messageArray:
          self.m.sendMessage( m['from'], "Grace", "MESSAGE", {'to':m['message']['user'], 'message':"Pong."})
    if self.running:
      threading.Timer(1, self.Listener).start()
  
  def run(self):
    threading.Timer(1, self.Listener).start()
    
    
    
class Messages(threading.Thread):
  
  def __init__(self):
    threading.Thread.__init__(self)
    self.messages=[]
    self.name="Messenger"
    self.names=[]
    self.running=True
    self.registerListener("Messenger")
    
  def sendMessage(self, to, f, subject, message):
    self.messages.append({'to':to,'from':f,'subject':subject,'message':message})
    
  def Listener(self):
      mes=self.readMessages(self.name)
      for m in mes:
        if m['subject']=="STOP":
          self.running=False
      if self.running:
        threading.Timer(1, self.Listener).start()
    
  def registerListener(self,name):
    self.names.append(name)
    
  def readMessages(self, recepient):
    m=[]
    for message in self.messages:
      if message['to']==recepient:
        m.append(message)
    for message in m:
      self.messages.remove(message)
    return m
    
  def run(self):
    print("Messaging Service Starting")
    threading.Timer(1, self.Listener).start()
    while self.running:
      time.sleep(1)
      #print(self.messages)
      m=self.readMessages("ALL")
      for mes in m:
        for name in self.names:
          self.sendMessage(name, mes['from'], mes['subject'], mes['message'])
          
    print("Messaging Service Stopped")
    
    


    
    
    
class TestRoutine(Routine):
  def __init__(self,name,messenger):
    Routine.__init__(self, name, messenger)
    self.name=name
    self.messenger=messenger
    
  def superListener(self,mes):
    for m in mes:
      pass
    print("Listened")
    
  def actions(self):
    print("Testing Routine")



class Switchboard(Routine):

  def __init__(self,messenger):
    name="SWITCHBOARD"
    Routine.__init__(self,name,messenger)
    self.name=name
    self.messenger=messenger
    self.switchboard={'kik':{}, 'email':{}}

  def registerRedirect(self, username, service, destination):
    self.switchboard[service][username]=destination
    print("Added Redirect of "+username+" from "+service+" to "+destination)

  def deleteRedirect(self, username, service, destination):
    self.removeRedirect(username, service, destination)
    
  def removeRedirect(self, username, service, destination):
    if self.switchboard[service][username]==destination:
      del self.switchboard[service][username]
      print("Removed Redirect of "+username+" from "+service+" to "+destination)
      
  def superListener(self,mes):
    for m in mes:
      if m['subject']=="REDIRECT":
        service=m['message']['service']
        f=m['message']['user']
        if service in self.switchboard:
          if f in self.switchboard[service]:
            self.messenger.sendMessage(self.switchboard[service][f], m['from'], 'MESSAGE', m['message'])
            self.messenger.sendMessage("Grace", m['from'], 'COMMAND', m['message'])
          else:
            self.messenger.sendMessage("Grace", m['from'], 'MESSAGE', m['message'])
        else:
          self.messenger.sendMessage("Grace", m['from'], 'MESSAGE', m['message'])  
      elif m['subject']=="registerRedirect":
        self.registerRedirect(m['message']['username'], m['message']['service'], m['message']['destination'])
      elif m['subject']=="removeRedirect" or m['subject']=="deleteRedirect":
        self.deleteRedirect(m['message']['username'], m['message']['service'], m['message']['destination'])
      
  def actions(self):
    pass
    


class KikListener(Routine):
  
  def __init__(self,messenger):
    Routine.__init__(self,"KikListener", messenger)
    self.name="KikListener"
    self.messenger=messenger
    self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.s.bind(("192.168.0.105", 46623)) #CONFIGURE
    except socket.error:
      print("Error Binding, stopping.")
      self.messenger.sendMessage("ALL", "KikListener", "STOP", "STOP")
      self.running=False
    self.s.listen(5)
    self.s.settimeout(10)
    self.key="YOURKEY" #CONFIGURE
    if self.running==True:
      self.m.sendMessage("KikListener", "Grace", "MESSAGE", {'to':"YOU", 'message':"Grace Started."}) #CONFIGURE
    
  def send(self,conn,string):
    length=len(string)
    #print "Length: "+str(length)
    conn.send(str(length))
    #print "Sent length"
    conn.recv(20)
    conn.send(string)
    #print "Sent String"

  def recv(self,conn):
    length=conn.recv(1024)
    conn.send("OK")
    m=conn.recv(int(length))
    return m
  
  
  def superListener(self, mes):
    for m in mes:
      if m['subject']=="STOP":
        self.running=False
        self.m.sendMessage("KikListener", "Grace", "MESSAGE", {'to':"YOU", 'message':"Grace Shutting Down. "}) #CONFIGURE
        self.s.shutdown(2)
        self.s.close()
      elif m['subject']=="MESSAGE":
        print(self.name+": Sending Message through Kikout from "+m['from'])
        r=requests.post("http://gracebot6000.herokuapp.com/kikout", {m['message']['to']:m['message']['message']}) #CONFIGURE
        #print r.status_code
  
  def actions(self):
    try:
      state=0
      c, addr=self.s.accept()
      state=1
      print(self.name+": Accepted connection from "+str(addr))
      key=self.recv(c)
      #print "Received Key"
      self.send(c, "OK")
      user=self.recv(c)
      self.send(c, "OK")
      mes=self.recv(c)
      print("Got message: "+str(mes))
      self.messenger.sendMessage("SWITCHBOARD", "KikListener", "REDIRECT", {'service': 'kik', 'user':user, 'message':mes})
    except socket.timeout:
      if state==1:
        print("Timeout")
    except:
      self.messenger.sendMessage("ALL", "KikListener", "STOP", "STOP") 

if __name__=="__main__":
  print("Run launch.py")
                        
