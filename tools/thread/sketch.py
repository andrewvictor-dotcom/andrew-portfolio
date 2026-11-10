# pencil line drawing made from each real cover (same layout, so the scan can turn it into the real UI in place)
import sys,numpy as np
from PIL import Image,ImageFilter
def portrait(src,dst,crop=.8):
    # graphite-on-paper pencil portrait (dodge blend), same crop as the photo on the page
    im=Image.open(src).convert('L');W,H=im.size;tw=min(W,round(H*crop));th=round(tw/crop);im=im.crop(((W-tw)//2,(H-th)//2,(W-tw)//2+tw,(H-th)//2+th));im.thumbnail((900,1125))
    g=np.asarray(im,dtype=np.float32);bl=np.asarray(Image.fromarray((255-g).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)),dtype=np.float32)
    d=np.clip(g*255/np.maximum(1,255-bl),0,255);d=np.clip((d-30)/225,0,1)**1.6
    paper=np.array([239,235,227],dtype=np.float32);ink=np.array([46,44,42],dtype=np.float32)
    Image.fromarray((ink+(paper-ink)*d[...,None]).astype(np.uint8)).save(dst,'WEBP',quality=80,method=6)
def sketch(src,dst,maxw=1200,crop=None,blur=.7,thr=.16):
    im=Image.open(src).convert('RGBA')
    if crop:
        W,H=im.size;tw=min(W,round(H*crop));th=round(tw/crop);im=im.crop(((W-tw)//2,(H-th)//2,(W-tw)//2+tw,(H-th)//2+th))
    bg=Image.new('RGBA',im.size,(255,255,255,255));bg.alpha_composite(im);g=bg.convert('L')
    if g.width>maxw:g=g.resize((maxw,round(g.height*maxw/g.width)),Image.LANCZOS)
    a=np.asarray(g.filter(ImageFilter.GaussianBlur(blur)),dtype=np.float32)
    gx=np.zeros_like(a);gy=np.zeros_like(a)
    gx[:,1:-1]=a[:,2:]-a[:,:-2];gy[1:-1,:]=a[2:,:]-a[:-2,:]
    m=np.hypot(gx,gy);m=m/np.percentile(m,99.3);m=np.clip(m,0,1)
    m=np.where(m<thr,0,m);m=np.clip((m-thr)/.5,0,1)**.8
    al=(m*255).astype(np.uint8)
    out=Image.new('LA',g.size,(0,0));out.putalpha(Image.fromarray(al))
    out.convert('RGBA').save(dst,'WEBP',quality=82,method=6)
if sys.argv[1]=='--from':
    import re,json
    h=open(sys.argv[2]).read();st=json.loads(re.search(r'id="state">(.*?)</script>',h,re.S).group(1).replace('<\\/','</'))
    for p in st['projects']:
        c=p.get('cover') or ''
        if re.match(r'^media/[0-9a-f]+\.\w+$',c):d=re.sub(r'\.\w+$','_sk.webp',c);sketch(c,d);print(d)
    ph=st.get('profile',{}).get('photo') or ''
    if re.match(r'^media/[0-9a-f]+\.\w+$',ph):d=re.sub(r'\.\w+$','_sk.webp',ph);__import__('pencil').pencil(ph,d);print(d)
else:
    for s in sys.argv[1:]:
        d='sketch/'+s.split('/')[-1].split('.')[0]+'_sk.webp';sketch(s,d);print(d)
