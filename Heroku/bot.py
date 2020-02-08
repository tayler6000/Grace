#!/usr/bin/env python3

from flask import Flask, request, Response
import os

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage, SuggestedResponseKeyboard, TextResponse

apikey=os.environ.get('API')
apikey="KIK-KEY" #CONFIGURE
ainame=os.environ.get('AINAME')
ainame="KIK-BOT-NAME" #CONFIGURE
app = Flask(__name__)
kik = KikApi(ainame, apikey)
kik.set_configuration(Configuration(webhook='https://YOURAPP.herokuapp.com/')) #CONFIGURE

import socket

import time
from ast import literal_eval
import sys
from random import randint
import logging
import threading
import urllib.parse

db="YOURGRACE.com" #CONFIGURE
port=46623 #CONFIGURE
key=os.environ.get('GKEY') #This is your key in grace.py on line 219

def send(conn,string):
  string=string.encode('utf8')
  length=len(string)
  #print("Length: "+str(length))
  conn.send(str(length).encode('utf8'))
  #print("Sent length")
  conn.recv(20)
  #print(string)
  conn.send(string)
  #print("Sent String")

def recv(conn):
  length=conn.recv(1024)
  conn.send("OK".encode('utf8'))
  m=str(conn.recv(int(length)), 'utf8')
  return m

#main

@app.route('/', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        print("Not Kik: "+str(request.get_data()))
        return Response(status=403)
    print("Kik: "+str(request.get_data()))
    messages = messages_from_json(request.json['messages'])
    print(messages)
    for message in messages:
        if isinstance(message, TextMessage):
          try:
            print("Trying to connect")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket Made")
            s.connect((db, port))
            print("Connected")
            time.sleep(1)
            print("Sending Key")
            send(s,key)
            data = recv(s)
            print("Received Response")
            if data=="OK":
              print("Sending User")
              send(s,message.from_user)
              data = recv(s)
              if data=="OK":
                print("Sending Message")
                send(s,message.body)
              else:
                sendMessage(message,data)
            else:
              sendMessage(message,"Invalid Key Error")
            s.close()
          
          except socket.error:
            print("Connection Failed")
          except:
            print(sys.exc_info()[0].__doc__)
            print(sys.exc_info()[1])
          finally:
            try:
              s.close()
              print("ERROR")
            except:
              pass

    return Response(status=200)

@app.route('/test', methods=['POST'])
def outin():
  return Response(status=200)

@app.route('/kikout',methods=['POST'])
def kikout():
  data=str(request.get_data(), 'utf8')
  data=data.split("=")
  data[1]=urllib.parse.unquote(data[1].replace('+',' '))
  kik.send_messages([TextMessage(to=data[0], body=data[1])])
  return Response(status=200)
def sendMessage(message, response):
  print("Response: "+response)
  kik.send_messages([TextMessage(to=message.from_user, chat_id=message.chat_id, body=response)])

if __name__ == "__main__":
  app.run(port=8080, debug=True)
    
    
