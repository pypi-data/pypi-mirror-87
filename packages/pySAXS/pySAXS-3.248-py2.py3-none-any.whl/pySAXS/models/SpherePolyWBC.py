from pySAXS.models.model import Model
from pySAXS.LS.LSsca import Qlogspace
import numpy
from scipy import signal
import time
from numba import jit



@jit(nopython=True)
def gs(x, A,x0,sigma):
        return A*numpy.exp(-(x - x0)**2 / (2*sigma**2))
    
#@jit(["float64[:](float64[:],float64,float64,float64,float64,float64,float64,float64)"],nopython=True)
@jit(nopython=True)
def goFast(q,p0,p1,p2,p3,p4,p5,p6):
        """
        q array of q (A-1)
        par[0] Mean diameter(nm)
        par[1] Gaussian standard deviation (A)
        par[2] concentration of spheres (cm-3)
        par[3] scattering length density of spheres (cm-2)
        par[4] scattering length density of outside (cm-2)
        par[5] background
        par[6] sigma beam
        """
        
        R = (p0/2)*10 #R is need in A and in radius
        s = (p1/2)*10#s in A and in radius
        n = p2
        rho1 = p3
        rho2 = p4
        t1 = q*R
        t2 = q*s
        prefactor = 1e-48*8.*numpy.pi**2.*n*(rho1-rho2)**2./q**6.
        fcos = ((1+2.*t2**2.)**2.-t1**2.-t2**2.)*numpy.cos(2.*t1)
        fsin = 2.*t1*(1.+2.*t2**2.)*numpy.sin(2.*t1)
        f = 1.+t1**2.+t2**2.-numpy.exp(-2.*t2**2)*(fcos+fsin)
        I=prefactor*f+p5
        
        #Beam shape convolution

        sigma=p6/2.3548
        '''Tc=numpy.zeros(len(q))
        center=(q[-1]-q[0])/2+q[0]
        Beam=self.gs(q[0:50],1,q[25],sigma)
        filtered = signal.convolve(I,Beam, mode='same') / sum(Beam)
        '''
        Tc=numpy.zeros(len(q))
        for i in range(len(q)):
            B=gs(q,1,q[i],sigma)
            Tc[i]=Tc[i]+numpy.sum(B*I)/numpy.sum(B)
        
        return Tc


class SphereOTBackgdBC(Model):
    '''
    Spheres polydisperses distribution semi-Gaussienne analytique
    by DC : 18/06/2009
    '''
    
    
    def fSphereOTBackgdBC(self,q,par):
        #start=time.time()
        i=goFast(q,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]))
        #end = time.time()
        #print("Elapsed  = %s" % (end - start))
        return i
        
        
    
    '''
    parameters definition
    
    Model(2,PolyGauss_ana_DC,Qlogspace(1e-4,1.,500.),
    ([250.,10.,1.5e14,2e11,1e10]),
    ("Mean (A)",
    "Polydispersity ","number density","scattering length density of sphere (cm-2)",
    "scattering length density of medium (cm-2)"),
    ("%f","%f","%1.3e","%1.3e","%1.3e"),
    (True,True,False,False,False)),
    
    
    '''
    def __init__(self):
        Model.__init__(self)
        self.IntensityFunc=self.fSphereOTBackgdBC #function
        self.N=0
        self.q=Qlogspace(1e-2,0.4,500.)      #q range(x scale)
        self.Arg=[25.,1.,1.5e14,2e11,1e10,0,0.01]            #list of parameters
        self.Format=["%f","%f","%1.3e","%1.3e","%1.3e","%f","%f"]      #list of c format
        self.istofit=[True,True,True,False,False,False,False]    #list of boolean for fitting
        self.name="Spheres polydisperses with beam convolution"          #name of the model
        self.category="spheres"
        self.Doc=["Mean Diameter(nm)",\
             "Sigma (nm) ",\
             "concentration of spheres (cm-3)",\
             "scattering length density of sphere (cm-2)",\
             "scattering length density of medium (cm-2)",\
             "background",\
             "beam FWMH"] #list of description for parameters
        self.Description="Spheres polydisperses with beam convolution"  # description of model
        self.Author="OT"       #name of Author
        self.WarningForCalculationTime=False
    

