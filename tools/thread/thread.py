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
rep("<a class=\"btn sm dark nav-cta\" href=\"#book\" data-book>Book a call</a>","'+(function(){var hr=thHomeData().hero;return hr.cv?'<a class=\"nav-cv\" href=\"'+esc(hr.cv)+'\"'+thCvAttr(hr)+'>CV ↓</a>':''})()+'<a class=\"btn sm dark nav-cta\" href=\"#book\" data-book>Book a call</a>")
rep("  if(!force&&Date.now()-ag.lastBubble<14000)return false;","  if(!force&&Date.now()-ag.lastBubble<14000)return false;if(innerWidth<760){if(ag.mob1)return false;ag.mob1=1}")
rep("function dots(){",open('thread.js').read()+"\nfunction dots(){")
m=re.search(r'(<script type="application/json" id="state">)(.*?)(</script>)',h,re.S)
st=json.loads(m.group(2))
NEW={'qarar-hiring-dashboard':'#96482E','tryout':'#9E3466','workspace-enhancements':'#337465','steel-construction-tool':'#88622F','chatbot-vs-ai-agent':'#685DB0'}
for p in st['projects']:
    if p['id'] in NEW: p['color']=NEW[p['id']]
st['education']['years']='2020 – 2024'
st['experience']=[
 {'company':'WideBot','role':'Product Designer','meta':'Cairo, Egypt · Full-time · Hybrid','period':'Jun 2026 — Present','points':[
  'QARAR: owned a hiring dashboard end to end, replacing about 10 tools for WideBot’s HR team.',
  'Tryout: designed and built a usability testing tool for HTML prototypes, live with real testers in 6 days.',
  'Onboarding and underwriting (KYB and KYC): took shop owners from sign-up to a live AI agent in 6 steps, in English and Arabic; 5 of 5 test participants finished in 2 minutes without help.',
  'Connected data to AI agents: designed how users connect their databases so agents answer from the business’s own data.',
  'AI agents (voice and text): designed the experience for building, customizing and managing them.',
  'Workspace: usability tests with 15 users showed 80% missed the main button; the redesign cut setup from up to 15 minutes to 1–3.']},
 {'company':'WideBot','role':'Junior Product Designer','meta':'Cairo, Egypt · Full-time · Hybrid','period':'Jun 2024 — Jun 2026','points':[
  'Led the complete UI overhaul of the sign-up flow; 70% of users now register faster and with fewer errors.',
  'Led the redesign of the bot training interface, making it simpler for non-technical users.',
  'Refined the Live Chat inbox for quicker, less frustrating navigation across conversations.',
  'Contributed to the omnichannel service architecture unifying WhatsApp, Facebook and other platforms.',
  'Designed the add-ons marketplace, a PayTabs checkout flow, WooCommerce integration and Add-ons management inside the Wallet.']},
 {'company':'Placement Dost','role':'UI/UX Designer · Intern','meta':'Bengaluru, India · Internship','period':'Mar 2024 — Jun 2024','points':[
  'Participated in 3 full product redesigns focused on student and job-seeker usability.',
  'Created 20+ wireframes and interactive prototypes in Figma for rapid testing and iteration.',
  'Ran usability testing sessions and applied the feedback to improve onboarding.',
  'Worked with senior designers to standardize a mini design system across the platform.']}]
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
LOAD='<div class="th-load" id="thLoad" aria-hidden="true"><div class="th-sigw"><img id="thSigImg" alt="" width="820" height="202" data-src="'+SIGIMG+'"></div>'+'</div><script>(function(){var L=document.getElementById("thLoad"),R=matchMedia("(prefers-reduced-motion: reduce)").matches;if(R){L.remove();return}document.documentElement.classList.add("th-loading");var started=0;function x(){if(L.classList.contains("out"))return;var y=null;try{var f=document.getElementById("thFl"),p=f.getPointAtLength(f.getTotalLength()*.995),m=f.getScreenCTM();y=p.x*m.b+p.y*m.d+m.f}catch(e){}L.classList.add("out");if(window.__thHandoff)window.__thHandoff(y);else document.documentElement.classList.remove("th-loading");setTimeout(function(){L.remove()},1700)}function go(){if(started)return;started=1;requestAnimationFrame(function(){requestAnimationFrame(function(){var si=document.getElementById("thSigImg");L.classList.add("go");setTimeout(function(){si.onerror=function(){si.style.visibility="hidden"};si.src=si.getAttribute("data-src")},350);setTimeout(x,1100)})})}L.onclick=x;["wheel","touchstart","keydown"].forEach(function(e){addEventListener(e,x,{once:true,passive:true})});try{if(sessionStorage.getItem("th-seen")){L.classList.add("go");setTimeout(x,0)}sessionStorage.setItem("th-seen","1")}catch(e){}if(document.readyState!=="loading")go();else document.addEventListener("DOMContentLoaded",go);setTimeout(go,4000)})();</script>'
h=h.replace('</style></head><body>','</style></head><body>'+LOAD+'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><filter id="zzPencil" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter></svg>',1)
e=h.index('</style>',h.index('<style id="css">'));h=h[:e]+open('thread.css').read()+h[e:]
h=h.replace('<div class="cal" id="cal" aria-label="Pick a time to talk">','<div class="cal" id="cal" aria-label="Pick a time to talk"><svg class="th-calline" aria-hidden="true"><rect x="0.8" y="0.8" width="99%" height="99%" rx="18" pathLength="1"/></svg>',1)
open(O,'w').write(h);print('ok',round(len(h)/1e6,2))
