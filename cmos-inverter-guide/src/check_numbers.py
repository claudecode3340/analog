import sys; sys.path.insert(0, 'src')
from model import *
import numpy as np
u=1e-6
print('WE23.1', closed(5,1,-1,2), crit(5,1,-1,2,1))
print('Q1.1', closed(3.3,.6,-.7,2.5), crit(3.3,.6,-.7,200,80))
print('Q2.1', closed(3.3,.6,-.7,1.6), crit(3.3,.6,-.7,480,300))
print('Q2.4', closed(5,1,-1,4))
print('sym 2.5/0.6', closed(2.5,.6,-.6,1))
print('Q2.7 razavi', closed(3,.7,-.8,134.3/38.4))
print('capstone', closed(2.5,.5,-.5,2), crit(2.5,.5,-.5,300,150))
# pseudo NMOS
V=3.3; Ip=40e-6*2.6**2; a=np.roots([1,-5.4,Ip/100e-6]); print('pseudo VOL',a, Ip, V*Ip)
def delays(C,VDD,vtn,vtp,kn,kp):
    a=abs(vtp)
    phl=C/(kn*(VDD-vtn))*(2*vtn/(VDD-vtn)+np.log(4*(VDD-vtn)/VDD-1))
    plh=C/(kp*(VDD-a))*(2*a/(VDD-a)+np.log(4*(VDD-a)/VDD-1))
    V50=VDD/2
    i1=kn/2*(VDD-vtn)**2; i2=kn/2*(2*(VDD-vtn)*V50-V50**2) if V50<VDD-vtn else kn/2*(VDD-vtn)**2
    avg_hl=C*V50/((i1+i2)/2)
    j1=kp/2*(VDD-a)**2; j2=kp/2*(2*(VDD-a)*V50-V50**2) if V50<VDD-a else j1
    avg_lh=C*V50/((j1+j2)/2)
    return phl,plh,avg_hl,avg_lh,(i1,i2,j1,j2)
print('WE25.2', delays(0.3e-12,3.3,.6,-.7,200e-6,80e-6))
d=delays(0.3e-12,3.3,.6,-.7,200e-6,80e-6); print('Q3.3 ratio', d[1]/d[0])
print('capstone delays', delays(50e-15,2.5,.5,-.5,300e-6,150e-6))
# Q3.4/3.5
kn=134.3e-6*100; C=1e-12
print('Q3.4', C/(kn*2.3)*np.log(1*(4.6-.5)/(.5*(4.6-1))))
print('Q3.5', 2*C/kn*(1/0.3-1/1.3))
# Q1.4 (now 2.6)
kR=((3-.8-1.5)/(1.5-.7))**2; kn=134.3e-6*20; kp=kn/kR; I=kn/2*.8**2
gm1=kn*.8; gm2=kp*.7; ro1=1/(.1*I); ro2=1/(.2*I); rp=ro1*ro2/(ro1+ro2)
print('Q2.6',kR,kp/38.4e-6,I,gm1,gm2,ro1,ro2,rp,-(gm1+gm2)*rp)
# Q0.5
print('Q0.5', 134.3e-6*100/2*0.8**2, 38.4e-6*100/2*0.7**2)
# Q3.7 Razavi table cap
Cgdn=0.4*5; Cgdp=0.3*10; Cdbn=5*1.5*0.56+2*6.5*0.035; Cdbp=10*1.5*0.94+2*11.5*0.032; Cg=3.84*(5*.5+10*.5)
Ct=Cgdn+Cgdp+Cdbn+Cdbp+Cg; I=134.3e-6*10/2*2.3**2
print('Q3.7',Cgdn,Cgdp,Cdbn,Cdbp,Cg,Ct, I, Ct*1e-15*3/I)
print('Q3.1', 3.8*.08, 3.8*2.5*.08, 3.8*(.5+1.25), 3.8*.08+3.8*2.5*.08+2+4+5+3.8*1.75)
print('Q2.3', ((1.65-.7)/(1.65-.6))**2, (580/230)/((1.65-.7)/(1.65-.6))**2)
