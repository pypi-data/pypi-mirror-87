from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5 import QtTest
import pySAXS
import sys
from jinja2 import Template

def my_excepthook(type, value, tback):
    # log the exception here
    #print value
    #print tback
    # then call the default handler
    sys.__excepthook__(type, value, tback)

sys.excepthook = my_excepthook

class sampleHolderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, parameterfile=None, outputdir=None):
        QtWidgets.QWidget.__init__(self, parent)
        
        self.ui = uic.loadUi(pySAXS.UI_PATH+"sampleholder.ui", self)#
        
        self.workingdirectory="S:\\DEV\\sampleH"#pySAXS.UI_PATH
        
        self.setWindowTitle('Sample Holder application')
        self.ui.btnOpen.clicked.connect(self.OnClick_btnOpen)
        self.ui.btnOpen_template.clicked.connect(self.OnClick_btnOpen_template)
        self.ui.btnGenerate.clicked.connect(self.OnClick_btnGenerate)
        self.ui.btnAPlus.clicked.connect(self.OnClick_btnAPlus)
        self.ui.btnAMinus.clicked.connect(self.OnClick_btnAMinus)
        self.ui.btnASuppr.clicked.connect(self.OnClick_btnASuppr)
        self.ui.btnAInsert.clicked.connect(self.OnClick_btnAInsert)
        self.ui.btnACopy.clicked.connect(self.OnClick_btnACopy)
        self.ui.btnSave.clicked.connect(self.OnClick_btnSave)
        self.ui.btnSaveMacro.clicked.connect(self.OnClick_btnSaveMacro)
        self.ui.btnSaveTemplate.clicked.connect(self.OnClick_btnSaveTemplate)
        self.ui.btnSetTime.clicked.connect(self.OnClick_btnSetTime)
        
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setRowCount(10)
        headerNames = ["Name", "Sample", "x", "z","time"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headerNames)
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 50)
        self.ui.tableWidget.setColumnWidth(2, 50)
        self.ui.tableWidget.setColumnWidth(3, 50)
        self.ui.tableWidget.setColumnWidth(4, 50)
        self.templateStr=None


    def OnClick_btnOpen(self):
        fd = QtWidgets.QFileDialog(self)
        fn=self.ui.edtFileName.text()
        if fn=="":
            fn=self.workingdirectory
        else:
            self.workingdirectory=fn
        filename = fd.getOpenFileName(directory=self.workingdirectory)[0]
        #print(filename)
        self.ui.edtFileName.setText(str(filename))
        if filename != "":
            self.readSampleHolderFile(filename)
            self.ui.tableWidget.setRowCount(len(self.samples))
            
            for i in range(len(self.samples)):
                s=self.samples[i]
                self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(s[0].rstrip()))
                self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(s[1].rstrip()))
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(s[2].rstrip()))
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(s[3].rstrip()))
                self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(s[4].rstrip()))
                self.ui.tableWidget.setRowHeight(i, 20)
    
    def OnClick_btnOpen_template(self):
        fd = QtWidgets.QFileDialog(self)
        fn=self.ui.edtFileName_template.text()
        if fn=="":
            fn=self.workingdirectory
        else:
            self.workingdirectory=fn
        filename = fd.getOpenFileName(directory=self.workingdirectory)[0]
        #print(filename)
        self.ui.edtFileName_template.setText(str(filename))
        f=open(filename)
        self.templateStr=f.read()
        print(self.templateStr)
        self.ui.textEdit.setText(self.templateStr)
    
    def OnClick_btnGenerate(self):
        self.table2sample()
        txt=str(self.ui.textEdit.toPlainText())
        if txt is not None:
            self.templateStr=txt
        if self.templateStr is not None:
            template = Template(self.templateStr)
            r=template.render(sample=self.samples,user=str(self.ui.edtUserName.text()),directory=str(self.ui.edtDirectory.text()))
            #print(template.vars)
            self.ui.edtCode.setText(r)
    
    def OnClick_btnAPlus(self):
        '''
        swap two rows
        '''
        selectedItem=self.ui.tableWidget.selectedIndexes()[0]
        r=selectedItem.row()
        #print(r)
        if r<1:
            return
        temp=[]
        for i in range(5):
            tempItem=self.ui.tableWidget.item(r-1,i).text()
            item=self.ui.tableWidget.item(r,i).text()
            self.ui.tableWidget.setItem(r-1,i,QtWidgets.QTableWidgetItem(item))
            self.ui.tableWidget.setItem(r,i,QtWidgets.QTableWidgetItem(tempItem))
        self.ui.tableWidget.setCurrentCell(r-1,0)
    
    def OnClick_btnAMinus(self):
        '''
        swap two rows
        '''
        selectedItem=self.ui.tableWidget.selectedIndexes()[0]
        r=selectedItem.row()
        #print(r)
        if r>=self.ui.tableWidget.rowCount()-1:
            return
        temp=[]
        for i in range(5):
            tempItem=self.ui.tableWidget.item(r+1,i).text()
            item=self.ui.tableWidget.item(r,i).text()
            self.ui.tableWidget.setItem(r+1,i,QtWidgets.QTableWidgetItem(item))
            self.ui.tableWidget.setItem(r,i,QtWidgets.QTableWidgetItem(tempItem))
        self.ui.tableWidget.setCurrentCell(r+1,0)
        
    
    def OnClick_btnASuppr(self):
        rows=self.selectedRows()
        for r in rows:
            self.ui.tableWidget.removeRow(r)
    
    def OnClick_btnAInsert(self):
        rc=self.ui.tableWidget.rowCount()+1
        self.ui.tableWidget.setRowCount(rc)
        self.ui.tableWidget.setItem(rc-1, 0, QtWidgets.QTableWidgetItem(str(rc)))
        self.ui.tableWidget.setItem(rc-1, 1, QtWidgets.QTableWidgetItem("sf"))
        self.ui.tableWidget.setItem(rc-1, 2, QtWidgets.QTableWidgetItem("sdf"))
        self.ui.tableWidget.setItem(rc-1, 3, QtWidgets.QTableWidgetItem("sdf"))
        self.ui.tableWidget.setItem(rc-1, 4, QtWidgets.QTableWidgetItem(str(0)))
        self.ui.tableWidget.setRowHeight(rc-1, 20)
     
    def OnClick_btnACopy(self):
        '''
        copy selected rows
        '''
        rows=self.selectedRows()
        #copy the datas in memory
        ll=[]
        for r in rows:
            l=[]
            for i in range(5):
                item=self.ui.tableWidget.item(r,i).text()
                l.append(item)
            ll.append(l)
        #duplicate
        for r in ll:
            rc=self.ui.tableWidget.rowCount()+1
            self.ui.tableWidget.setRowCount(rc)
            for i in range(5):
                self.ui.tableWidget.setItem(rc-1, i, QtWidgets.QTableWidgetItem(str(r[i])))
            self.ui.tableWidget.setRowHeight(rc-1, 20)
                   
    
    def selectedRows(self):
        '''
        return a list of selected rows
        '''
        indexes=list(set(index.row() for index in self.ui.tableWidget.selectedIndexes()))
        
        return indexes
        
    
    def OnClick_btnSave(self):
        '''
        '''
        fd = QtWidgets.QFileDialog(self)
        fn=self.ui.edtFileName_template.text()
        if fn=="":
            fn=self.workingdirectory
        else:
            self.workingdirectory=fn
        filename = fd.getOpenFileName(directory=self.workingdirectory)[0]
        
        #print(filename)
        self.ui.edtFileName_template.setText(str(filename))
        self.saveSampleHolderFile(filename)
        
    def OnClick_btnSetTime(self):
        t=self.ui.edtTime.text()
        
        for row in self.selectedRows():
            #ll.append()
            #row=item#.row()
            #print(row)
            self.ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(t))
            
    def OnClick_btnSaveTemplate(self):
        fd = QtWidgets.QFileDialog(self)
        fn=str(self.ui.edtFileName_template.text())
        if fn=="":
            fn=self.workingdirectory
        else:
            self.workingdirectory=fn
        #filename = fd.getOpenFileName(directory=self.workingdirectory)[0]
        filename = fd.getSaveFileName(directory=fn)[0]#self.workingdirectory)[0]
        print(filename)
        if filename=="" :
            return
        txt=str(self.ui.textEdit.toPlainText())
        try:
            f=open(filename,'w')
            f.write(txt)
            f.close()
        except:
             QtWidgets.QMessageBox.information(self,text="Error occured when trying to save "+filename, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
    
    def OnClick_btnSaveMacro(self):
        fd = QtWidgets.QFileDialog(self)
        fn=str(self.ui.edtFileName_macro.text())
        filename = fd.getSaveFileName(directory=fn)[0]#self.workingdirectory)[0]
        if filename=="" :
            return
        self.ui.edtFileName_macro.setText(filename)
        txt=str(self.ui.edtCode.toPlainText())
        try:
            f=open(filename,'w')
            f.write(txt)
            f.close()
        except:
            QtWidgets.QMessageBox.information(self,text="Error occured when trying to save "+filename, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
        
    
    
    
    def readSampleHolderFile(self,filename):
        sh=open(filename)
        ll=sh.readlines()
        title=ll[0].rstrip()
        date=ll[1].rstrip()
        username=ll[2].split("=")[1].rstrip()
        self.ui.edtUserName.setText(username)
        directory=ll[3].split("=")[1].rstrip()
        self.ui.edtDirectory.setText(directory)
        self.samples=[]
        for sample in ll[4:]:
            s=sample.split()
            if len(s)<5:
                for n in range(5-len(s)):
                    s.append("")
            self.samples.append(s)
            
    def saveSampleHolderFile(self,filename):
        f=open(filename,"w")
        rc=self.ui.tableWidget.rowCount()
        title=""
        f.write("#sampleholder=%s\n"%title)
        date=""
        f.write("#date=%s\n"%date)
        username=self.ui.edtUserName.text()
        f.write("#username=%s\n"%username)
        directory=self.ui.edtDirectory.text()
        f.write("#directory=%s\n"%directory)
        samples=[]
        for i in range(rc):
            sample=[]
            sampletxt=""
            for j in range(5):
                txt=str(self.ui.tableWidget.item(i,j).text())
                sample.append(txt)
                sampletxt+=txt+"\t"
            f.write(sampletxt+"\n")
            samples.append(sample)
        #print(samples)
        f.close()
        
    def table2sample(self):
        rc=self.ui.tableWidget.rowCount()
        self.samples=[]
        for i in range(rc):
            sample=[]
            for j in range(5):
                txt=str(self.ui.tableWidget.item(i,j).text())
                sample.append(txt)
            self.samples.append(sample)
        print(self.samples)
    
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  myapp = sampleHolderDialog()
  myapp.show()
  sys.exit(app.exec_())