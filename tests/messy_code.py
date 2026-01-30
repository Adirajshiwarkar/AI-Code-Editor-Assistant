def calc(a,b,c):
 x=a+b
 y=x*c
 return y

def print_all(l):
 for i in l:
  print(i)

import os
def get_files():
 return os.listdir('.')

class MyClass:
 def __init__(self, n):
  self.name = n
 def say_hi(self):
  print("hi "+self.name)
