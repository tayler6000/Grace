#!/usr/bin/env python
from grace import *
from routines import Routine
from reminder import Reminder
from users import UserRegistry
from pleasantries import Pleasantries

print("Grace 3.0 Starting...")

if __name__=="__main__":
  mes=Messages()
  mes.start()
  ur=UserRegistry("UserRegistry",mes)
  ur.start()
  g=Grace(mes, ur)
  g.start()
  switch=Switchboard(mes)
  switch.start()
  kik=KikListener(mes)
  kik.start()
  remind=Reminder("Reminders", mes)
  remind.start()
  ples=Pleasantries("Pleasantries", mes, ur)
  ples.start()
  print("Grace 3.0 Started")
  mes.join()
  ur.join()
  g.join()
  switch.join()
  kik.join()
  remind.join()
  ples.join()
  print("Grace 3.0 Stopped")
            
