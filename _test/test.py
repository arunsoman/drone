from drone import *

t = ThrustManager()
t.print_motors()
t._manual(10,20,30,15)
t.print_motors()