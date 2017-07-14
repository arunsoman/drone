import numpy as np
import time as tm

def createPID(Kp, Ki, Kd):
  startTime = int(round(tm.time.time() * 1000))
  err,prevErr =0
  errs= [0]
  def compute(currTime):
    return Kp*err + ki*sum( int(i) for i in errs) +  Kd*slope(currTime)
    
  def start(error):
    err = error
    startTime = int(round(time.time() * 1000))
    errs.append(error)
    return compute(startTime)
    
  def update(error):
    prevErr = err
    err = error
    return compute(int(round(time.time() * 1000)))
    
  return {'start': start, 'update': update}
  
def test():
  pid = createPID(1, -.08, -.23)
  print (pid.start(10))
  print(pid.update(5))
