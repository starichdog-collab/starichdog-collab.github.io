"""Build both 30-second clinic videos with local FFmpeg and original synthesized music.
Requires ffmpeg, numpy, and NotoSansCJKkr Regular/Bold. No external API or paid service.
Run: python marketing/build_video.py
"""
from pathlib import Path
import subprocess, tempfile, wave, math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
TMP=Path(tempfile.mkdtemp(prefix='clinic-video-'))
REG='/usr/local/share/fonts/noto-korean/NotoSansCJKkr-Regular.otf'
BOLD='/usr/local/share/fonts/noto-korean/NotoSansCJKkr-Bold.otf'
RATE=44100
DURATION=30

# An original, quiet instrumental cue synthesized from sine-wave notes.
# No samples, speech, or third-party recordings are used.
audio=np.zeros((RATE*DURATION,2),dtype=np.float64)
beat=30/32
chords=[[48,55,59,64],[45,52,55,60],[41,48,52,57],[43,50,57,62]]*2
for bar,notes in enumerate(chords):
 start=int(bar*4*beat*RATE);n=min(int(4.5*beat*RATE),len(audio)-start);t=np.arange(n)/RATE
 env=np.minimum(t/.8,1)*np.minimum((n/RATE-t)/1.2,1)
 for k,note in enumerate(notes):
  hz=440*2**((note-69)/12)
  tone=(np.sin(2*np.pi*hz*t)+.15*np.sin(4*np.pi*hz*t))*env*.026
  pan=.35+.1*k
  audio[start:start+n,0]+=tone*(1-pan);audio[start:start+n,1]+=tone*pan
melody=[72,76,79,76,69,72,76,74,69,72,77,76,71,74,79,74]
for i,note in enumerate(melody):
 start=int((i*2+.3)*beat*RATE);n=min(int(2.4*beat*RATE),len(audio)-start);t=np.arange(n)/RATE
 hz=440*2**((note-69)/12);env=(1-np.exp(-t*50))*np.exp(-t*2)
 tone=(np.sin(2*np.pi*hz*t)+.17*np.sin(4*np.pi*hz*t)+.04*np.sin(6*np.pi*hz*t))*env*.10
 audio[start:start+n,0]+=tone*.65;audio[start:start+n,1]+=tone*.55
fade=np.minimum(np.arange(len(audio))/RATE/1.0,1)*np.minimum((len(audio)-np.arange(len(audio)))/RATE/2,1)
audio*=fade[:,None]
audio=np.clip(audio,-1,1)
wav=TMP/'original-music.wav'
with wave.open(str(wav),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes((audio*32767).astype('<i2').tobytes())

def txt(text,size,x,y,color='white',bold=False,spacing=12):
 name=TMP/f'text-{len(list(TMP.glob("text-*")))}.txt';name.write_text(text)
 return f"drawtext=fontfile='{BOLD if bold else REG}':textfile='{name}':fontsize={size}:fontcolor={color}:x={x}:y={y}:line_spacing={spacing}"

photo_scenes=[
 ('dialysis-room.jpg','면목동에서 만나는\n신장질환·혈액투석 진료','면목연세석내과 인공신장실'),
 ('dialysis-center.jpg','인공신장실 5·6층\n외래 진료 2층','서울 중랑구 면목로 398 스마트빌딩'),
 ('dialysis-room.jpg','상봉동·망우동에서 방문 전\n위치와 일정을 확인하세요','병원은 중랑구 면목동에 있습니다.')
]

def run(args):
 subprocess.run(['ffmpeg','-v','error','-y','-threads','2']+args,check=True)

def build(vertical):
 W,H=(720,1280) if vertical else (1280,720)
 tag='vertical' if vertical else 'wide'
 clips=[]
 for scene in range(6):
  output=TMP/f'{tag}-{scene}.mp4';clips.append(output)
  filters=[];complex_filter=False
  if scene==0:
   image=ASSETS/('myeonmok-dialysis-poster.webp' if vertical else 'jungnang-dialysis-guide.webp')
   inputs=['-loop','1','-framerate','24','-i',str(image)]
   filters=[f'scale={W}:{H}:force_original_aspect_ratio=decrease',f'pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0xf5f5ef', 'setsar=1']
  elif scene in (1,2,3):
   image,title,subtitle=photo_scenes[scene-1]
   inputs=['-loop','1','-framerate','24','-i',str(ASSETS/image)]
   if vertical:
    complex_filter=True
    prefix=f'[0:v]scale=720:405:force_original_aspect_ratio=increase,crop=720:405,setsar=1[photo];color=c=0x173e45:s=720x1280:r=24:d=5[bg];[bg][photo]overlay=0:250'
    filters=[txt('면목연세석내과',38,50,105,bold=True),txt('MYEONMOK YONSEI SEOK',15,52,168,color='0xb6cbb8'),txt(title,40,50,740,bold=True,spacing=20),txt(subtitle,23,50,930,color='0xd5e1d1'),txt('사진 출처: 병원 공식 홈페이지',17,50,1170,color='0xb6cbb8')]
   else:
    filters=[f'scale={W}:{H}:force_original_aspect_ratio=increase',f'crop={W}:{H}', 'setsar=1','drawbox=x=0:y=430:w=iw:h=290:color=0x173e45@0.91:t=fill',txt('면목연세석내과',21,60,35,bold=True),txt(title,43,65,470,bold=True,spacing=15),txt(subtitle,24,65,610,color='0xd5e1d1'),txt('사진 출처: 병원 공식 홈페이지',16,65,685,color='0xb6cbb8')]
  elif scene==4:
   inputs=['-f','lavfi','-i',f'color=c=0x173e45:s={W}x{H}:r=24:d=5']
   if vertical:
    filters=[txt('면목연세석내과',26,50,90,color='0xb6cbb8'),txt('외래 진료 안내',48,50,240,bold=True),txt('평일     08:30 – 20:00\n토요일  08:30 – 16:00\n점심     13:00 – 14:00',32,50,420,spacing=40),txt('일요일·공휴일 휴진',32,50,720,color='0xdbe6cf'),txt('투석 일정·접수 마감은\n전화로 확인해 주세요.',26,50,940,color='0xb6cbb8',spacing=15)]
   else:
    filters=[txt('면목연세석내과',23,80,60,color='0xb6cbb8'),txt('외래 진료 안내',50,80,150,bold=True),txt('평일 08:30 – 20:00    토요일 08:30 – 16:00',35,80,290),txt('점심 13:00 – 14:00    일요일·공휴일 휴진',32,80,380,color='0xdbe6cf'),txt('투석 일정·접수 마감은 전화로 확인해 주세요.',25,80,560,color='0xb6cbb8')]
  else:
   inputs=['-f','lavfi','-i',f'color=c=0xf5f5ef:s={W}x{H}:r=24:d=5']
   if vertical:
    filters=[txt('중랑구 신장투석 안내',24,50,100,color='0x416f68'),txt('면목연세석내과',49,50,260,color='0x173e45',bold=True),txt('서울 중랑구 면목로 398\n스마트빌딩',32,50,430,color='0x416f68',spacing=20),txt('02-437-0808',61,50,650,color='0x173e45',bold=True),txt('공식 홈페이지에서\n자세히 확인하세요.',30,50,900,color='0x416f68',spacing=20),txt('진료 정보 확인 2026.10.27',18,50,1160,color='0x64746f')]
   else:
    filters=[txt('중랑구 신장투석 안내',23,80,65,color='0x416f68'),txt('면목연세석내과',58,80,165,color='0x173e45',bold=True),txt('서울 중랑구 면목로 398 스마트빌딩',33,80,295,color='0x416f68'),txt('02-437-0808',74,80,395,color='0x173e45',bold=True),txt('공식 홈페이지에서 자세히 확인하세요.',27,80,555,color='0x416f68'),txt('진료 정보 확인 2026.10.27',16,80,670,color='0x64746f')]
  filters+=['format=yuv420p','fade=t=in:st=0:d=0.2','fade=t=out:st=4.8:d=0.2']
  args=inputs
  if complex_filter:args+=['-filter_complex_threads','1','-filter_complex',prefix+','+','.join(filters)]
  else:args+=['-filter_threads','1','-vf',','.join(filters)]
  args+=['-t','5','-r','24','-an','-c:v','libx264','-preset','fast','-crf','26','-pix_fmt','yuv420p','-threads','2',str(output)]
  run(args)
  print(tag,'scene',scene+1,'done',flush=True)
 concat=TMP/f'{tag}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in clips))
 out=ASSETS/('myeonmok-yonsei-seok-dialysis-vertical.mp4' if vertical else 'myeonmok-yonsei-seok-dialysis-30s.mp4')
 run(['-f','concat','-safe','0','-i',str(concat),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','96k','-t','30','-movflags','+faststart','-metadata','title=면목연세석내과 신장투석 안내','-metadata','comment=Actual clinic photos; original locally synthesized music; no narration.',str(out)])
 print('FINISHED',out,out.stat().st_size,flush=True)

build(False)
build(True)
print('Temporary render files:',TMP)
