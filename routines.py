import threading
import time
import traceback

class Routine(threading.Thread):

  def __init__(self, name, messenger):
    threading.Thread.__init__(self)
    self.name=name
    self.m=messenger
    self.running=True
    self.m.registerListener(name)
    
  def Listener(self):
    mes=self.m.readMessages(self.name)
    for m in mes:
      if m['subject']=="STOP":
        self.running=False
    try:
      self.superListener(mes)
    except:
      print("Error in Thread: "+self.name+" superListener: "+str(mes))
      traceback.print_exc()
    #print self.name+"'s Listener"
    if self.running:
      threading.Timer(1, self.Listener).start()
      
  def superListener(self, m):
    pass
      
  def run(self):
    self.Listener()
    while self.running:
      time.sleep(1)
      #print self.name+"'s Action"
      try:
        self.actions()
      except:
        print("Error in Thread: "+self.name+" Actions.")
        traceback.print_exc()
      
  def actions(self):
    pass
