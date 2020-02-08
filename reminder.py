from routines import Routine
import time

class Reminder(Routine):

  def __init__(self, name, messenger):
    Routine.__init__(self, name, messenger)
    self.name=name
    self.m=messenger
    self.reminders=[]
    self.stages={}
    self.m.sendMessage("Grace", self.name, "addKeywords", ['REMIND', 'ME', 'TO', 'IN'])
    #Reminder: {'time':2200, 'user':'tayler6000', 'service':'kik', 'reminder': 'Reminder'}
      
  def superListener(self, mes):
    for m in mes:
      if m['subject']=="addReminder":
        if m['message']['user'] in self.stages:
          pass
        else:
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
          try:
            toIndex=messageArray.index("TO")
            inIndex=messageArray.index("IN")
          except ValueError:
            self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':"I'm sorry, I'm not sure what you're asking."})
            break
          if inIndex<toIndex:
            reminder=tmessageArray[toIndex+1:]
          elif inIndex>toIndex:
            reminder=tmessageArray[toIndex+1:inIndex]
          else:
            reminder=['Reminder']
          r=""
          for word in reminder:
            if r=="":
              r+=word
            else:
              r+=" "+word
          lengthError=False
          remindTime=0
          remindAt=messageArray[inIndex+1:inIndex+4]
          if remindAt[1]=="A" and remindAt[0]=="HALF" and remindAt[2]=="HOUR":
            remindTime=int(remindTime)+30*60
          elif remindAt[0]=="AN" and remindAt[1]=="HOUR":
            remindTime=remindTime+60*60
          elif remindAt[0]=="A" and remindAt[1]=="MINUTE":
            remindTime=remindTime+1*60
          elif remindAt[1]=="MINUTES" or remindAt[1]=="MINUTE":
            remindTime=remindTime+int(remindAt[0])*60
          elif remindAt[1]=="HOURS" or remindAt[1]=="HOUR":
            remindTime=remindTime+(int(remindAt[0])*60*60)
          
          
          remindTime=remindTime+time.time()
          
          if remindTime!=0 and lengthError==False:
            self.m.sendMessage("SWITCHBOARD", self.name, "registerRedirect", {'username':m['message']['user'], 'service':m['message']['service'], 'destination':self.name})
            self.stages[m['message']['user']]={}
            self.stages[m['message']['user']]['stage']=1
            self.stages[m['message']['user']]['remind']=r
            self.stages[m['message']['user']]['time']=remindTime
            self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':"Just to confirm, you'd like me to remind you '"+r+"' at "+time.strftime("%H:%M on %A", time.localtime(remindTime))+"?"})
          elif lengthError==True:
            self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':"I'm sorry, but I can't remind you about things in more than 47 hours."})
      elif m['subject']=="MESSAGE":
        message=m['message']['message']
        messageArray=message.replace(".","")
        messageArray=messageArray.replace(",","")
        messageArray=messageArray.replace("!","")
        messageArray=messageArray.replace(";","")
        messageArray=messageArray.replace(":","")
        messageArray=messageArray.upper()
        messageArray=messageArray.split(" ")
        if m['message']['user'] in self.stages:
          if self.stages[m['message']['user']]['stage']==1:
            if "YES" in messageArray or "CORRECT" in messageArray or "YEAH" in messageArray or "YUP" in messageArray:
              self.m.sendMessage("SWITCHBOARD", self.name, "removeRedirect", {'username':m['message']['user'], 'service':m['message']['service'], 'destination':self.name})
              r=self.stages[m['message']['user']]['remind']
              remindTime=self.stages[m['message']['user']]['time']
              del self.stages[m['message']['user']]
              self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':"Okay, I'll remind you to '"+r+"' at "+time.strftime("%H:%M on %A", time.localtime(remindTime))+"."})
              self.addReminder(remindTime, m['message']['user'], m['message']['service'], r)
            else:
              self.m.sendMessage("SWITCHBOARD", self.name, "removeRedirect", {'username':m['message']['user'], 'service':m['message']['service'], 'destination':self.name})
              self.m.sendMessage(m['from'], self.name, "MESSAGE", {'to':m['message']['user'], 'message':"Cancelling reminder."}) 
              del self.stages[m['message']['user']]
        elif "REMIND" in messageArray and "ME" in messageArray:
          remind=messageArray.index("REMIND")
          me=messageArray.index("ME")
          if me==remind+1:
            self.m.sendMessage("Reminders", m['from'], "addReminder", m['message'])
 
  def addReminder(self, time, user, service, reminder):
    self.reminders.append({'time':time, 'user':user, 'service':service, 'reminder':reminder})
  
  def actions(self):
    #print "Reminders: "+str(self.reminders)
    for r in self.reminders:
      t=time.time()
      if t>=int(r['time']):
        if r['service']=='kik':
          self.m.sendMessage("KikListener", self.name, 'MESSAGE', {'to':r['user'], 'message':"Reminder: '"+r['reminder']+"'"})
          self.reminders.remove(r)
    time.sleep(10)
            
            