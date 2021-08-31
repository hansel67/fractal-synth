import fsynthfuncs as f
import math as m
import numpy as np
import os
import matplotlib.pyplot as plt

MIDDLEC = 261.625565

sampleRate = 44100.0 # hertz
duration = 5.0 # seconds
freq = MIDDLEC

filename = 'BLANCMANGE_WAVE' #enter filename here
numSamps = m.floor(sampleRate*duration)
direc = os.getcwd()+'\\CUSTOM_WAVES\\'
samples = np.ndarray(numSamps)

print('Writing sound for ' + filename+'.',end='\n')

for i in range(1,numSamps):
    t = i/sampleRate
    p = i/numSamps
    x = t*freq
    samples[i] = f.takagi(x,0.5,30) #enter function here
    if i%1000 == 0:
        print(str(m.floor(p*100))+'% complete.',end='\r')

f.render(direc + filename,samples,sampleRate)
os.system(direc + filename + '.wav')
plt.plot(samples[1:m.floor(sampleRate/freq)])
plt.show()
