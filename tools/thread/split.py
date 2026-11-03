# move big embedded images/videos out of the page into separate files that load only when shown
import re,sys,base64,hashlib,os,json
src,out=sys.argv[1],sys.argv[2];h=open(src).read();os.makedirs('media',exist_ok=True)
ext={'image/webp':'webp','image/jpeg':'jpg','image/png':'png','video/mp4':'mp4'};files={};SIG=[];n0=len(h)
def rep(m):
    sig=h[max(0,m.start()-10):m.start()].endswith('data-src="')
    t,d=m.group(1),m.group(2)
    if len(d)<6000:return m.group(0)
    b=base64.b64decode(d);k=hashlib.sha1(b).hexdigest()[:12]+'.'+ext[t];p='media/'+k
    if p not in files:open(p,'wb').write(b);files[p]=os.path.abspath(p)
    if sig:SIG.append(p)
    return p
h=re.sub(r'data:(image/webp|image/jpeg|image/png|video/mp4);base64,([A-Za-z0-9+/=]+)',rep,h)
h=h.replace('</head>','<link rel="preload" as="image" href="'+SIG[0]+'"></head>',1) if SIG else h
i=h.find('<link rel="stylesheet" href="https://fonts.googleapis.com');e=h.find('>',i)
if i>-1:h=h[:i]+h[i:e].replace('rel="stylesheet"','rel="stylesheet" media="print" onload="this.media=\'all\'"')+h[e:]
open(out,'w').write(h);json.dump(files,open('media_map.json','w'))
print(round(n0/1e6,2),'MB ->',round(len(h)/1e6,2),'MB;',len(files),'files',round(sum(os.path.getsize(f) for f in files.values())/1e6,2),'MB')
