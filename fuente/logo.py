# Genera la silueta del logo como trazo caligráfico (relleno, ancho variable)
import math
def bez(p0,p1,p2,p3,t):
    u=1-t;return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
# linea central del lado izquierdo: hombro -> cintura -> cadera -> muslo
segs=[((31,4),(22,26),(42,44),(39,64)),((39,64),(36,82),(12,90),(17,112)),((17,112),(21,130),(34,136),(37,148))]
pts=[]
for i,s in enumerate(segs):
    for k in range(0 if i==0 else 1,17): pts.append(bez(*s,k/16))
n=len(pts)
def w(i):
    t=i/(n-1)
    base=1.2+5.6*math.sin(math.pi*min(1,t*1.05))**1.3   # fino en los extremos
    hip=2.2*math.exp(-((t-0.62)/0.13)**2)               # más cuerpo en la cadera
    return (base+hip)/2
L=[];R=[]
for i,(x,y) in enumerate(pts):
    a=pts[max(0,i-1)];b=pts[min(n-1,i+1)]
    dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);nx,ny=-dy/l,dx/l
    L.append((x+nx*w(i),y+ny*w(i)));R.append((x-nx*w(i),y-ny*w(i)))
poly=L+R[::-1]
d="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in poly)+"Z"
mirror="M"+" L".join(f"{100-x:.1f} {y:.1f}" for x,y in poly)+"Z"
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 152"><path fill="#D93A7A" d="{d}"/><path fill="#16A39A" d="{mirror}"/></svg>'''
open('../logo/silueta.svg','w').write(svg)
open('../logo/paths.txt','w').write(d+"\n"+mirror)
print(len(svg))
