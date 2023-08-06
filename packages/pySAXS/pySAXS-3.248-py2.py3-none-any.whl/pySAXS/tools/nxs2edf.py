# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:10:56 2020

@author: tache
"""

from nexusformat.nexus import *
import os
import sys
from fabio import edfimage

from glob import glob
from sys import argv

def main(argv):
    file=argv
    print('*'*40)
    print("Reading nx file : %s"%file)
    dc=nxload(file)
    dcl=list(dc)
    print("Nx entry : %s "%dcl[0])
    
    
    edfName=file.split('.')[0]+".edf"
    print("EDF file wiil be : %s"%edfName)
    im=dc[list(dc)[0]].scan_data.eiger_image.nxvalue
    print("averaging %i images"%len(im))
    avgIm=im[0]
    for imm in im[1:]:
        avgIm+=imm
    avgIm=avgIm/len(im)
    edf=edfimage.EdfImage(avgIm)
    edf.header['Comment']=dc[list(dc)[0]]
    #dheader={'x','z','count_time','pilroi0','pilai1']
    diode=eval("dc['"+list(dc)[0]+"']['SWING']['i11-c-c09__dt__mi_diode.8b']['AverageIntensity']").nxvalue
    tt=eval("dc['"+list(dc)[0]+"']['SWING']['EIGER-4M']['exposure_time']").nxvalue
    edf.header['count_time']=tt
    edf.header['pilroi0']=diode
    edf.header['pilai1']=eval("dc['"+list(dc)[0]+"']['SWING']['i11-c-c09__dt__mi_diode.9']['AverageIntensity']").nxvalue
    
    for n in list(dc[dcl[0]]['SWING']['EIGER-4M']):
        print("%s  : %s "%(n,dc[dcl[0]]['SWING']['EIGER-4M'][n].nxvalue))
        edf.header[n]=dc[dcl[0]]['SWING']['EIGER-4M'][n].nxvalue
    edf.write(edfName)
    print("EDF file written")
    
if __name__ == "__main__":
    
    for filename in glob(argv[1]):
        #print(filename)
        main(filename)