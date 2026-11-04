# human-like pen animation of the signature → animated WebP
import asyncio,json,base64,io,sys
from PIL import Image
from playwright.async_api import async_playwright
SVG=json.load(open('../pf/sig2.json'))['load']
FPS=40;W,H=1640,404
JS=r"""
(svgText)=>{
 const host=document.createElement('div');host.innerHTML=svgText;document.body.appendChild(host);
 const svg=host.querySelector('svg');const vb=svg.getAttribute('viewBox').split(/\s+/).map(Number);
 const sx=%W%/vb[2],sy=%H%/vb[3];
 // seeded random so every build is identical
 let s=7;const R=()=>{s=(s*16807)%2147483647;return (s-1)/2147483646};
 const paths=[...svg.querySelectorAll('path')];const segs=[];let t=0;
 const V=150; // base pen speed (viewBox units / s)
 paths.forEach((p,pi)=>{const L=p.getTotalLength();if(L<1)return;
   const N=Math.max(4,Math.ceil(L/0.6));const pts=[];for(let i=0;i<=N;i++){const q=p.getPointAtLength(L*i/N);pts.push([q.x,q.y])}
   // pen lift before each stroke: short and uneven, longer before the second word
   if(pi>0){const big=(pts[0][0]>300&&!segs.bigDone);if(big)segs.bigDone=1;t+=big?0.16+R()*0.06:0.035+R()*0.07}
   const ph1=R()*6.28,ph2=R()*6.28,mood=0.85+R()*0.35; // each stroke has its own tempo
   const raw=[],ds=[];
   for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i],c=pts[Math.min(pts.length-1,i+1)];
     const d=Math.hypot(b[0]-a[0],b[1]-a[1]);const a1=Math.atan2(b[1]-a[1],b[0]-a[0]),a2=Math.atan2(c[1]-b[1],c[0]-b[0]);let da=Math.abs(a2-a1);if(da>Math.PI)da=2*Math.PI-da;
     const curv=da/Math.max(d,0.01),u=i/pts.length,ease=Math.min(1,0.35+u*7)*Math.min(1,0.45+(1-u)*5),wob=1+0.12*Math.sin(u*9+ph1)+0.07*Math.sin(u*23+ph2);
     raw.push(V*mood*wob*ease/(1+curv*5.5));ds.push(d)}
   // smooth the speed so the line flows instead of jittering
   const K=14,vs=raw.map((_,i)=>{let sum=0,n=0;for(let j=Math.max(0,i-K);j<=Math.min(raw.length-1,i+K);j++){sum+=raw[j];n++}return sum/n});
   for(let i=1;i<pts.length;i++){const v=vs[i-1],a=pts[i-1],b=pts[i],u=i/pts.length;t+=ds[i-1]/Math.max(v,12);
     const w=2.05*(0.86+0.26*Math.min(1,26/Math.max(v,1)));
     segs.push([a[0],a[1],b[0],b[1],t,w])}
 });
 return {segs,total:t,vb,sx,sy};
}"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page()
    await pg.set_content('<html><body></body></html>')
    r=await pg.evaluate(JS.replace('%W%',str(W)).replace('%H%',str(H)),SVG)
    total=r['total'];print('natural duration',round(total,2))
    target=float(sys.argv[1]) if len(sys.argv)>1 else 2.75
    k=target/total
    frames=await pg.evaluate("""({segs,k,vb,sx,sy,fps,W,H})=>{
      const c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');g.lineCap='round';g.lineJoin='round';g.strokeStyle='#E35A32';
      const out=[];let i=0;const n=Math.ceil(segs[segs.length-1][4]*k*fps)+1;
      for(let f=1;f<=n;f++){const T=f/fps;while(i<segs.length&&segs[i][4]*k<=T){const s=segs[i];g.lineWidth=s[5]*sx;g.beginPath();g.moveTo((s[0]-vb[0])*sx,(s[1]-vb[1])*sy);g.lineTo((s[2]-vb[0])*sx,(s[3]-vb[1])*sy);g.stroke();i++}
        out.push(c.toDataURL('image/png'))}
      return out}""",{'segs':r['segs'],'k':k,'vb':r['vb'],'sx':r['sx'],'sy':r['sy'],'fps':FPS,'W':W,'H':H})
    ims=[Image.open(io.BytesIO(base64.b64decode(f.split(',')[1]))).convert('RGBA') for f in frames]
    # a clear first frame so nothing shows before the pen starts
    ims=[Image.new('RGBA',(W,H),(0,0,0,0))]+ims
    dur=[1000//FPS]*len(ims);dur[-1]=3000
    ims[0].save('sig_anim.webp',save_all=True,append_images=ims[1:],duration=dur,loop=1,quality=80,method=6,lossless=False,allow_mixed=True)
    import os;print(len(ims),'frames',os.path.getsize('sig_anim.webp'),'bytes')
    ims[-1].save('last.png');ims[len(ims)//3].save('third.png')
    await b.close()
asyncio.run(main())
