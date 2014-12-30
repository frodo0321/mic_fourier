import audioop
import alsaaudio
import numpy as np
import scipy.signal
import time
import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import sys


mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
mic.setchannels(1)
mic.setrate(8000)
mic.setformat(alsaaudio.PCM_FORMAT_U8)
mic.setperiodsize(160)


fig = plt.figure()
#ax = plt.axes(xlim=(0, 4000), ylim=(0, 2000))
ax = plt.axes(xlim=(0, 1600), ylim=(0, 500))
line, = ax.plot([], [], lw=2)
wavque=deque()

def init():
    line.set_data([], [])
    return line,

def animate(i):
	dataarray=[]
	l, data = mic.read()
	print l
	if l==160 or l==80:
		for s in data:
			dataarray.append(ord(s))
		wavque.append(dataarray)	

		while(len(wavque)>10):
			wavque.popleft()
	
		prefft=[]
		for e in wavque:
			prefft.extend(e)

		fft = np.fft.rfft(prefft)
		line.set_data(xrange(0, len(np.real(fft))*5, 5), np.real(fft))
		#line.set_data(xrange(len(prefft)), prefft)
		time.sleep(.001)
	return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=1, interval=1, blit=True)
try:
	plt.show()
except AttributeError:
	pass
