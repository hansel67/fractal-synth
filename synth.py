import wave, struct
import math as m
import numpy as np
import os

def tri(x):
    return 0.5-abs(x-m.floor(x)-0.5)

def blanc(x,w,iter): #continuous if |w|<1 and CND if w>1/4
    retval = 0
    for i in range(1,iter):
        retval += tri(x*m.pow(2.0,i))*m.pow(w,i)
    return retval

def oss(x,a,b):
    return (m.sin(x*m.pi*2)+1)*abs(a-b)/2+min(a,b)

def wei(x,a,b,iter): #classically a=0.5 and b=2
    retval = 0
    for i in range(1,iter):
        retval += m.sin(2*m.pi*x*pow(b,i))*pow(a,i)
    return retval

def qm(x,iter): #minkowski's question mark function
    N = x
    D = 1
    retval = m.floor(x)
    ps_a = 0
    for i in range(1,iter):
        Dtemp = D
        D = N % D
        N = Dtemp
        if D != 0.0:
            ps_a += m.floor(N/D)
            if ps_a > 10000:
                break
            retval += 2*pow(-1,i+1)/pow(2,ps_a)
        else:
            break
    return retval

def digit(x,i,b):
    return m.floor(pow(b,-i)*x)-b*m.floor(pow(b,-1-i)*x)

def cant(x,iter):
    retval = 0
    d = 0
    for i in range(1,iter):
        d = digit(x,-i,3)
        if d != 0:
            retval += pow(2,-i)
        if d == 1:
            break
    return m.floor(x)+retval

def bump(x):
  p = 1
  y = x - m.floor(x)
  if y <= 0:
      retval = 0
  elif y >= 1:
      retval = 1
  else:
      z = m.exp(-m.pow(y,-p))
      retval = z/(z+m.exp(-m.pow(1-y,-p)))
  return m.floor(x)+retval

sampleRate = 44100.0 # hertz
duration = 10.0 # seconds
MIDDLEC = 261.625565
LFO_FREQ = 6.49 #hertz
filename = os.getcwd() + '/CUSTOM_WAVES/QM_TWOSIDED_WAVE'

numSamps = m.floor(sampleRate*duration)
freq = MIDDLEC

obj = wave.open(filename+'.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)

for i in range(1,numSamps):
    t = i/sampleRate
    p = i/numSamps
    if t - m.floor(t)<.00001:
        print(t)
    x = t*MIDDLEC
    value = qm(tri(x+0.25)*2,20)*2-1 
    data = struct.pack('<h',m.floor(value*32767))
    obj.writeframesraw(data)

obj.close()

os.system(filename + '.wav')
# if f(t) is a monotonic bijection [0,1]->[0,1]
# we extend to the line by f(x)=m.floor(x)+f(x-m.floor(x))
# we can make certain waves from such f. namely:
# wave1 = f(x)-x
# wave2 = f(tri(x+0.25)*2)*2-1
#
# if f(t) is more of an arc with f(0)=f(1)=0 and max f ~ 1
# this time we extend f to the line via simply f(x)=f(x-m.floor(x))
# we can make waves from such f via
# wave1 = f(2x)*sign(np.sin(m.pi*2*x))
