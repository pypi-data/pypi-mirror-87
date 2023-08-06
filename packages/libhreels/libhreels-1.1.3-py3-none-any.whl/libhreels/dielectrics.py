# Testing dielectric models and their surface loss function
import matplotlib.pyplot as plt
import numpy as np
from numpy import real, imag, sqrt
#from scipy.constants import physical_constants

# Thz = 100*physical_constants['speed of light in vacuum'][0] # conversion from cm^-1 to Hz 

def doping2plasmaFrequency(doping,epsInfinity=1.):
    '''Returns the bulk plasma frequency in cm-1 for a doping 
       given by the argument in cm-3.
       Check if eps_Infinity handling is correct.'''
    return np.sqrt(doping)*1.8817885780819758e-06/np.sqrt(epsInfinity)

def doping2surfacePlasma(doping,epsInfinity=1.):
    '''Returns the surface plasma frequency in cm-1 for a doping 
       given by the argument in cm-3'''
    return np.sqrt(doping)*1.8817885780819758e-06/np.sqrt(1+epsInfinity)

def loss(eps):
    return np.imag(1/eps)

def surfaceLoss(eps):
    return np.imag(1/(1+eps))

def reflectivity(eps):  # IR reflectivity
    sq = np.sqrt(eps)
    a =np.abs((sq-1)/(sq+1))
    return a*a

def sigma(eps,w,eps_Infinity=1):       # Complex conductivity 
    return np.imag((eps-eps_Infinity)*w)

def plotDielectrics(x,eps):
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(6,6))
    axs[0].plot(x, -np.imag(eps), label='-Im $\epsilon (\omega )$')
    axs[0].plot(x, np.real(eps), label='Re $\epsilon (\omega )$')    
    axs[0].legend()
    axs[0].set_ylabel('Dielectric Function')

    axs[1].plot(x, surfaceLoss(eps), linestyle='-')    
    axs[1].set_ylabel('Surface Loss Function')
    axs[1].set_ylim([0,None])

    axs[2].plot(x, reflectivity(eps))
    axs[2].set_ylabel('Reflectivity')
    axs[2].set_xlabel('Frequency')
    axs[2].set_ylim([0,1])
    axs[0].set_xlim(left=0, right=max(x))

    plt.show()
class oscillator:
    def __init__(self, wTO, wLO, gammaTO=20, gammaLO=20):
        self.wTO = wTO
        self.wLO = wLO
        self.gammaTO = gammaTO
        self.gammaLO = gammaLO

    def eps(self,w):
        nom = self.wLO*self.wLO - w*w + 1j*self.gammaLO*w
        denom = self.wTO*self.wTO - w*w + 1j*self.gammaTO*w
        return nom/denom

    def __call__(self, w):
        return self.eps(w)

class simpleOsci(oscillator):
    def __init__(self, wTO, Q, gammaTO=20):
        self.wTO = wTO
        self.Q = Q
        self.gammaTO = gammaTO

    def eps(self,w):
        nom = self.wTO*self.wTO*self.Q
        denom = self.wTO*self.wTO - w*w + 1j*self.gammaTO*w
        return nom/denom

class drude:
    def __init__(self, wPL, gamma):
        self.wPL = wPL
        self.gamma = gamma

    def eps(self,w):
        return 1. - (self.wPL*self.wPL)/(w*w - 1j*self.gamma*w)

    def __call__(self, w):
        return self.eps(w)

class drude2:
    '''This defines an additive Drude component to a dielectric function: 
    eps_drude = drude2(omega_p, gamma_p, gamma_0)
    ... eps(omega) + eps_drude(omega)
    '''
    def __init__(self, omega_p, gamma_p, gamma_0):
        self.omega_p = omega_p
        self.gamma_p = gamma_p
        self.gamma_0 = gamma_0

    def eps(self,w):
        newW = np.where(w==0, 0.000567894, w)   # Avoid zeros to avoid devision by zero 
        w = newW
        return -((self.omega_p**2 + 1j*(self.gamma_p-self.gamma_0)*w)/(w*(w - 1j *self.gamma_0)))

    def __call__(self, w):
        return self.eps(w)

def myMain():
    # BaTiO3
    data = [
        [178.6, 8.02, 3.09800E-02],
        [270.6, 24.00, 10.0800E-02],
        [522.9, 1.20, 6.97200E-02]]
    # Width (3rd parameter) is given in fraction of TO frequency

    oscis = [simpleOsci(TO, Q, f*TO) for (TO, Q, f) in data]
        
    x = np.linspace(0,1000,num=1200)
    epsInfinity = 5.25
    eps = epsInfinity
    for each in oscis:
        eps += each(x)

    plotDielectrics(x, eps)

if __name__ == '__main__':
	myMain()
