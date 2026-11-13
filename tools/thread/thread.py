import sys,json,re
S,O=sys.argv[1],sys.argv[2];h=open(S).read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:80],h.count(a));h=h.replace(a,b)
a=h.index("  // hero\n");e=h.index("  h+=contactHtml(links);\n")+len("  h+=contactHtml(links);\n")
h=h[:a]+"  h+=thHome(P,links);h+='</div>';\n  h+=contactHtml(links);\n"+h[e:]
rep("logo-mark\">'+esc(initials(P.name))+'</span>","logo-mark\">'+TH_AV+'</span>")
rep("function buildDoc(){","function buildDoc0(){")
rep("['shots','Shots'],","['home','Homepage'],['drawer','Unreleased'],")
rep("  if(t==='shots'){","  if(t==='home')return thAdminHome();if(t==='drawer')return thAdminDrawer();\n  if(t==='shots'){")
rep("function wire(){blendCovers();","function wire(){blendCovers();thWire();")
rep("function dots(){",open('thread.js').read()+"\nfunction dots(){")
m=re.search(r'(<script type="application/json" id="state">)(.*?)(</script>)',h,re.S)
st=json.loads(m.group(2))
NEW={'qarar-hiring-dashboard':'#96482E','tryout':'#9E3466','workspace-enhancements':'#337465','steel-construction-tool':'#88622F','chatbot-vs-ai-agent':'#685DB0'}
for p in st['projects']:
    if p['id'] in NEW: p['color']=NEW[p['id']]
if 'drawer' not in st: st['drawer']=[{'id':'widebot-d','title':'WideBot','sub':'Calm enterprise homepage','note':'Concept · not shipped','meta':['Arabic-first, English and Arabic','Version D of five directions','Names and numbers are demo values'],'proto':'drawer/widebot-d.html',
 'pins':[
  {'s':'top','poster':'drawer/wbs-top.webp','cap':'the homepage','w':9,'r':-1.4},
  {'s':'flow','poster':'drawer/wbs-flow.webp','cap':'one request, start to finish','w':6,'r':1.3,'dy':10,'hint':'plays on hover','scrub':1},
  {'s':'live','poster':'drawer/wbs-live.webp','cap':'requests being solved right now','w':6,'r':-1.1,'dy':50}]}]
js=json.dumps(st,ensure_ascii=False).replace('</','<\\/')
h=h[:m.start(2)]+js+h[m.end(2):]
h=h.replace("family=Bricolage+Grotesque","family=Caveat:wght@400;500;600&family=Archivo:wdth,wght@62..125,400..900&family=Bricolage+Grotesque")
h=h.replace("<title>Andrew Victor Portfolio</title>","<title>Andrew Victor Thread</title>")
rep("$('#csBack').onclick=function(){closeCase()};","$('#csBack').onclick=function(){closeCase()};thCs();")
sg=json.load(open('sig2.json'))
import base64
SIGIMG='data:image/webp;base64,'+base64.b64encode(open('sig_anim.webp','rb').read()).decode()
AV='<svg class="th-mark" viewBox="0 0 132 104" aria-hidden="true"><path class="s1" d="M8 98 L40 6 L72 98"/><path class="s2" d="M22 62 L58 62"/><path class="s3" d="M56 6 L90 98 L124 6"/></svg>'
LOAD='<div class="th-load" id="thLoad" aria-hidden="true"><div class="th-sigw"><img id="thSigImg" alt="" width="820" height="202" data-src="'+SIGIMG+'"></div>'+'</div><script>(function(){var L=document.getElementById("thLoad"),R=matchMedia("(prefers-reduced-motion: reduce)").matches;if(R){L.remove();return}document.documentElement.classList.add("th-loading");var started=0;function x(){if(L.classList.contains("out"))return;var y=null;try{var f=document.getElementById("thFl"),p=f.getPointAtLength(f.getTotalLength()*.995),m=f.getScreenCTM();y=p.x*m.b+p.y*m.d+m.f}catch(e){}L.classList.add("out");if(window.__thHandoff)window.__thHandoff(y);else document.documentElement.classList.remove("th-loading");setTimeout(function(){L.remove()},1700)}function go(){if(started)return;started=1;requestAnimationFrame(function(){requestAnimationFrame(function(){var si=document.getElementById("thSigImg");L.classList.add("go");setTimeout(function(){si.onerror=function(){si.style.visibility="hidden"};si.src=si.getAttribute("data-src")},350);setTimeout(x,3300)})})}L.onclick=x;if(document.readyState!=="loading")go();else document.addEventListener("DOMContentLoaded",go);setTimeout(go,4000)})();</script>'
h=h.replace('</style></head><body>','</style></head><body>'+LOAD+'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><filter id="zzPencil" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter></svg>',1)
e=h.index('</style>',h.index('<style id="css">'));h=h[:e]+open('thread.css').read()+h[e:]
h=h.replace('<div class="cal" id="cal" aria-label="Pick a time to talk">','<div class="cal" id="cal" aria-label="Pick a time to talk"><svg class="th-calline" aria-hidden="true"><rect x="0.8" y="0.8" width="99%" height="99%" rx="18" pathLength="1"/></svg>',1)
open(O,'w').write(h);print('ok',round(len(h)/1e6,2))
