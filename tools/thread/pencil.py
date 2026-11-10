# hand-drawn pencil portrait: XDoG contour lines + cross-hatching for the darks + paper grain
import sys,numpy as np
from PIL import Image,ImageFilter
def blur(a,s):return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(s)),dtype=np.float32)/255
def pencil(src,dst,crop=.8,W0=900):
    rgbim=Image.open(src).convert('RGB');W,H=rgbim.size;tw=min(W,round(H*crop));th=round(tw/crop);rgbim=rgbim.crop(((W-tw)//2,(H-th)//2,(W-tw)//2+tw,(H-th)//2+th)).resize((W0,round(W0/crop)),Image.LANCZOS)
    c=np.asarray(rgbim,dtype=np.float32)/255;im=rgbim.convert('L');g=np.asarray(im,dtype=np.float32)/255
    lum=g;person=((lum<.2)|((c[...,0]>c[...,1]*1.04)&(lum<.92))).astype(np.float32)  # dark suit/hair or skin tones; the garden is green
    person=np.clip((blur(person,5)-.45)/.2,0,1);person=np.clip((blur(person,3)-.3)/.4,0,1)
    # keep only the figure in the middle (drop dark leaves at the edges)
    hh,ww=person.shape;Y,X=np.mgrid[0:hh,0:ww].astype(np.float32);ell=np.clip(1.25-np.abs(X/ww-.5)/.34-np.clip(.18-Y/hh,0,1)*2,0,1);person*=ell
    g=np.clip((g-np.percentile(g,2))/(np.percentile(g,98)-np.percentile(g,2)),0,1)
    # contour lines (XDoG)
    g1=blur(g,1.1);g2=blur(g,1.1*1.8);D=g1-.985*g2;eps=-.004;phi=60
    lines=np.clip(1-np.where(D>=eps,1,1+np.tanh(phi*(D-eps))),0,1)
    # suppress the soft, blurry background: keep lines only where there is real detail
    det=blur(np.abs(g-blur(g,3)),6);det=np.clip((det-.012)/.03,0,1);lines*=det
    subj=person  # where the person is (sharp detail), not the blurry garden
    gb1=blur(g,2.2);gb2=blur(g,4.4);D2=gb1-.98*gb2;l2=np.clip(1-(1+np.tanh(40*(D2+.006))),0,1)*subj  # softer, wider lines for the suit and folds
    lines=np.maximum(lines,l2*.7)
    # cross-hatching for the dark areas
    h,w=g.shape;yy,xx=np.mgrid[0:h,0:w].astype(np.float32);rng=np.random.default_rng(3)
    tone=1-blur(g,2.2);wob=blur(rng.random((h,w)).astype(np.float32),4)*6
    def hatch(ang,sp,thr):
        a=np.deg2rad(ang);p=(xx*np.cos(a)+yy*np.sin(a)+wob)%sp;ln=np.clip(1-np.abs(p-sp/2)/.9,0,1)
        return ln*np.clip((tone-thr)/.18,0,1)
    hat=np.maximum.reduce([hatch(48,7,.45),hatch(-40,8,.66),hatch(20,6,.82)])*.55*subj
    shade=np.clip(tone-.35,0,1)**1.2*.42*subj
    ink=np.clip(np.maximum(np.maximum(lines*.95,hat),shade),0,1)
    grain=blur(rng.random((h,w)).astype(np.float32),.6);ink=np.clip(ink*(.8+.4*grain),0,1)
    paper=np.array([240,236,228],dtype=np.float32)*(0.985+0.03*grain[...,None]);lead=np.array([52,51,49],dtype=np.float32)
    rgb=paper+(lead-paper)*ink[...,None]
    Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).save(dst,'WEBP',quality=82,method=6)
if __name__=='__main__':pencil(sys.argv[1],sys.argv[2])
