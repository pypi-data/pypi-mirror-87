# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 09:32:28 2019

@author: tache
"""

from nexusformat.nexus import *
from numpy import *
import os
#filepath="//crabe/Communs/NIMBE/LIONS/SWING-Jan2019/20181790/2019/Run2/dc"
#file="DC_00280_2019-03-13_21-48-14.nxs"
def exportEDF(nxfile):
    if not os.path.exists(nxfile):
        print(str(nxfile)+" not exist. Exiting")
        return
    print('opening '+nxfile,end="",flush=True)
    try:
        dc=nxload(nxfile)
        im=dc[list(dc)[0]].scan_data.eiger_image.nxvalue
    
        print('\taveraging '+str(len(im))+" frames",end="",flush=True)
        avgIm=im[0]
        for imm in im[1:]:
            avgIm+=imm
        avgIm=avgIm/len(im)
        from fabio import edfimage
        edf=edfimage.EdfImage(avgIm)
        outfile=nxfile.split('.')[0]+".edf"
        print('\twriting to '+outfile,end="",flush=True)
        #edfName=filepath+os.sep+fname+".edf"
        edf.write(outfile)   #UNCOMMENT THIS LINE
        print('\tdone ',end="\n")
    except:
        print("\tError when opening nexus file")
        return
    
if __name__=='__main__':
    #from sys import argv
    import sys
    from glob import glob
    #from sys import argv
    if len(sys.argv)<=1:
        print("USAGE : nexus.py filename")
    else:
        for filename in glob(sys.argv[1]):
            #print(filename)
            exportEDF(filename)

    

