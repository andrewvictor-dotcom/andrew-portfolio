# turn the Thread artifact build into the live site's index.html (Vercel + Supabase + Gemini Zizo)
import re,sys,json,html
src,live,out=sys.argv[1],sys.argv[2],sys.argv[3]
t=open(src).read();L=open(live).read()
la=re.search(r'<script type="text/plain" id="app">(.*?)</script>',L,re.S).group(1)
m=re.search(r'<script id="app">(.*?)</script>',t,re.S);ta=m.group(1)
# 1. Zizo answers come from the site's own server (Gemini) instead of the Claude preview runtime
old="if(window.claude&&window.claude.use){window.claude.use('sample').then(function(f){ag.fn=f||null;if(ag.open)renderAgent()},function(){ag.fn=null})}else ag.fn=null;"
assert old in ta;ta=ta.replace(old,"ag.fn=zizoServer;")
# 2. editing: owner login + publish to Supabase (taken from the current live site)
web=la[la.index('/* ---------- web: owner login'):la.index('/* ---------- boot')]
web=web.replace("sb.from('site').upsert({id:'main',data:state,","sb.from('site').upsert({id:'main',data:thLockedCopy(state),")
assert 'thLockedCopy(state)' in web
def fn(code,name):
    i=code.index('function '+name+'(');k=code.index('{',i);d=0;q=None;e=False
    for x in range(k,len(code)):
        c=code[x]
        if q:
            if e:e=False
            elif c=='\\':e=True
            elif c==q:q=None
            continue
        if c in '\'"':q=c
        elif c=='{':d+=1
        elif c=='}':
            d-=1
            if d==0:return code[i:x+1]
lp=fn(la,'publish');tp=fn(ta,'publish')
print(len(lp),len(tp))
ta=ta.replace(tp,lp)
ta=ta.replace('/* ---------- boot ----------',web+'/* ---------- boot ----------',1)
ta=ta.replace("if(/^#p-[a-z0-9-]+$/.test(location.hash)){var hid=location.hash.slice(3);setTimeout(function(){openCaseQuiet(hid)},60)}\n(function(){","if(/^#p-[a-z0-9-]+$/.test(location.hash)){var hid=location.hash.slice(3);setTimeout(function(){openCaseQuiet(hid)},60)}\nownerBoot();\n(function(){",1)
assert 'ownerBoot();' in ta
t=t[:m.start()]+'<script>window.SITE='+json.dumps({'url':'https://cegbdtgmhgsngfrstigc.supabase.co','key':'sb_publishable_Eccdsxg6cOV1P690TKmdEg_7fmbbkck','owner':'andrw.victor2@gmail.com'})+';</script>\n<script type="text/plain" id="app">'+ta+'</script>\n<script>'+re.search(r'<script>(\(function\(\)\{var S=window\.SITE.*?)</script>',L,re.S).group(1)+'</script>'+t[m.end():]
# 3. head: title, description, sharing preview, icon
st=json.loads(re.search(r'id="state">(.*?)</script>',t,re.S).group(1).replace('<\\/','</'))
P=st['profile'];title=P['name']+' · '+P['role'];desc=P['lede'];B='https://andrew-portfolio-lemon.vercel.app'
fav="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23D9643C'/%3E%3Ctext x='32' y='42' font-family='Arial,sans-serif' font-weight='800' font-size='26' text-anchor='middle' fill='%23fff'%3EAV%3C/text%3E%3C/svg%3E"
head=f'''<meta name="description" content="{html.escape(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{B}/"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{B}/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#121214"><link rel="icon" href="{fav}"><link rel="preconnect" href="https://cegbdtgmhgsngfrstigc.supabase.co" crossorigin>
'''
t=re.sub(r'<title>[^<]*</title>','<title>'+html.escape(title)+'</title>\n'+head.replace('\\','\\\\'),t,count=1)
ROW='thread'
t=t.replace("site?id=eq.main&","site?id=eq."+ROW+"&").replace("upsert({id:'main',","upsert({id:'"+ROW+"',")
assert t.count('eq.'+ROW)==1 and t.count("{id:'"+ROW+"'")==1
open(out,'w').write(t);json.dump(st,open(out+'.content.json','w'),ensure_ascii=False)
print('web build',round(len(t)/1024),'KB')
