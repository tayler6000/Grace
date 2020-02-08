from routines import Routine
import time

class Pleasantries(Routine):

  def __init__(self, name, messenger, ur):
    Routine.__init__(self, name, messenger)
    self.name=name
    self.m=messenger
    self.ur=ur
    self.m.sendMessage("Grace", self.name, "addKeywords", ['HOW', 'ARE', 'YOU'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['HELLO'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['HI'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['HEY'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['YO'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['HIYA'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['GREETINGS'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['BYE'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['GOODBYE'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['FAREWELL'])
    
    
  def superListener(self, mes):
    for m in mes:
      if m['subject']=='MESSAGE':
        message=m['message']['message']
        messageArray=message.replace(".","")
        messageArray=messageArray.replace(",","")
        messageArray=messageArray.replace("!","")
        messageArray=messageArray.replace(";","")
        messageArray=messageArray.replace(":","")
        messageArray=messageArray.replace("?","")
        messageArray=messageArray.upper()
        messageArray=messageArray.split(" ")
        tmessageArray=message.replace(".","")
        tmessageArray=tmessageArray.replace(",","")
        tmessageArray=tmessageArray.replace("!","")
        tmessageArray=tmessageArray.replace(";","")
        tmessageArray=tmessageArray.replace(":","")
        tmessageArray=tmessageArray.replace("?","")
        tmessageArray=tmessageArray.split(" ")
        if 'HELLO' in messageArray or 'HI' in messageArray or 'HEY' in messageArray or 'YO' in messageArray or 'HIYA' in messageArray or 'GREETINGS' in messageArray:
          if 'GRACE' in messageArray:
            mes="Hello "+self.ur.getName(m['message']['service'], m['message']['user'])+"."
          else:
            mes="Hello."
          self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':mes})
        if "HOW" in messageArray and "ARE" in messageArray and "YOU" in messageArray:
          if messageArray.index("ARE")==messageArray.index("HOW")+1 and messageArray.index("YOU")==messageArray.index("HOW")+2:
            self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':"I'm good."})
        if 'BYE' in messageArray or 'GOODBYE' in messageArray or 'FAREWELL' in messageArray:
          if 'GRACE' in messageArray:
            mes="Goodbye "+self.ur.getName(m['message']['service'], m['message']['user'])+"."
          else:
            mes="Goodbye."
          self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':mes})
        
      
  def actions(self):
    pass
