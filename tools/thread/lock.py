# encrypt the private parts of locked case studies (AES-GCM, key from the password via PBKDF2)
import re,sys,json,os,base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
src,out,pw=sys.argv[1],sys.argv[2],open('lock_pw.txt').read().strip()
IDS=['qarar-hiring-dashboard'];PRIV=['gallery','stages','story','intro','problem','outcome','tldr','tools','galleryNoun','galleryTitle','anim']
h=open(src).read();m=re.search(r'(<script type="application/json" id="state">)(.*?)(</script>)',h,re.S);s=json.loads(m.group(2))
def empty(v):return [] if isinstance(v,list) else {} if isinstance(v,dict) else '' if isinstance(v,str) else None
IT=210000
for p in s['projects']:
    if p['id'] not in IDS:continue
    priv={k:p[k] for k in PRIV if k in p}
    salt,iv=os.urandom(16),os.urandom(12)
    key=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=IT).derive(pw.encode())
    ct=AESGCM(key).encrypt(iv,json.dumps(priv).encode(),None)
    for k in priv:p[k]=empty(priv[k])
    b=lambda x:base64.b64encode(x).decode()
    p['lock']={'salt':b(salt),'iv':b(iv),'ct':b(ct),'it':IT}
s['profile']['phone']='+20 121 046 5729'
txt=json.dumps(s).replace('</','<\\/')
h=h[:m.start(2)]+txt+h[m.end(2):]
open(out,'w').write(h);print('locked',IDS)
