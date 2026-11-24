#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,requests,time,json,hashlib,re

ROOT=Path(__file__).resolve().parent
MEDIA=ROOT/'stock'; TMP=ROOT/'tmp_lote05'; DIST=ROOT/'dist_lote05'
for d in [MEDIA,TMP,DIST]:d.mkdir(parents=True,exist_ok=True)
W,H,FPS=720,1280,24
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
PALE=(250,247,239); PEACH=(237,189,143); DARK=(8,24,20)
REELS=[
 {
  "id": 1,
  "slug": "olhe-de-verdade",
  "music": 614,
  "scenes": [
   [
    8499352,
    4,
    "VOCÊ OLHOU DE VERDADE?",
    "NÃO É SÓ MAIS UM CÃO."
   ],
   [
    9421538,
    4,
    "EXISTE UMA VIDA ALI.",
    "E ELA MERECE CUIDADO."
   ],
   [
    7474315,
    4,
    "UM GESTO CONSCIENTE",
    "PODE FAZER DIFERENÇA."
   ],
   [
    9314168,
    4,
    "FAÇA PARTE DESSA CAUSA",
    "CONHEÇA NO LINK DA BIO."
   ]
  ],
  "caption": "Às vezes, o primeiro passo é enxergar. Não precisamos inventar histórias para lembrar que todo animal merece cuidado e respeito. Conheça o trabalho educativo do Pata por Perto no link da bio. Cenas ilustrativas do Pexels. #PataPorPerto #ProtecaoAnimal #CuidadoResponsavel"
 },
 {
  "id": 2,
  "slug": "cuidar-tambem-e-informar",
  "music": 601,
  "scenes": [
   [
    3863747,
    4,
    "UM CÃO DESAPARECEU?",
    "A PRESSA PODE CONFUNDIR."
   ],
   [
    18516731,
    4,
    "REGISTRE E CONFIRA.",
    "INFORMAÇÃO TEM VALOR."
   ],
   [
    16436884,
    4,
    "DIVULGUE COM CUIDADO.",
    "SEM INVENTAR HISTÓRIAS."
   ],
   [
    7474415,
    4,
    "APRENDA COMO AJUDAR.",
    "CONHEÇA NO LINK DA BIO."
   ]
  ],
  "caption": "Encontrou um animal que parece perdido? Observe com segurança, registre local e horário e tente identificar os responsáveis com cuidado. Evite conclusões precipitadas. Saiba mais sobre proteção animal responsável no Pata por Perto. Link na bio. Cenas ilustrativas do Pexels. #PataPorPerto #CaoPerdido #ProtecaoAnimal"
 },
 {
  "id": 3,
  "slug": "amor-e-atitude",
  "music": 682,
  "scenes": [
   [
    29337111,
    4.25,
    "ELES NÃO ESCOLHEM",
    "QUEM VAI CUIDAR."
   ],
   [
    6235744,
    4.25,
    "CUIDAR EXIGE TEMPO.",
    "E RESPONSABILIDADE."
   ],
   [
    7474285,
    4.25,
    "AMOR É ATITUDE.",
    "NÃO SÓ UMA PALAVRA."
   ],
   [
    13588269,
    4.25,
    "APOIE O PATA POR PERTO",
    "CONHEÇA NO LINK DA BIO."
   ]
  ],
  "caption": "O cuidado não acontece só no momento da emoção. Acontece na responsabilidade, no respeito e nas escolhas diárias. O Pata por Perto compartilha informações para incentivar atitudes conscientes. Conheça e apoie pelo link da bio. Cenas ilustrativas do Pexels. #PataPorPerto #AmorAosAnimais #GuardaResponsavel"
 },
 {
  "id": 4,
  "slug": "nao-passe-reto",
  "music": 587,
  "scenes": [
   [
    34337396,
    4,
    "PASSAR RETO É FÁCIL.",
    "ENXERGAR MUDA TUDO."
   ],
   [
    9421538,
    4,
    "VOCÊ NÃO PRECISA",
    "RESOLVER TUDO SOZINHO."
   ],
   [
    6235182,
    4,
    "PROCURE AJUDA CERTA.",
    "CUIDAR É TER CRITÉRIO."
   ],
   [
    7474315,
    4,
    "APOIE NOSSO TRABALHO",
    "CONHEÇA NO LINK DA BIO."
   ]
  ],
  "caption": "Você viu um animal em situação de risco? Antes de agir por impulso, avalie sua segurança e procure orientação especializada quando necessário. Informação também faz parte da proteção. Conheça o Pata por Perto pelo link da bio. Cenas ilustrativas do Pexels. #PataPorPerto #ProtecaoAnimal #Conscientizacao"
 },
 {
  "id": 5,
  "slug": "um-convite-a-empatia",
  "music": 614,
  "scenes": [
   [
    40964514,
    4.5,
    "NÃO É APENAS UM VÍDEO.",
    "É UM CONVITE À EMPATIA."
   ],
   [
    8056269,
    4.5,
    "APRENDA. COMPARTILHE.",
    "PROTEÇÃO É COLETIVA."
   ],
   [
    7469676,
    4.5,
    "MAIS INFORMAÇÃO.",
    "MAIS CUIDADO RESPONSÁVEL."
   ],
   [
    7474285,
    4.5,
    "CONHEÇA O PATA POR PERTO",
    "LINK NA BIO."
   ]
  ],
  "caption": "A proteção animal precisa de cuidado, informação e responsabilidade. Compartilhar boas orientações também é uma maneira de contribuir. Saiba mais sobre o projeto educativo Pata por Perto e como apoiá-lo pelo link da bio. Cenas ilustrativas do Pexels. #PataPorPerto #Empatia #ProtecaoAnimal"
 }
]
def run(cmd,quiet=True):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(' '.join(map(str,cmd[:10]))+' FAILED '+p.stderr[-2400:])
 return p.stdout
def download(url,dst):
 if dst.exists() and dst.stat().st_size>200000:return
 for attempt in range(3):
  try:
   with requests.get(url,stream=True,timeout=(15,95),headers={'User-Agent':'Mozilla/5.0'}) as r:
    r.raise_for_status()
    if not any(k in r.headers.get('Content-Type','') for k in ('video','audio','octet-stream')):raise RuntimeError('wrong content-type '+r.headers.get('Content-Type',''))
    with dst.with_suffix('.part').open('wb') as f:
     for chunk in r.iter_content(1024*512):
      if chunk:f.write(chunk)
   dst.with_suffix('.part').replace(dst)
   assert dst.stat().st_size>200000
   print('Downloaded:',dst.name,dst.stat().st_size,flush=True)
   return
  except Exception as e:
   print('Retry',dst.name,str(e)[:190],flush=True)
   if attempt==2:raise
   time.sleep(3*(attempt+1))
def ft(path,size):return ImageFont.truetype(path,size)
def wrap(draw,phrase,font,maxw):
 words=phrase.split();r=[];line=''
 for word in words:
  candidate=(line+' '+word).strip()
  if draw.textbbox((0,0),candidate,font=font)[2]<maxw or not line:line=candidate
  else:r.append(line);line=word
 if line:r.append(line)
 return r
def graphic(idx,title,subtitle,final):
 image=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(image)
 for y in range(0,330):
  a=int(165*(1-y/330)**1.6)
  d.line((0,y,W,y),fill=(*DARK,a))
 for y in range(320,H):
  a=min(232,int(232*((y-320)/(H-320))**1.14))
  d.line((0,y,W,y),fill=(*DARK,a))
 d.text((60,105),'PATA POR PERTO',font=ft(BOLD,27),fill=PALE)
 d.line((60,151,132,151),fill=PEACH,width=4)
 f=ft(BOLD if final else SERIF,44 if final else 51)
 head=wrap(d,title,f,600)
 y=717 if not final else 703
 for i,s in enumerate(head):
  d.text((60,y+i*72),s,font=f,fill=PALE,stroke_width=1,stroke_fill=(0,8,4))
 sep=y+len(head)*72+8
 d.line((61,sep,141,sep),fill=PEACH,width=4)
 f2=ft(BOLD,24)
 for i,s in enumerate(wrap(d,subtitle,f2,594)):
  d.text((61,sep+23+i*38),s,font=f2,fill=PEACH)
 if final:
  d.rounded_rectangle((60,1050,404,1113),radius=25,fill=(*PEACH,235))
  d.text((90,1067),'LINK NA BIO',font=ft(BOLD,24),fill=DARK)
 d.text((61,1195),'CUIDADO • EDUCAÇÃO • RESPONSABILIDADE',font=ft(BOLD,14),fill=PALE)
 return image
def scene(r,i,src,duration,title,sub):
 ov=TMP/f"overlay_{r['id']}_{i}.png";graphic(i,title,sub,i==3).save(ov)
 out=TMP/f"shot_{r['id']}_{i}.mp4"
 vf=f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},eq=saturation=0.92:contrast=1.04,format=yuv420p[v];[1:v]format=rgba,fade=t=in:st=0:d=0.38:alpha=1,fade=t=out:st={duration-0.35}:d=0.35:alpha=1[t];[v][t]overlay=0:0:shortest=1[vout]"
 run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-y','-ss','0.5','-t',duration,'-i',src,'-loop','1','-framerate',FPS,'-i',ov,'-filter_complex',vf,'-map','[vout]','-an','-c:v','libx264','-preset','veryfast','-crf','22','-r',FPS,'-pix_fmt','yuv420p',out])
 return out
def render(r):
 cuts=[]
 for i,(id,sec,title,subtitle) in enumerate(r['scenes']):
  cuts.append(scene(r,i,MEDIA/f'{id}.mp4',sec,title,subtitle))
 concat=TMP/f"concat_{r['id']}.txt"
 concat.write_text('\n'.join("file '"+str(p.resolve())+"'" for p in cuts)+'\n')
 joined=TMP/f"joined_{r['id']}.mp4"
 run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-y','-f','concat','-safe','0','-i',concat,'-c','copy',joined])
 duration=sum(float(row[1]) for row in r['scenes'])
 output=DIST/f"PATA-{r['id']:02d}-{r['slug']}.mp4"
 track=MEDIA/f"music-{r['music']}.mp3"
 run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-y','-i',joined,'-ss','12','-stream_loop','-1','-i',track,'-filter_complex',f'[1:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume=0.93,afade=t=in:st=0:d=0.55,afade=t=out:st={duration-1.2}:d=1.2[a]','-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-shortest','-movflags','+faststart',output])
 # derive cover from genuine film frame and graphic
 still=TMP/f"still_{r['id']}.png"
 run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-y','-ss','0.7','-i',MEDIA/f"{r['scenes'][0][0]}.mp4",'-vf',f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}','-frames:v','1',still])
 base=Image.open(still).convert('RGBA')
 base.alpha_composite(graphic(0,r['scenes'][0][2],r['scenes'][0][3],False))
 cover=DIST/f"PATA-{r['id']:02d}-CAPA.png";base.convert('RGB').save(cover,optimize=True)
 (DIST/f"PATA-{r['id']:02d}-LEGENDA.txt").write_text(r['caption'],encoding='utf-8')
 probe=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,codec_type,width,height','-show_entries','format=duration','-of','json',output]))
 ss=probe['streams'];v=[x for x in ss if x.get('codec_type')=='video'];a=[x for x in ss if x.get('codec_type')=='audio']
 assert len(v)==1 and len(a)==1 and a[0]['codec_name']=='aac' and v[0]['width']==W and v[0]['height']==H
 assert abs(float(probe['format']['duration'])-duration)<0.3
 levels=subprocess.run(['ffmpeg','-hide_banner','-i',str(output),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True).stderr
 m=re.search(r'mean_volume:\s*(-?\d+(?:\.\d+)?) dB',levels)
 assert m and float(m.group(1))>-38,(output,levels[-1500:])
 entry={'reel':r['id'],'file':output.name,'cover':cover.name,'seconds':float(probe['format']['duration']),'audio_db':float(m.group(1)),'audio_codec':'aac','dimensions':[W,H],'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'stocks':[x[0] for x in r['scenes']],'music':r['music']}
 print('REEL_FINISHED',json.dumps(entry,ensure_ascii=False),flush=True)
 return entry
def main():
 for vid in {s[0] for r in REELS for s in r['scenes']}:
  download(f'https://www.pexels.com/download/video/{vid}/',MEDIA/f'{vid}.mp4')
 for id in {r['music'] for r in REELS}:
  download(f'https://assets.mixkit.co/music/{id}/{id}.mp3',MEDIA/f'music-{id}.mp3')
 done=[render(r) for r in REELS]
 (DIST/'QA-REPORT.json').write_text(json.dumps(done,ensure_ascii=False,indent=2),encoding='utf-8')
 (DIST/'FONTES-LICENCA.txt').write_text('Cenas ilustrativas Pexels https://www.pexels.com/license/\nTrilhas Mixkit https://mixkit.co/license/#musicFree\nO projeto não declara ter resgatado os animais nas cenas.\n',encoding='utf-8')
 print('RENDER_ALL_DONE_LOTE05',len(done),flush=True)
if __name__=='__main__':main()
