
from numpy import sin, cos
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import math

m_E = 5.9742 * 10**24  # Mass of the Earth in kg
m_M = 7.35 * 10**22 # Mass of the Moon in kg

G = 6.6726 * 10**(-11) # Gravitational constant in N m^2 kg^-2
d = 3.844 * 10**8 #Earth-Moon distance in m
pi = math.pi 
d_E = d*m_M/(m_M + m_E) # Distance of Earth to center of mass
d_M = d*m_E/(m_M + m_E) # Distance of Moon to center of mass


def kpIII_T(a,M):  #Returns the period of orbit in seconds calculated using Kepler's third law. 'a' is the radius of orbit, and 'M' is mass of system
    G = 6.6726 * 10**(-11)
    return math.sqrt(4*math.pi**2 * a**3/(G*M))

T_EM = kpIII_T(d,m_E+m_M) # Period of Earth-Moon Orbit

def earth_pos_evolver(dt, t_0 = 0):
    theta_0 = (t_0*2*pi/T_EM) + math.pi 
    d_theta = dt*2*pi/T_EM
    tot_theta = theta_0+d_theta
    fin_theta = ((tot_theta/(2*pi))-((tot_theta/(2*pi))//1))*2*pi
    #The above line limits the final angle to be between 0 and 2pi (as in 5pi becomes pi) to mitigate the error caused by the math.trig functios
    return np.array([d_E*math.cos(fin_theta),d_E*math.sin(fin_theta)])  #There is an error produced by the math.sin function and the value of pi

def moon_pos_evolver(dt, t_0 = 0):
    theta_0 = (t_0*2*pi/T_EM)
    d_theta = dt*2*pi/T_EM
    tot_theta = theta_0+d_theta
    fin_theta = ((tot_theta/(2*pi))-((tot_theta/(2*pi))//1))*2*pi #See earth evolver for explanation on errors and angle rounding
    return np.array([d_M*math.cos(fin_theta),d_M*math.sin(fin_theta)])  #There is an error produced by the math.sin function and the value of pi

def acceleration_calc(r,r_E,r_M): #returns the acceleration of an object at position r in the Earth-Moon system
    return -G*m_E*((r-r_E)/np.linalg.norm(r-r_E)**3) -G*m_M*((r-r_M)/np.linalg.norm(r-r_M)**3)

def te_v(v,a,dt, show_error = False): #Calculates the next velocity using a Taylor expansion
    if show_error:
        return [v + dt*a,dt**2]
    return v+dt*a

def te_r(r,v,a,dt,show_error = False): #Calculates the next position using Taylor expansion method
    if show_error:
        return [r + dt*v + (dt**2)*a/2, dt**3]
    return r + dt*v + (dt**2)*a/2

###########################
dt = 1
t_max = 1209600
animation_length = 10 #Animation length in seconds

r0 = np.array([3.076319*10**8,0])
v0 = np.array([0,0])
t = 0
playback_speed = int((t_max*0.01*3)/(dt*animation_length))
print(playback_speed)
frame_num = 0
nstep = int((t_max-t)/(dt*playback_speed))
all_E_pos = [np.array([-1*d_E,0])]
all_M_pos = [np.array([d_M,0])]
E_pos_shown = [np.array([-1*d_E,0])]
M_pos_shown = [np.array([d_M,0])]
r_pos_shown = [r0]
all_r = [r0]
all_v = [v0]
all_a = []

while t < t_max:
    frame_num += 1
    all_a += [acceleration_calc(all_r[-1],all_E_pos[-1],all_M_pos[-1])]
    all_r += [te_r(all_r[-1],all_v[-1],all_a[-1],dt)]
    all_v += [te_v(all_v[-1],all_a[-1],dt)]
    t += dt
    all_E_pos += [earth_pos_evolver(dt, t_0 = t)]
    all_M_pos += [moon_pos_evolver(dt,t_0 = t)]
    if frame_num%playback_speed == 0:
        E_pos_shown += [all_E_pos[-1]]
        M_pos_shown += [all_M_pos[-1]]
        r_pos_shown += [all_r[-1]]
    

int_ms=10 # interval between frames in ms
lag=50

fig=plt.figure(figsize=(12,12))

xmin=-1.25*d
xmax=-xmin
ymin=xmin
ymax=xmax
ax=fig.add_subplot(111,autoscale_on=True,xlim=(xmin,xmax),ylim=(ymin,ymax))
ax.set_aspect('equal')
orbit0,=ax.plot([],[],'o-',lw=2)
trail0,=ax.plot([],[],'b-',lw=1)
orbit1,=ax.plot([],[],'o-',lw=2)
trail1,=ax.plot([],[],'r-',lw=1)
orbit2,=ax.plot([],[],'o-',lw=2)
trail2,=ax.plot([],[],'g-',lw=1)
x0,y0,x1,y1,x2,y2=[],[],[],[],[],[]

def animate_all(i):
    modified = []
    if i>lag:
        imin=i-lag
    else:
        imin=0
    
    thisx=[E_pos_shown[i][0]]
    thisy=[E_pos_shown[i][1]]
    orbit0.set_data(thisx,thisy)
    x0=np.array(E_pos_shown)[imin:i,0]
    y0=np.array(E_pos_shown)[imin:i,1]
    trail0.set_data(x0,y0)
    #######
    thisx=[M_pos_shown[i][0]]
    thisy=[M_pos_shown[i][1]]
    orbit1.set_data(thisx,thisy)
    x1=np.array(M_pos_shown)[imin:i,0]
    y1=np.array(M_pos_shown)[imin:i,1]
    trail1.set_data(x1,y1)
    ######
    thisx=[r_pos_shown[i][0]]
    thisy=[r_pos_shown[i][1]]
    orbit2.set_data(thisx,thisy)
    x2=np.array(r_pos_shown)[imin:i,0]
    y2=np.array(r_pos_shown)[imin:i,1]
    trail0.set_data(x2,y2)
    modified+=[orbit0,trail0,orbit1,trail1,orbit2,trail2]
    return modified

ani=animation.FuncAnimation(fig,animate_all,range(1,nstep),interval=int_ms,blit=True,repeat=False)
plt.show()


