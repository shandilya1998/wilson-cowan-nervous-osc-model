import numpy as np
from tqdm import tqdm 
import matplotlib.pyplot as plt

class CPGWilsonCowan(object):
    def __init__(self, Tu, Tv, a, b, c, d, Su, Sv, mu, p,W, f = np.tanh, num = 4, dt = 0.001, n = 10000000):
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
        self.u = np.zeros((self.num,))
        self.v = np.zeros((self.num,))
        self.n = n 
        self.p = p
        self.W = W
        self.Au = np.zeros((self.n, self.num))
        self.Av = np.zeros((self.n, self.num))
        self.Ay = np.zeros((self.n, self.num))
        self.dt = dt 

    def du(self):
        du = np.zeros((self.num,))
        for i in range(self.num):
            temp = 0.0
            for j in range(self.num):
                temp += self.W[i][j]*self.u[j]
            du[i] = (self.f(self.a*self.u[i] - self.b*self.v[i] + temp + self.Su[i]) - self.u[i])/self.Tu[i]
        return du

    def dv(self):
        dv = np.zeros((self.num,))
        for i in range(self.num):
            temp = 0.0 
            for j in range(self.num):
                temp += self.W[i][j]*self.v[j]
            dv[i] = (self.f(self.c*self.u[i] - self.d*self.v[i] + temp + self.Sv[i]) - self.v[i])/self.Tv[i]
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

    def set_u(self, u):
        self.u = u
    
    def set_v(self, v):
        self.v = v

    def set_W(self, W):
        self.W = W
