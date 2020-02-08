import os

print("\nConfigure not complete! Only configures the #! on launch.py\n")

with open('launch.py', 'r') as f:
  lines=f.read().splitlines()

o=""
while not (o=="1" or o=="2"):
  print("Select an operating system.")
  print("1. Linux")
  print("2. Windows")
  o=input(">")
if o=="1":
  lines[0]='#!/usr/bin/env python3'
else:
  conf=False
  while not conf:
    path=input("Enter the path to python 3: ")
    path=path.replace('"', '')
    if path[-11:]=='\\python.exe':
      path=path.replace('\\python.exe', '')
    if not path[-1]=='\\':
      path+="\\"
    if not os.path.isfile(path+'python.exe'):
      print("Python 3 not detected")
      continue
    else:
      conf=True
      lines[0]='#!"'+path+'python.exe"'

os.mkdir('build')
os.chdir('build')  
with open('launch.py', 'w') as f:
  f.write('\n'.join(lines))