import numpy as np
from tqdm import tqdm 
from cpg-wilson-cowan import osc

class QuadCPG(object):
    def __init__(self, alpha_k, alpha_h, base_cpg, A_k, A_h):
        self.alpha_k = alpha_k
        self.alpha_h = alpha_h
        self.A_k
        self.base_cpg = base_cpg
        self.u_h = np.random.random((self.base_cpg.num,))
        self.v_h = np.random.random((self.base_cpg.num,))
        self.base_cpg.set_u(self.u_h)
        self.base_cpg.set_v(self.v_h)
        self.y_h = self.base_cpg.p*(self.u_h - self.v_h)
        self.y_k = np.random.random((self.base_cpg.num,))
        self.y_h_dot = np.random.random((self.base_cpg.num,))
        self.Arr_y_h = np.zeros((self.base_cpg.n, self.base_cpg.num))
        self.Arr_y_k = np.zeros((self.base_cpg.n, self.base_cpg.num))      
            
    def get_y_h_dot(self):
        return self.base_cpg.p*(self.base_cpg.du()-self.base_cpg.dv())

    def simulate(self):
        for i in range(self.base_cpg.n):
            self.Arr_y_h[i, :] = self.y_h
            self.Arr_y_k[i, :] = self.y_k
            self.y_h_dot = self.get_y_h_dot()
            if y_h_dot < 0:
                self.y_k = 0.0
            else:
                self.y_k = self.alpha_k*self.A_k*(1-(self.y_h/(self.alpha_h*self.A_h))**2))
            self.u_h = self.base_cpg.get_u()
            self.base_cpg.set_u(self.u_h)
            self.v_h = self.base_cpg.get_v()
            self.base_cpg.set_v(self.v_h)
            self.y_h = self.base_cpg.p*(self.u_h - self.v_h)
            
