from pySAXS.models.model import Model
from pySAXS.LS.LSsca import Qlogspace
import numpy
from scipy import signal

class SphereOTDoubleLogNormalInverse(Model):
    '''
    Spheres polydisperses distribution log normal inverse
    with beam convolution
    by OT : 23/03/2020
    '''
    
    def LOGNORMa_ix2(self,R,Rm,Rm2,sigma,sigma2,A=1,A2=1):
        Ri=(Rm-R)+Rm
        F1=1/(Ri*sigma*numpy.sqrt(2*numpy.pi))
        F2=-(log(Ri/Rm)/(sigma*numpy.sqrt(2)))**2
        L1=(A*nan_to_num(F1*numpy.exp(F2)))
        Ri2=(Rm2-R)+Rm2
        F12=1/(Ri*sigma2*numpy.sqrt(2*numpy.pi))
        F22=-(log(Ri2/Rm2)/(sigma2*numpy.sqrt(2)))**2
        L2=(A2*nan_to_num(F12*numpy.exp(F22)))
        return L1+L2
    
    def MonoSphereFunction(self,q,par):
        """
        q array of q (A-1)
        par[0] radius of the sphere (nm)
        par[1] scattering length density of sphere (cm-2)
        par[2] scattering length density of outside (cm-2)
        par[3] concentration of sphere (cm-3)
        """
        par[0]=(par[0]/2)*10 #nm conversion
        return par[3]*(par[1]-par[2])**2.*getV(par[0])*getV(par[0])*1e-48*P1(q,par[0])
        
    
    def fSphereOTBackgdBC(self,q,par):
        """
        q array of q (A-1)
        par[0] Mean diameter(nm)
        par[0] Mean diameter 2(nm)
        par[1] sigma 1(nm)
        par[1] sigma 2(nm)
        par[2] concentration of spheres (cm-3)
        par[3] scattering length density of spheres (cm-2)
        par[4] scattering length density of outside (cm-2)
        par[5] background
        par[6] sigma beam
        """
        R = (par[0]/2)*10 #R is need in A and in radius
        s = (par[1]/2)*10#s in A and in radius
        n = par[2]
        rho1 = par[3]
        rho2 = par[4]
        t1 = q*R
        t2 = q*s
        prefactor = 1e-48*8.*numpy.pi**2.*n*(rho1-rho2)**2./q**6.
        fcos = ((1+2.*t2**2.)**2.-t1**2.-t2**2.)*numpy.cos(2.*t1)
        fsin = 2.*t1*(1.+2.*t2**2.)*numpy.sin(2.*t1)
        f = 1.+t1**2.+t2**2.-numpy.exp(-2.*t2**2)*(fcos+fsin)
        I=prefactor*f+par[5]
        
        #Beam shape convolution

        sigma=par[6]/2.3548
        '''Tc=numpy.zeros(len(q))
        center=(q[-1]-q[0])/2+q[0]
        Beam=self.gs(q[0:50],1,q[25],sigma)
        filtered = signal.convolve(I,Beam, mode='same') / sum(Beam)
        '''
        Tc=numpy.zeros(len(q))
        for i in range(len(q)):
            B=self.gs(q,1,q[i],sigma)
            Tc[i]=Tc[i]+numpy.sum(B*I)/numpy.sum(B)
        
        return Tc
    
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
    

