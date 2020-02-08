from routines import Routine
import time

class Routine(Routine):

  def __init__(self, name, messenger):
    Routine.__init__(self, name, messenger)
    self.name=name
    self.m=messenger
    self.m.sendMessage("Grace", self.name, "addKeywords", ['REMIND', 'ME', 'TO', 'IN'])
      
  def superListener(self, mes):
    for m in mes:
      if m['subject']=='MESSAGE':
        message=m['message']['message']
        messageArray=message.replace(".","")
        messageArray=messageArray.replace(",","")
        messageArray=messageArray.replace("!","")
        messageArray=messageArray.replace(";","")
        messageArray=messageArray.replace(":","")
        messageArray=messageArray.upper()
        messageArray=messageArray.split(" ")
        tmessageArray=message.replace(".","")
        tmessageArray=tmessageArray.replace(",","")
        tmessageArray=tmessageArray.replace("!","")
        tmessageArray=tmessageArray.replace(";","")
        tmessageArray=tmessageArray.replace(":","")
        tmessageArray=tmessageArray.split(" ")
      
  def actions(self):
    pass
