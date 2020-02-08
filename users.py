from grace import Messages
from routines import Routine
import time
import requests

class UserRegistry(Routine):

  def __init__(self, name, messenger):
    Routine.__init__(self, name, messenger)
    self.name=name
    self.m=messenger
    self.m.sendMessage("Grace", self.name, "addKeywords", ['CALL', 'ME'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['ACCOUNT', 'DETAILS'])
    self.m.sendMessage("Grace", self.name, "addKeywords", ['WHATS', 'MY', 'ACCOUNT'])
    
  def sql(self, sql):
    try:
      r=requests.get("http://localhost/grace/sql.php?auth=SECRET&sql="+sql).json() #CONFIGURE
      return r[0]
      
    except requests.exceptions.ConnectionError:
      print("Error connecting to Database")
    except IndexError:
      pass
  def getName(self, service, user):
    try:
      r=requests.get("http://localhost/grace/sql.php?auth=SECRET&sql=SELECT * FROM `people` WHERE `"+service+"`='"+user+"'").json() #CONFIGURE
      #print r
      if r[0]['title']!=None:
        return r[0]['title']
    except requests.exceptions.ConnectionError:
      print("Error connecting to Database")
    except IndexError:
      #TODO: Add a create account/login prompt here.
      pass
    return user
      
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
        if "ME" in messageArray and "CALL" in messageArray:
          if messageArray.index("ME")==messageArray.index("CALL")+1:
            nn=tmessageArray[messageArray.index("CALL")+2:]
            first=True
            newname=""
            for x in nn:
              if first==False:
                newname+=" "
              newname+=x
              first=False
            service=m['message']['service']
            user=m['message']['user']
            self.m.sendMessage(m['from'], self.name, "MESSAGE", {"to":m['message']['user'], "message":"Ok, from now on I'll call you "+newname+"."})
            self.sql("UPDATE `people` SET `title`='"+newname+"' WHERE `"+service+"`='"+user+"'")
        if ("ACCOUNT" in messageArray and "DETAILS" in messageArray) or ("WHATS" in messageArray and "MY" in messageArray and "ACCOUNT" in messageArray):
          if not (messageArray.index("ACCOUNT")==messageArray.index("DETAILS")-1):
            continue
          elif not (messageArray.index("WHATS")==messageArray.index("MY")-1 and messageArray.index("MY")==messageArray.index("ACCOUNT")-1):
            continue
          details=self.sql("SELECT * FROM `people` WHERE `"+message['service']+"`='"+message['user']+"'")
          self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':str(details)})
  def actions(self):
    pass
            

if __name__=="__main__":
  print('''Launch Code:
  ur=UserRegistry("UserRegistry",mes)
  ur.start()
  
  Handles account management''')
