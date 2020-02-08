import time

remindTime=0
remindAt=["50", "MINUTES"]
if remindAt[1]=="AN" and remindAt[0]=="HALF" and remindAt[2]=="HOUR":
  remindTime=int(time.strftime("%H%M"))+30
elif remindAt[0]=="AN" and remindAt[1]=="HOUR":
  remindTime=int(time.strftime("%H%M"))+60
elif remindAt[1]=="MINUTES" or remindAt[1]=="MINUTE":
  remindTime=int(time.strftime("%H%M"))+int(remindAt[0])
elif remindAt[1]=="HOURS" or remindAt[1]=="HOUR":
  remindTime=int(time.strftime("%H%M"))+(int(remindAt[0])*100)

print int(time.strftime("%H%M"))
remindTime=str(remindTime)
print remindTime
if len(remindTime)==3:
  remindTime="0"+str(remindTime)
print remindTime
while int(str(remindTime)[2:])>=60:
  remindTime=int(remindTime)
  remindTime-=60
  remindTime+=100
  print remindTime
remindTime=str(remindTime)
if len(remindTime)==3:
  remindTime="0"+str(remindTime)
print remindTime
while int(str(remindTime)[0:2])>=24:
  remindTime-=2400
  print remindTime

print str(remindTime)
