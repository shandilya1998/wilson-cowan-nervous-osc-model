import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

class WilsonCowan(object):
    def __init__(self, Tu, Tv, a, b, c, d, Su, Sv, mu, f = np.tanh, dt = 0.001, n = 10000000):
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
        self.u = 0.0
        self.v = 0.0
        self.n = n
        self.Au = np.zeros((self.n,))
        self.Av = np.zeros((self.n,))
        self.Ay = np.zeros((self.n,))
        self.dt = dt
  
    def du(self):
        return (self.f(self.mu*(self.a*self.u - self.b*self.v + self.Su)) - self.u)/self.Tu

    def dv(self):
        return (self.f(self.mu*(self.c*self.u - self.d*self.v + self.Sv)) - self.v)/self.Tv

    def simulate(self):
        for i in tqdm(range(self.n)):
            self.Au[i] = self.u
            self.Av[i] = self.v
            self.Ay[i] = self.u - self.v
            self.u += self.dt*self.du()
            self.v +=self.dt*self.dv()

osc = WilsonCowan(Tu = 1, Tv = 0.2, a = 5.6, d = -2.4, b = 5.6, c = 2.4, Su = 0.02, Sv = 0.02, mu = 1)
osc.simulate()
fig, axes = plt.subplots(3, 1, figsize = (30, 10))
axes[0].plot(osc.Au[-10000:])
axes[0].set_ylabel('excitatory neuron output')
axes[0].set_xlabel('time')
axes[1].plot(osc.Av[-10000:])
axes[1].set_ylabel('inhibitory neuron output')
axes[1].set_xlabel('time')
axes[2].plot(osc.Ay[-10000:])
axes[2].set_ylabel('CPG output')
axes[2].set_xlabel('time')
fig.savefig('wilson_cowan_exp2.png')
plt.show()
