# This file is licensed under the CeCILL License
# See LICENSE for details.
"""
author : Olivier Tache
(C) CEA 2015
"""
import sys
from PyQt5 import QtGui, QtCore, uic,QtWidgets
from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import dlgAbsoluteI
from pySAXS.guisaxs import dataset
import pySAXS
from pySAXS.mcsas import MCtools
from time import sleep
import numpy
from matplotlib.pyplot import bar
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from scipy.optimize import curve_fit
from pySAXS.guisaxs.qt import preferences
import weightedstats as ws
from time import *
#from pySAXS.mcsas.test_mcsas import datas


classlist=['MCsas'] #need to be specified

def GaussianFunction(x,p0,p1,p2,p3):
        """
        Gaussian model to fit the peak to get exact zero position
        p0 : height of gaussian
        p1 : sigma
        p2 : center of gaussian
        p3 : background
        """
        #print p0,p1,p2,p3
        sigm0=p1#*0.58870501125773733#((2*log(2))**0.5)/2
        return (p0-p3)*numpy.exp(-((x-p2)**2)/(p1*0.58)**2)+p3
    
def prefit(x,y):
        '''
        try to determine some parameters from the datas
        '''
        center=(x[0]+x[-1])/2
        center=x[y.argmax()]
        FWMH=(x[-1]-x[0])/10
        slope=FWMH/2
        maxi=y.max()
        mini=y.min()
        if len(y)>10:
            m=y[:10].mean()
            HalfValue=(maxi-mini)/2
            if HalfValue<m:
                #decreasing front
                t=maxi
                maxi=mini
                mini=t
            #idx = numpy.argmin(numpy.abs(y - HalfValue))
        Arg=[maxi,FWMH,center,mini]
        return Arg

class MCsas(plugin.pySAXSplugin):
    menu="Data Treatment"
    subMenu="MC SAS"
    subMenuText="Start MC"
    icon="chart-medium.png"
    def execute(self):
        datalist=self.ListOfDatasChecked()
        
        #display the dialog box
        label=self.selectedData
        if self.selectedData is None:
            QtWidgets.QMessageBox.information(self.parent,"pySAXS", "No data are selected", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        #print self.data_dict[label].parameters
        #print label
        
        self.dlg=dlgMCSAS(self.selectedData,self.parent)
        
    

class dlgMCSAS(QtWidgets.QDialog):
    def __init__(self, selectedData,parent):
        self.selectedData=selectedData
        self.parent=parent
        if parent is not None:
            self.printout = parent.printTXT
            self.workingdirectory = parent.workingdirectory
        datas=self.parent.data_dict[self.selectedData]
        q=numpy.array(datas.q)#*10
        QtWidgets.QDialog.__init__(self, parent)
        self.popt=None
        self.A=None
        self.ui = uic.loadUi(pySAXS.UI_PATH+"dlgMCsas.ui", self)
        #print "ici"
        self.ui.labelDataset.setText(str(selectedData))
        
        #-- get preferences
        self.pref=preferences.prefs()
        if parent is not None:
            self.pref=self.parent.pref
            
            if self.pref.fileExist():
                    self.pref.read()
                    self.ui.editNbSpheres.setText(str(self.pref.getSet('NbSpheres',section="mc sas",defaultValue=300)))
                    self.ui.editNbIter.setText(str(self.pref.getSet('NbIter',section="mc sas",defaultValue=5)))
                    self.ui.editHistBin.setText(str(self.pref.getSet('HistBin',section="mc sas",defaultValue=50)))
                    self.ui.editLowLim.setText(str(self.pref.getSet('LowLim',section="mc sas",defaultValue=0.1*4*numpy.pi/numpy.max(q))))
                    self.ui.editHighLim.setText(str(self.pref.getSet('HighLim',section="mc sas",defaultValue=0.1*4*numpy.pi/numpy.min(q))))
                    self.ui.editQmin.setText(str(self.pref.getSet('Qmin',section="mc sas",defaultValue=numpy.min(q))))
                    self.ui.editQmax.setText(str(self.pref.getSet('Qmax',section="mc sas",defaultValue=numpy.max(q))))
                    self.ui.editConvValue.setText(str(self.pref.getSet('ConvValue',section="mc sas",defaultValue=1.0)))
            else:
                    self.pref.save()
            
        
        #QtCore.QObject.connect(self.ui.btnFit, QtCore.SIGNAL("clicked()"), self.OnClickFit)
        #QtCore.QObject.connect(self.ui.btnCompare, QtCore.SIGNAL("clicked()"), self.OnClickCompare)
        self.ui.btnFit.clicked.connect(self.OnClickFit)
        self.ui.btnCompare.clicked.connect(self.OnClickCompare)
        self.ui.pushButton.clicked.connect(self.MagicTest)
        self.hscale='lin'
        self.ui.labelCredits.setText('Small programs for Monte-Carlo fitting of SAXS patterns.\n'+\
                                     'It is released under a Creative Commons CC-BY-SA license. \n'+\
                                     'Please cite as:\n'+\
                                     'Brian R. Pauw, 2012, http://arxiv.org/abs/1210.5304 arXiv:1210.5304.')
        #self.fig2=self.ui.matplotlibwidget.figure
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton*)"), self.click)#connect buttons signal
        #print "ici3"
        self.ui.buttonBox.clicked.connect(self.click)
        self.ui.navi_toolbar = NavigationToolbar(self.ui.matplotlibwidget, self)
        self.ui.verticalLayout_2.insertWidget(0,self.ui.navi_toolbar)
        self.ui.btnTry.clicked.connect(self.startMC)
        self.ui.btnInit.clicked.connect(self.OnClickInit)
        
        self.ui.show()
        
    def click(self,obj=None):
        name=obj.text()
        print(name)
        if name.find('Close')>=0:
            self.savePrefs()
            self.close()
        elif name.find('OK')>=0:
          
            self.startMC()
        elif name.find('Save')>=0:
            self.Export()
    
    def savePrefs(self):
        if self.parent is not None:
                #self.parent.pref.set("outputdir",section="pyFAI",value=str(self.ui.outputDirTxt.text()))
                self.pref.set("NbSpheres",section="mc sas",value=str(self.ui.editNbSpheres.text()))
                self.pref.set("NbIter",section="mc sas",value=str(self.ui.editNbIter.text()))
                self.pref.set("HistBin",section="mc sas",value=str(self.ui.editHistBin.text()))
                self.pref.set("LowLim",section="mc sas",value=str(self.ui.editLowLim.text()))
                self.pref.set("HighLim",section="mc sas",value=str(self.ui.editHighLim.text()))
                self.pref.set("Qmin",section="mc sas",value=str(self.ui.editQmin.text()))
                self.pref.set("Qmax",section="mc sas",value=str(self.ui.editQmax.text()))
                self.pref.set("ConvValue",section="mc sas",value=str(self.ui.editConvValue.text()))
                self.pref.save()
    
    def OnClickInit(self):
        datas=self.parent.data_dict[self.selectedData]
        q=numpy.array(datas.q)
        self.ui.editNbSpheres.setText(str(300))
        self.ui.editNbIter.setText(str(5))
        self.ui.editHistBin.setText(str(50))
        self.ui.editLowLim.setText("%6.2f"%(0.1*2*numpy.pi/numpy.max(q)))
        self.ui.editHighLim.setText("%6.2f"%(0.1*2*numpy.pi/numpy.min(q)))
        #print "ici2"
        self.ui.editQmin.setText("%6.4f"%numpy.min(q))
        self.ui.editQmax.setText("%6.4f"%numpy.max(q))
        self.ui.editConvValue.setText(str(1.0))
        
            
    def updateConval(self,nr):
        #print("update %6.2f"%nr)
        self.ui.lblConValue.setText('%6.2f'%nr)
        self.ui.lblConValue.repaint()
        
    def MagicTest(self):
        self.updateConval(time())
    
    def startMC(self):
        self.savePrefs()
        datas=self.parent.data_dict[self.selectedData]
        qmin=float(self.ui.editQmin.text())
        qmax=float(self.ui.editQmax.text())
        #print((qmin, qmax))
        q=numpy.array(datas.q)
        
        nQmin=numpy.where((q>=qmin))[0][0]
        nQmax=numpy.where((q<=qmax))[0][-1]
        q=q[nQmin:nQmax]*10
        #q=numpy.array(datas.q)*10
        I=numpy.array(datas.i)[nQmin:nQmax]
        E=numpy.array(datas.error)[nQmin:nQmax]
        #print E
        q=q[numpy.nonzero(I)]
        itemp=I[numpy.nonzero(I)]
        #print((numpy.nonzero(I)))
        #print((len(E)))
        #print((len(I)))
        E=E[numpy.nonzero(I)]
        I=itemp
        '''self.plt2=self.fig2.add_subplot(111) 
        self.plt2.plot(q,I)
        #self.axes.hold(True)
        
        self.ui.matplotlibwidget.draw()'''


        NbSph=int(self.ui.editNbSpheres.text())
        NbReps=int(self.ui.editNbIter.text())
        H=int(self.ui.editHistBin.text())
        Smin=float(self.ui.editLowLim.text())/2
        Smax=float(self.ui.editHighLim.text())/2
        if self.ui.checkBox.isChecked():
            self.hscale='log'
        else:
            self.hscale='lin'
        '''self.ui.progressBar.setMaximum(NbReps)
        self.ui.progressBar.setValue(0)'''
        Convcrit=float(self.ui.editConvValue.text())
        #try:
        test,self.A=MCtools.Analyze_1D(q,I,numpy.maximum(0.01*I,E),Nsph=NbSph,Convcrit=Convcrit,\
                             Bounds=numpy.array([Smin,Smax]),\
                             Rpfactor=1.5/3,Maxiter=1e4,Histscale=self.hscale,drhosqr=1,Nreps=NbReps,Histbins=H,\
                             ConvValueDisplay=self.updateConval)#feedback=self.updateUI,endf=self.plotBar)
        #except:
        #QtWidgets.QMessageBox.information(self,"pySAXS", "MC SAS could not reach optimization ", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
        '''self.c.verbose=False
        self.c.start()'''
        if not test :
            QtWidgets.QMessageBox.information(self,"pySAXS", "MC SAS could not reach optimization criterion but convergence value found=%6.2f"%self.A, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
                                              #if self.A is None:
                                              #    QtWidgets.QMessageBox.information(self,"pySAXS", "MC SAS could not reach optimization criterion", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
        else:
            self.plotBar()
            self.reDraw()
            #self.ui.btnExport.setEnabled(True)
    

    def reDraw(self):
        self.plt.grid()
        self.fig.tight_layout()
        self.ui.matplotlibwidget.draw()

    def plotBar(self):    
        
        A=self.A
    
        q=A['q']/10
        i=A['Imean']
        #print q
        error=A['Istd']
        name=self.selectedData+ " mc fit"
        self.parent.data_dict[name]=dataset.dataset(name,q,i, name,parent=[self.selectedData],error=error,type='mc_fit',color='darkviolet')
        self.parent.redrawTheList()
        self.parent.Replot()        
        
        s=A['Hx'][0:-1]*2 #diameter
        V=A['Hmean']/sum(A['Hmean'])
        #Volume from radius
        VR=(4/3.)*numpy.pi*(s/2)**3  #DIAMETER
        n=V/VR  #number=Vtotal/V per sphere
        #print n
        #print sum(n)
        
        mean=ws.numpy_weighted_mean(s, weights=V)
        median=ws.numpy_weighted_median(s, weights=V)
        maxi=s[numpy.argmax(V)]
        #plt.bar(r, n,label="data",color='c' )
        
        '''print('max %6.2f'%maxi)
        print('mean %6.2f'%mean)
        print('median %6.2f'%median)'''
        average = numpy.average(s, weights=V)
        variance = numpy.sqrt(numpy.average((s-average)**2, weights=V))
        #print("AVG = %6.2f   VARIANCE =%6.2f"%(average,variance))
        
        
        
        
        self.fig=self.ui.matplotlibwidget.figure
        self.fig.clear() 
        self.plt=self.fig.add_subplot(211)
        self.plt.set_title('Particule size distribution')
        w=A['Hwidth']*2
        #print((w, len(s)))
        self.plt.bar(s-w/2,V,\
                     yerr=A['Hstd']/sum(A['Hmean']),width=A['Hwidth']*2,\
                     color='orange',edgecolor='b',linewidth=1,ecolor='blue',capsize=5,alpha=0.8) #
        self.plt.axvline(maxi,color='r',label='mode(max)=%6.2f'%maxi)
        self.plt.axvline(mean,color='g',label='mean= %6.2f'%mean)
        self.plt.axvline(median,color='y',label='median= %6.2f'%median)
        self.plt.axvline(mean-variance,color='k',linestyle='--',linewidth=1.0,label='variance= %6.2f'%variance)
        self.plt.axvline(mean+variance,color='k',linestyle='--',linewidth=1.0)
        
        self.plt.set_xlabel("diameter (nm)")
        self.plt.set_ylabel('Volume-weighted')
        self.plt.legend()
        self.plt.set_ylim(bottom=0.0)
        if self.ui.checkBox.isChecked():
            self.plt.set_xscale('log')
        
        self.plt2=self.fig.add_subplot(212) 
        self.plt2.bar(s-w/2,n,width=A['Hwidth']*2,color='c',edgecolor='black',\
                      linewidth=1,zorder=2,ecolor='blue',capsize=5)
        self.plt2.set_xlabel("diameter (nm)")
        self.plt2.set_ylabel('number')
        if self.ui.checkBox.isChecked():
            self.plt2.set_xscale('log')
        self.plt2.grid()
        #self.reDraw()
        
     
        #self.ui.matplotlibwidget.draw()
    
    
    
    def OnClickFit(self):
        if self.A is None:
            return
        X1=numpy.array(self.A['Hx'][0:-1])*2
        Y1=numpy.array(self.A['Hmean'])
        #print X1,Y1
        res1=prefit(X1,Y1)    
        #print(("Prefit result : ",res1))
        popt, pcov = curve_fit(GaussianFunction, X1, Y1,p0=res1)
        self.popt=popt
        #plt.plot(X2,Y2, 'b-')
        #plt.grid()
        #print(("Best diameter :",popt[2], "nm  Sigma : ",popt[1]))
        self.plotBar()
        X2=numpy.arange(X1[0],X1[-1],(X1[-1]-X1[0])/200)
        Y2=GaussianFunction(X2, popt[0], popt[1],popt[2],popt[3])
        self.plt.plot(X2,Y2/sum(Y1), 'r-',label='MC SAS r ='+"{:.2f}".format(popt[2])+ "nm  S="+"{:.2f}".format(popt[1]))
        #self.plt.legend(fontsize='x-small')
        self.plt.grid()
        self.ui.editCompMax.setText(str(popt[0]))
        self.ui.editCompR.setText(str(popt[2]))
        self.ui.editCompS.setText(str(popt[1]))
        self.reDraw()
        
    def OnClickCompare(self):
        CompM=float(self.ui.editCompMax.text())
        CompR=float(self.ui.editCompR.text())
        CompS=float(self.ui.editCompS.text())
        if self.A is None:
            return
        X1=numpy.array(self.A['Hx'][0:-1])*2
        Y1=numpy.array(self.A['Hmean'])
        self.plotBar()
        X2=numpy.arange(X1[0],X1[-1],(X1[-1]-X1[0])/200)
        if self.popt is not None:
            Y2=GaussianFunction(X2, self.popt[0], self.popt[1],self.popt[2],self.popt[3])
            self.plt.plot(X2,Y2/sum(Y1), 'r-',label='MC SAS r ='+"{:.2f}".format(self.popt[2])+ "nm  S="+"{:.2f}".format(self.popt[1]))
        Y3=GaussianFunction(X2,CompM, CompS, CompR,0.0)
        self.plt.plot(X2,Y3, 'g-',label='pySAXS r ='+"{:.2f}".format(CompR)+ "nm  S="+"{:.2f}".format(CompS))
        self.plt.grid()
        self.plt.legend(fontsize='x-small')
        self.reDraw()
    
    def Export(self):
        '''
        export datas
        '''
        if self.A is None:
            return
        #ask for a file
        fd = QtWidgets.QFileDialog(self)
        #get the filenames, and the filter
        wc = "txt file (*.txt)"
        filename,filter=fd.getSaveFileName(filter=wc,directory=self.workingdirectory)#[0]
        filename=str(filename)
        print(("filename:",filename))
        #self.setWorkingDirectory(filename) #set working dir
        if  filename!="":
            #check if file exist already
            #export datas
            A=self.A
            #print "export"
            w=A['Hwidth']
            #x=A['Hx'][0:-1]-w/2
            y=A['Hmean']/numpy.sum(A['Hmean'])
            s=(A['Hx'][0:-1]-w/2)*2 #diameter nm
            V=A['Hmean']/sum(A['Hmean'])
            '''r=(V*3/4.)**(1./3)    #radius from V
            n=r/s  #number
            V=A['Hmean']/sum(A['Hmean'])
            #Volume from radius
            VR=(4/3.)*numpy.pi*s**3 
            n=V/VR  #number=Vtotal/V per sphere
            '''
            #Volume from radius
            VR=(4/3.)*numpy.pi*(s/2)**3  #DIAMETER
            n=V/VR  #number=Vtotal/V per sphere
            #print "export"
            yerr=A['Hstd']/numpy.sum(A['Hmean'])
            #print "export"
            
            data=numpy.array([numpy.array(s),numpy.array(y),numpy.array(yerr),numpy.array(n)]).transpose()
            #print "data", data
            try:
                NbSph=int(self.ui.editNbSpheres.text())
                NbReps=int(self.ui.editNbIter.text())
                H=int(self.ui.editHistBin.text())
                Smin=float(self.ui.editLowLim.text())
                Smax=float(self.ui.editHighLim.text())
                Convcrit=float(self.ui.editConvValue.text())
                qmin=float(self.ui.editQmin.text())
                qmax=float(self.ui.editQmax.text())
                header="MC SAS histogram integrated on pySAXS\n"
                header+="Qmin :"+str(qmin)+"\tQmax:"+str(qmax)+"\tSmin :"+str(Smin)+"\tSmax:"+str(Smax)+"\tNb spheres:"+str(NbSph)+"\tNb iters:"+str(NbReps)+"\n"
                numpy.savetxt(filename, data,header=header+"diameter (nm)\tVolume-weighted\tvolume error\tNumber")#, fmt, delimiter, newline, header, footer, comments)
                print("save successfull")
            except:
                print(("Unexpected error for :"+filename, sys.exc_info()[0]))            
                               
        return

