import json,html,sys
BASE=sys.argv[1] if len(sys.argv)>1 else 'https://andrew-portfolio.vercel.app'
st=json.load(open('build/content.json'))
css=open('build/style.css').read();app=open('build/app.web.js').read()
P=st['profile']
title=P['name']+' · '+P['role']
desc=P['lede']
cfg={'url':'https://cegbdtgmhgsngfrstigc.supabase.co','key':'sb_publishable_Eccdsxg6cOV1P690TKmdEg_7fmbbkck','owner':'andrw.victor2@gmail.com'}
j=json.dumps(st,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
links=''.join('<a href="%s">%s</a> '%(html.escape(l['url']),html.escape(l['label'])) for l in st.get('links',[]))
fav="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23101218'/%3E%3Ctext x='32' y='42' font-family='Arial,sans-serif' font-weight='800' font-size='26' text-anchor='middle' fill='%23fff'%3EAV%3C/text%3E%3C/svg%3E"
loader="""(function(){var S=window.SITE,done=false;
function go(d){if(done)return;done=true;if(d&&d.profile)document.getElementById('state').textContent=JSON.stringify(d);var a=document.getElementById('app'),s=document.createElement('script');s.text=a.textContent;document.body.appendChild(s)}
var t=setTimeout(function(){go(null)},1500);
try{fetch(S.url+'/rest/v1/site?id=eq.live&select=data',{headers:{apikey:S.key,Authorization:'Bearer '+S.key}}).then(function(r){return r.ok?r.json():null}).then(function(j){clearTimeout(t);go(j&&j[0]&&j[0].data)},function(){clearTimeout(t);go(null)})}catch(e){clearTimeout(t);go(null)}})();"""
doc=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}/">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{BASE}/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#E8EBF0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D0F13" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://cegbdtgmhgsngfrstigc.supabase.co" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap">
<style id="css">{css}</style>
</head>
<body>
<div id="root"></div>
<noscript><main style="max-width:680px;margin:40px auto;padding:0 16px;font-family:system-ui,sans-serif"><h1>{html.escape(P['name'])}</h1><p>{html.escape(P['role'])} · {html.escape(P['location'])}</p><p>{html.escape(desc)}</p><p>{html.escape(P['email'])}</p><p>{links}</p></main></noscript>
<script type="application/json" id="state">{j}</script>
<script>window.SITE={json.dumps(cfg)};</script>
<script type="text/plain" id="app">{app}</script>
<script>{loader}</script>
</body>
</html>
'''
open('index.html','w').write(doc)
print('index.html',round(len(doc)/1024),'KB')
