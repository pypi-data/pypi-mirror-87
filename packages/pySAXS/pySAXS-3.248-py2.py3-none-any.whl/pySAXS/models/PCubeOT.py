from pySAXS.models.model import Model
from pySAXS.LS.LSsca import *
import numpy
import time

class CubeOT(Model):
    '''
    Cubes and parallelepiped
    by OS : 03/11/2011
    '''
    
    def PCube(self,q,par):
        """
        q array of q (A-1)
        par[0] side length 1 (in 1/q)
        par[1] SLD particle (cm-2)
        par[2] SLD medium (cm-2)
        par[3] number density (cm-3)
        """        
        a = par[0]
        rho1 = par[1]
        rho2 = par[2]
        n=par[3]

        prefactor = 1e-48*n*(rho1-rho2)**2

        f = a**6*Ppara(q,a,a,a)
        
    def gs(self,x,A,x0,sigma):
        return A*exp(-(x - x0)**2 / (2*sigma**2))
    
    def MC2(self,q,par):
        start=time.time()
        a = par[0]
        rho1 = par[1]
        rho2 = par[2]
        n=par[3]
        #sca=par[4]
        backgd=par[4]
        beamsize=par[5]
        prefactor = 1e-48*n*(rho1-rho2)**2

        P = prefactor*a**6*Ppara(q,a,a,a)+backgd
        #P=LSsca.Ppara(q,a,a,a)*sca+backgd
        if beamsize==0:
            return P
        #beamsize=0.003
        sigma=beamsize/2.3548
        
        I=P
        Tc=numpy.zeros(len(q))
        for i in range(len(q)):
            B=self.gs(q,1,q[i],sigma)
            Tc[i]=Tc[i]+numpy.sum(B*I)/numpy.sum(B)
        print(time.time()-start)
        return Tc   
        
        
        
        return prefactor*f
    def __init__(self):
        Model.__init__(self)
        self.IntensityFunc=self.MC2 #function
        self.N=0
        self.q=Qlogspace(3e-4,1.,100.)                             #q range(x scale)
        self.Arg=[550.,1.31440e+12,9.8e10,1e10,0.001,0.001]                         #list of parameters
        self.Format=["%f","%1.3e","%1.3e","%1.3e","%6.2f","%6.2f"]      #list of c format
        self.istofit=[True,False,False,False,False,False]           #list of boolean for fitting
        self.name="Cubes PSD"                      #name of the model
        self.category="parallelepiped"
        self.Doc=["side length 1 ",\
             "scattering length density of particle (cm-2)",\
             "scattering length density of medium (cm-2)",\
             "Number density (cm-3)",
             "background",
             "beamsize convolution"]           #list of description for parameters
        self.Description="Cubes OT"  # description of model
        self.Author="Olivier Spalla & Olivier Tache"                 #name of Author
        self.WarningForCalculationTime=True
    
