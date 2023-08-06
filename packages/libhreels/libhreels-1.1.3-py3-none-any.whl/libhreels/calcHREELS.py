#!/usr/bin/env python3
import numpy as np
import json
import sys, re, os
from libhreels.HREELS import myPath
from copy import deepcopy

libDir = os.path.dirname(os.path.realpath(__file__)) 

if not (sys.version.startswith('3.6') or sys.version.startswith('3.8')):
    print('''Make sure the Fortran routines 'myEels2' and 'myBoson' 
    have been complied with the proper f2py3 for the right 
    python version!!''') 
try:
    from libhreels import myEels2 as LambinEELS   # wrapper for myEels2.f90
    from libhreels import myBoson as LambinBoson  # wrapper for myBoson.f90
except:
    print('myEels2 and MyBoson are not available here (Check your version)')			

# Experimental setup as dictionary:
setup = {
    "e0": 4.0,
    "theta": 60.,
    "phia": 0.33,
    "phib": 2.0,
    "temperature": 298.,
    "debug": False
}
# Instrumental function describing elastic peak shape:
instrument = {
    "width": 18.,
    "intensity": 100000.,
    "asym": 0.01,
    "gauss": 0.88
}

	
def importMaterials(string='', path=libDir):
    ''' Returns a dictionary with all phonon parameters for the material provided 
    as string argument. If the string is empty or not matching, a list of all available 
    materials is printed.
    '''
    file = os.path.join(myPath(path),'materials.json')
    with open(file) as json_file:
        materials = json.load(json_file)
        try:
            mat = materials[string]
        except:
            print('No data for material >>{}<< found in {} materials.json!!'.format(string, path))
            print('Available materials:\n{}\n'.format(materials.keys()))
            mat = 'None'
    return mat


def addDrude(wPlasma, gPlasma, material):
    ''' Adds a Drude response and returns a dictionary with all phonon parameters for the material provided 
    as 3rd argument.
    '''
    newMaterial = deepcopy(material)
    try:
        if len(newMaterial['wTO']) > 0:
            newMaterial['wTO'] += [-1*wPlasma]
            newMaterial['gTO'] += [-1*gPlasma]
            newMaterial['wLO'] += [0]
            newMaterial['gLO'] += [0]
            return newMaterial
    except:
        print('Cannot add Drude to material',material)
    return material

################################################################################
################################################################################
class lambin:
    def __init__(self, film, setup=setup, instrument=instrument):
        self.e0 = setup['e0']
        self.theta = setup['theta']
        self.phia = setup['phia']
        self.phib = setup['phib']
        self.temperature = setup['temperature']
        self.debug = setup['debug']
        self.width = instrument['width']
        self.gauss = instrument['gauss']
        self.intensity = instrument['intensity']
        self.asym = instrument['asym']
        self.layers = len(film)          # number of layers
        self.neps = self.layers
        name_size = self.layers
        self.name = []; self.thick=[]; self.listNOsci=[]; self.epsinf =[]; Q = []
        allTO=[]; allgTO=[];  allgLO=[]; nDrude=0
        name2 = []
        for layer in film:
            try:
                a = layer[0]['name']
            except:
                a = 'None'
            self.name.append('{:<10}'.format(a[:10]))        # film name and material
            name2.append(a)
            try:
                a = layer[1]
            except:
                a = 10000.
            self.thick.append(a)
            self.epsinf.append(layer[0]['eps'])
            nTO = 2 * len(layer[0]['wTO'])
            allTO.extend(layer[0]['wTO'])
            allgTO.extend(layer[0]['gTO'])
            allTO.extend(layer[0]['wLO'])
            allgTO.extend(layer[0]['gLO'])
            Q.extend(2*len(layer[0]['wTO'])*[10.])
            self.listNOsci.append(nTO)
        
        if len(allTO)!=sum(self.listNOsci) or len(allgTO)!=sum(self.listNOsci):
            print('Error in materials: ', layer[0])
        self.wOsc = np.array(allTO)
        self.gOsc = np.array(allgTO)
        self.osc = np.array([self.wOsc, np.array(Q), self.gOsc])
        return

    def calcSurfaceLoss(self,x):
        ''' Calculate the surface loss spectrum for the array of x, which needs to be an equidistant array. 
        All parameters are defined in the class __init__() call.'''
        wmin = min(x)
        wmax = max(x)-0.001
        dw = (wmax-wmin)/(len(x)-1)     # assumes that x is an equidistant array
        wn_array_size = len(x)     # size of array for x and epsilon (wn_array, loss_array)
        nper = 1.
        contrl = '{:<10}'.format('None'[:10])   # Can be 'image' to include image charge
        mode = '{:<10}'.format('kurosawa'[:10])           
        wn_array,loss_array = LambinEELS.mod_doeels.doeels(self.e0,self.theta,self.phia,self.phib,
            wmin,wmax,dw,self.layers,self.neps,nper,self.name,
            self.thick,self.epsinf,self.listNOsci,self.osc,contrl,mode,wn_array_size)
        i=0
        for item in wn_array:
            if item > 0: break
            i += 1
        return wn_array[i-1:], loss_array[i-1:]

    def calcHREELS(self,x, normalized=True):
        emin = min(x)
        emax = max(x)-0.001
        norm = 1
        xLoss,loss_array = self.calcSurfaceLoss(x)
        wmin = min(xLoss)
        wmax = max(xLoss)
        xOut,spectrum,n = LambinBoson.doboson3(self.temperature,self.width,self.gauss,self.asym,
            emin,emax,wmin,wmax,loss_array,self.debug,len(loss_array))
        if normalized:
            norm = max(spectrum[:n])
        # return xOut[:n], spectrum[:n]/norm
        return xOut[:len(x)], spectrum[:len(x)]/norm

    def calcEps(self, x):
        epsArray = []
        nOsci = len(self.wOsc)
        for wn in x:
            yn = LambinEELS.mod_doeels.seteps(self.listNOsci,nOsci,self.osc,self.epsinf,wn,self.layers)
            epsArray.append(yn)
        return np.transpose(np.array(epsArray))

####################################################################################
def myMain():
    import matplotlib.pyplot as plt
    oxide = importMaterials('NiO')
    substrate = importMaterials('Ag')
    x = np.linspace(-100.,1000.,1000)
    for d in [4., 20., 50., 200., 10000.]:
        film1 = lambin(film=[[oxide,d],[substrate,1000.]])
        # xs, spectrum = film1.calcSurfaceLoss(x)
        xs, spectrum = film1.calcHREELS(x, normalized=True)
        plt.plot(xs,spectrum, label=d)
    plt.ylabel('HREELS Intensity')
    plt.xlabel('Energy Loss (cm$^{-1}$)')
    plt.show()

if __name__ == '__main__':
	myMain()