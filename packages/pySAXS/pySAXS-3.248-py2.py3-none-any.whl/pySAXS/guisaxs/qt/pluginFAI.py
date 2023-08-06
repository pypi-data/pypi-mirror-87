from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import dlgQtFAI
from pySAXS.guisaxs.qt import dlgQtFAITest
from pySAXS.guisaxs.qt import dlgSurveyor
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import os
listofPotentialDirectories=[os.path.dirname(sys.executable),\
                            os.path.dirname(sys.executable)+os.sep+'bin',\
                            os.path.dirname(sys.executable)+os.sep+'scripts']
#from pySAXS.guisaxs.qt import startpyFAICalib

classlist=['pluginSurveyorXeuss','pluginTestFAI','pluginCalibStart','pluginDrawMaskStart']#,'pluginFAI',]

class pluginFAI(plugin.pySAXSplugin):
    menu="Data Treatment"
    subMenu="Image"
    subMenuText="Fast Radial Averaging"
    icon="image.png"
    toolbar=True
    
    def execute(self):
        #get the preferences
        parameterfile=self.parent.pref.get("parameterfile",'pyFAI')
        ouputdir=self.parent.pref.get('outputdir','pyFAI')
        #display the FAI dialog box
        self.dlgFAI=dlgQtFAI.FAIDialog(self.parent,parameterfile,ouputdir)
        self.dlgFAI.show()


class pluginTestFAI(plugin.pySAXSplugin):
    menu="Data Treatment"
    subMenu="Image"
    subMenuText="Radial Averaging parameters"
    icon="settings.png"
    
        
    def execute(self):
        parameterfile=self.parent.pref.get("parameterfile",'pyFAI')
        ouputdir=self.parent.pref.get('outputdir','pyFAI')
        #display the FAI dialog box
        self.dlgFAI=dlgQtFAITest.FAIDialogTest(self.parent,parameterfile,ouputdir)
        self.dlgFAI.show()
        
class pluginCalibStart(plugin.pySAXSplugin):
    menu="Data Treatment"
    subMenu="Image"
    subMenuText="Calibration tools"
    #icon="image.png"
    icon="calibre.png"
    """
    Calib Start program
    """
        
    def execute(self):
        cmd='pyFAI-calib2'
        found=False
        #search executable
        for d in listofPotentialDirectories:
            executableName=d+os.sep+cmd
            if os.name=='nt':
                executableName+=".exe"
            #print(executableName)
            if os.path.exists(executableName):
                found=True
                break
        if not found:
            QtWidgets.QMessageBox.critical(self.parent,'pySAXS error',"Could not find pyFAI-calib executable...")
            return
        parameterfile=self.parent.pref.get("parameterfile",'pyFAI')
        #print(parameterfile)
        os.chdir(os.path.dirname(parameterfile))
        ret = subprocess.call(executableName)

class pluginDrawMaskStart(plugin.pySAXSplugin):
    menu = "Data Treatment"
    subMenu = "Image"
    subMenuText = "Draw masks"
    # icon="image.png"
    icon = "carnival-mask-silhouette.png"
    """
    Calib Start program
    """

    def execute(self):
        cmd='pyFAI-drawmask'
        found = False
        # search executable
        for d in listofPotentialDirectories:
            executableName = d + os.sep + cmd
            if os.name == 'nt':
                executableName += ".exe"
            # print(executableName)
            if os.path.exists(executableName):
                found = True
                break
        if not found:
            QtWidgets.QMessageBox.critical(self.parent, 'pySAXS error', "Could not find pyFAI-calib executable...")
            return
        parameterfile=self.parent.pref.get("parameterfile",'pyFAI')
        #print(parameterfile)
        os.chdir(os.path.dirname(parameterfile))
        fd = QtWidgets.QFileDialog(self.parent)
        filename = fd.getOpenFileName(directory=os.path.dirname(parameterfile))[0]
        ret = subprocess.call(executableName+' '+filename)



    
class pluginSurveyorXeuss(plugin.pySAXSplugin):
    menu="Data Treatment"
    subMenu="Image"
    subMenuText="SAXS Image Surveyor"
    icon="eye.png"
    toolbar=True
        
    def execute(self):
        #display the FAI dialog box
        parameterfile=self.parent.pref.get("parameterfile",'pyFAI')
        #print "XEUSS"
        self.dlg=dlgSurveyor.SurveyorDialog(self.parent,parameterfile)
        self.dlg.show()
        