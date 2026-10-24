"""120 BPM, 10 bars, 20 seconds. Deterministic stereo score + UI effects."""
from pathlib import Path
import wave
import numpy as np
SR=48000; DURATION=20; BEAT=60/120
mix=np.zeros((int(SR*DURATION),2),np.float64)
rng=np.random.default_rng(3107)
def put(start,sound,gain=1,pan=0):
    offset=round(start*SR); length=min(len(sound),len(mix)-offset)
    if offset<0 or length<=0:return
    angle=(pan+1)*np.pi/4
    mix[offset:offset+length,0]+=sound[:length]*gain*np.cos(angle)
    mix[offset:offset+length,1]+=sound[:length]*gain*np.sin(angle)
def tone(freq,duration,decay=3):
    t=np.arange(round(SR*duration))/SR
    return (np.sin(2*np.pi*freq*t+.45*np.sin(2*np.pi*freq*2*t)*np.exp(-t*6))+.15*np.sin(2*np.pi*freq*3*t))*np.minimum(t*120,1)*np.exp(-decay*t)
def kick():
    t=np.arange(round(SR*.34))/SR
    return np.sin(2*np.pi*(45*t+2.3*(1-np.exp(-t*34))))*np.exp(-t*16)
D=[293.66,369.99,440,554.37]; B=[246.94,293.66,369.99,440]; G=[196,246.94,293.66,369.99]; A=[220,277.18,329.63,493.88]
chords=[D,B,G,A,D,B,G,A,A,D]
for bar,chord in enumerate(chords):
    start=bar*4*BEAT
    for i,f in enumerate(chord):put(start,tone(f,2.5,.95),.042,(i-1.5)/2)
    for beat in range(4):
        j=bar*4+beat; st=j*BEAT
        if j>36:continue
        energy=1 if bar in [2,3,5,6] else .8
        put(st,kick(),(.36 if beat%2==0 else .13)*energy)
        put(st,tone(chord[0]/2,.6,5),.17*energy)
        put(st,tone(chord[(beat+bar)%4]*2,.8,6),.09*energy,(-1)**j*.55)
        if j<36:
            t=np.arange(round(SR*.09))/SR;noise=rng.normal(0,1,len(t));hp=noise-np.convolve(noise,np.ones(7)/7,'same')
            put(st+BEAT/2,hp*np.exp(-t*100),.032,(-1)**j*.7)
            if beat%2:
                t=np.arange(round(SR*.16))/SR;noise=rng.normal(0,1,len(t))
                put(st,noise*np.exp(-t*38),.042)
for j in [0,4,10,16,22,28,34,36]:
    st=j*BEAT;t=np.arange(round(SR*.25))/SR
    noise=rng.normal(0,1,len(t));soft=np.convolve(noise,np.ones(38)/38,'same')
    put(max(0,st-.12),soft*np.sin(np.pi*t/.25)**2,.19,-.2)
    put(st,tone(880 if j!=36 else 1320,.5,8),.06,.3)
for st in [3,3.7,5.45,6.65,8.33,8.51,8.69,8.87,9.05,9.23,9.55,12.5,14.25,14.72,15.25]:
    put(st,tone(1760,.14,30),.035,.25)
# The final tonic lands at beat 36; later beats leave room for its release.
fade=np.minimum(1,np.maximum(0,(DURATION-np.arange(len(mix))/SR)/.7))
mix*=fade[:,None];mix=np.tanh(mix*1.5)
mix*=.88/max(.88,np.max(np.abs(mix)))
path=Path(__file__).parent/'assets/sound.wav'
with wave.open(str(path),'wb') as out:
    out.setnchannels(2);out.setsampwidth(2);out.setframerate(SR)
    out.writeframes((mix*32767).astype('<i2').tobytes())
print(f'{DURATION}s / 120 BPM / first beat 0.000s / peak {np.max(np.abs(mix)):.4f}')
