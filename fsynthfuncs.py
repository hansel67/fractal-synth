import math as m
import numpy as np
import numpy.random as rnd
import cmath as cpx
import wave, struct

#here are some utility functions

def tri(x): #triangle wave with amplitude 1/4 centered at y=1/4 and tri(0)=0
    return 0.5-abs(x-m.floor(x)-0.5)

def digit(x,i,b): #the digit in the (b^i)s place of x
    return m.floor(pow(b,-i)*x)-b*m.floor(pow(b,-1-i)*x)

def oss(x,a,b): #osscilator
    return (m.sin(x*m.pi*2)+1)*abs(a-b)/2+min(a,b)

def cap(x,c): #constrain |x|<=c
    return max(-c,min(c,x))

# if f is monotonic, then we can make waves such as
# f_1sided(x) = f(x)-x
# f_2sided(x) = f(tri(x+0.25)*2)*2-1

def cantor(x,iter): #cantor f'n, monotonic
    retval = 0
    d = 0
    for i in range(1,iter):
        d = digit(x,-i,3)
        if d != 0:
            retval += pow(2,-i)
        if d == 1:
            break
    return m.floor(x)+retval

def minkowski(x,iter): #minkowski's ? f'n, monotonic
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

def bump(x): #non-analytic smooth bump f'n, monotonic
  p = 1
  y = x - m.floor(x)
  z = m.exp(-m.pow(y,-p))
  retval = z/(z+m.exp(-m.pow(1-y,-p)))
  return m.floor(x)+retval

#here are some non-monotonic fractals

def takagi(x,w,iter): #Takagi-Landsberbg f'n, continuous if |w|<1 and nowhere diff'ble if w>1/4
    retval = 0
    for i in range(1,iter):
        i
        retval += tri(x*m.pow(2.0,i))*m.pow(w,i)
    return retval

def weierstraussr(x,a,b,iter): #weierstrauss f'n, classically a=0.5 and b=2
    retval = 0
    for i in range(1,iter):
        retval += m.sin(2*m.pi*x*pow(b,i))*pow(a,i)
    return retval

def render(path,samples,sampleRate):
    obj = wave.open(path+'.wav','w')
    obj.setnchannels(1) # mono
    obj.setsampwidth(2)
    obj.setframerate(sampleRate)
    numSamps = len(samples)
    for i in range(1,numSamps):
        value = samples[i]
        data = struct.pack('<h',m.floor(value*32767))
        obj.writeframesraw(data)
        if i%100 == 0:
            print(str(m.floor(100*i/numSamps))+'% complete.',end='\r')
    obj.close()
