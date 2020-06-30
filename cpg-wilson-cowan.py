import numpy as np
from tqdm import tqdm 
import matplotlib.pyplot as plt

class CPGWilsonCowan(object):
    def __init__(self, Tu, Tv, a, b, c, d, Su, Sv, mu, p,W, f = np.tanh, num = 4, dt = 0.0001, n = 1000000):
        self.num = num
        self.Tu = Tu
        self.Tv = Tv
        self.a = a 
        self.b = b 
        self.c = c 
        self.d = d 
        self.Su = Su
        self.Sv = Sv
        self.f = f 
        self.mu = mu
        self.u = np.random.random((self.num,))
        self.v = np.random.random((self.num,))
        self.n = n 
        self.p = p
        self.W = W
        self.Au = np.zeros((self.n, self.num))
        self.Av = np.zeros((self.n, self.num))
        self.Ay = np.zeros((self.n, self.num))
        self.dt = dt 
        self.t = np.arange(0, self.n)*dt

    def du(self):
        du = np.zeros((self.num,))
        for i in range(self.num):
            temp = 0.0
            for j in range(self.num):
                temp += self.W[i][j]*self.u[j]
            du[i] = (self.f(self.mu[i]*(self.a[i]*self.u[i] - self.b[i]*self.v[i] + temp + self.Su[i])) - self.u[i])/self.Tu[i]
        return du

    def dv(self):
        dv = np.zeros((self.num,))
        for i in range(self.num):
            temp = 0.0 
            for j in range(self.num):
                temp += self.W[i][j]*self.v[j]
            dv[i] = (self.f(self.mu[i]*(self.c[i]*self.u[i] - self.d[i]*self.v[i] + temp + self.Sv[i])) - self.v[i])/self.Tv[i]
        return dv

    def simulate(self, disturb_time = None, gait_transition = None ):
        for i in tqdm(range(self.n)):
            self.Au[i, :] = self.u
            self.Av[i, :] = self.v
            self.Ay[i, :] = self.p*(self.u - self.v)
            self.u += self.dt*self.du()
            self.v += self.dt*self.dv()
            if disturb_time and disturb_time == i:
                self.set_u(np.random.random((self.num,)))
                self.set_v(np.random.random((self.num,)))
            
            if gait_transition and gait_transition == i:
                self.W[0][2] = -self.W[0][2]
                self.W[2][3] = -self.W[2][3]
                self.W[2][0] = -self.W[2][0]
                self.W[3][2] = -self.W[3][2]

    def get_u(self):
        return self.u + self.dt*self.du()

    def get_v(self):
        return self.v + self.dt*self.dv()     

    def set_u(self, u):
        self.u = u
    
    def set_v(self, v):
        self.v = v

    def set_W(self, W):
        self.W = W
    
    def plot(self):
        labels = []
        fig, axes = plt.subplots(3, 2, figsize=(10, 15))
        for i in range(self.num):
            axes[0, 0].plot(self.t[-50000:], self.Au[-50000:, i])
            axes[0, 1].plot(self.t[:50000], self.Au[:50000, i])
            labels.append('neuron_'+str(i))
        axes[0, 0].set_ylabel('u steady')
        axes[0, 1].set_ylabel('u initial') 
        axes[0, 0].legend(labels, loc = 'upper left')
        axes[0, 1].legend(labels, loc = 'upper left')
        labels = []
        for i in range(self.num):
            axes[1, 0].plot(self.t[-50000:], self.Ay[-50000:, i])
            axes[1, 1].plot(self.t[:50000], self.Av[:50000, i])
            labels.append('neuron_'+str(i))
        axes[1, 0].legend(labels, loc = 'upper left')
        axes[1, 1].legend(labels, loc = 'upper left')
        axes[1, 0].set_ylabel('v steady')
        axes[1, 1].set_ylabel('v initial') 
        labels = []
        for i in range(self.num):
            axes[2, 0].plot(self.t[-50000:], self.Ay[-50000:, i])
            axes[2, 1].plot(self.t[:50000], self.Ay[:50000, i])
            labels.append('neuron_'+str(i))
        axes[2, 0].set_ylabel('y steady')
        axes[2, 1].set_ylabel('y initial') 
        axes[2, 0].legend(labels, loc = 'upper left')
        axes[2, 1].legend(labels, loc = 'upper left')
        fig.savefig('plots/cpg_wilson_cowan_exp2.png')

W = np.full((4,4), -0.1)
for i in range(4):
    W[i][i] = 0.0
Tu = np.full((4,), 0.2)
Tv = np.full((4,), 0.2)
a = np.full((4,), 5.6)
b = np.full((4,), 5.6)
c = np.full((4,), 2.4)
d = np.full((4,), -2.4)
Su = np.full((4,), 0.02)
Sv = np.full((4,), 0.02)
mu = np.full((4,), 1)
osc = CPGWilsonCowan(Tu = Tu, Tv = Tv, a = a, d = d, b = b, c = c, Su = Su, Sv = Sv, mu = mu, p = 0.5, W = W) 
osc.simulate(gait_transition = 0)#disturb_time = 5000000)
osc.plot()
