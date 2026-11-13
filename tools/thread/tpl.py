# store a tiny page template (everything except the big CSS, app and state blocks) so "Publish changes" in the editor rebuilds this exact page
import sys,json
src,out=sys.argv[1],sys.argv[2];h=open(src).read()
def span(start,end_tag):
    a=h.index(start)+len(start);b=h.index(end_tag,a);return a,b
assert 'id="th-tpl"' not in h
i=h.index('<script id="app">');h=h[:i]+'<script type="application/json" id="th-tpl">\u0001T\u0001</script>\n'+h[i:]
c=span('<style id="css">','</style>');s=span('<script type="application/json" id="state">','</script>');a=span('<script id="app">','</script>')
assert c[1]<s[0]<a[0]
T=h[:c[0]]+'\u0001C\u0001'+h[c[1]:s[0]]+'\u0001S\u0001'+h[s[1]:a[0]]+'\u0001A\u0001'+h[a[1]:]
tj=json.dumps(T).replace('<','\\u003c')
h=h.replace('\u0001T\u0001',tj,1)
open(out,'w').write(h);print('template',len(T),'chars')
