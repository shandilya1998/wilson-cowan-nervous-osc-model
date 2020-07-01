import numpy as np
from tqdm import tqdm 
from cpg_wilson_cowan import osc
import matplotlib.pyplot as plt

class QuadCPG(object):
    def __init__(self, alpha_k, alpha_h, base_cpg, A_k, A_h):
        self.alpha_k = alpha_k
        self.alpha_h = alpha_h
        self.A_k = A_k
        self.A_h = A_h 
        self.base_cpg = base_cpg
        self.u_h = np.random.random((self.base_cpg.num,))
        self.v_h = np.random.random((self.base_cpg.num,))
        self.base_cpg.set_u(self.u_h)
        self.base_cpg.set_v(self.v_h)
        self.y_h = self.base_cpg.p*(self.u_h - self.v_h)
        self.y_k = np.zeros((self.base_cpg.num,))
        self.y_h_dot = np.random.random((self.base_cpg.num,))
        self.Arr_y_h = np.zeros((self.base_cpg.n, self.base_cpg.num))
        self.Arr_y_k = np.zeros((self.base_cpg.n, self.base_cpg.num))      
            
    def get_y_h_dot(self):
        return self.base_cpg.p*(self.base_cpg.du()-self.base_cpg.dv())

    def simulate(self):
        for i in tqdm(range(self.base_cpg.n)):
            self.Arr_y_h[i, :] = self.y_h
            self.Arr_y_k[i, :] = self.y_k
            self.y_h_dot = self.get_y_h_dot()
            for j in range(self.base_cpg.num):
                if self.y_h_dot[j] < 0:
                    self.y_k[j] = 0.0 #*self.alpha_k*self.A_k*(-(self.y_h[j]/(self.alpha_h*self.A_h))**2)
                else:
                    self.y_k[j] = self.alpha_k*self.A_k*(1-(self.y_h[j]/(self.alpha_h*self.A_h))**2)
            self.u_h = self.base_cpg.get_u()
            self.v_h = self.base_cpg.get_v()
            if i == self.base_cpg.n -25000:
                self.u_h = np.random.random((self.base_cpg.num,))
                self.v_h = np.random.random((self.base_cpg.num,))
            self.base_cpg.set_u(self.u_h)
            self.base_cpg.set_v(self.v_h)
            self.y_h = self.base_cpg.p*(self.u_h - self.v_h)
        
    def plot(self):
        labels = []
        fig, axes = plt.subplots(4, 1,  figsize=(5, 20))
        for i in range(self.base_cpg.num):
            axes[i].plot(self.base_cpg.t[-50000:], self.Arr_y_h[-50000:, i])
            axes[i].plot(self.base_cpg.t[-50000:], self.Arr_y_k[-50000:, i])
        plt.show()
        fig.savefig('plots/cpg_quad_exp2.png')

cpg = QuadCPG(alpha_k = 1, alpha_h = 0.75, base_cpg = osc, A_h = 1, A_k = 0.91)
cpg.simulate()
cpg.plot()
