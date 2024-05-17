"""
Joshua Arribere, Apr 20, 2024

Script to plot the print-to-screen output of the monocle3. Will do
    as a heat map.

Input: pseudo-fasta format, like this for each gene:
>rpl-25.2, rpl-23A.2$
                            facet       tpm prop.cells.expr n.umi
Gonad                       Gonad 1330.6381      0.68899431 15000
Hypodermis             Hypodermis  596.9600      0.30767656  3520
Body wall muscle Body wall muscle  493.9855      0.37482000  9028
Glia                         Glia  328.5101      0.15037594   285
Pharynx                   Pharynx  206.6373      0.06443299   263
Neurons                   Neurons  176.9472      0.03300866   458
Intestine               Intestine  116.7435      0.16293279   138
    Will expect a single fasta file, and will plot genes in the
    order that they're given.

Output: heatmap. Will probably hard-code the tissue order too.

run as python3 plotCaoEtAlFacetTPMOutput.py inFile.txt outPrefix
"""
import sys, common, math
from logJosh import Tee
from pyx import *

def parse(inFile):
    """
    Will parse to a list of lists, where each entry is of the format:
    [geneName:{gonad:ct,...glia:ct}]
    """
    aa=[]
    started=False
    with open(inFile,'r') as f:
        for line in f:
            if line.startswith('>'):##then we're in a new gene
                if started:
                    aa.append({geneName:tempDict})
                geneName=line.strip()[1:]
                tempDict={}
                started=True
            else:
                if 'Gonad' in line:
                    tempDict['Gonad']=line.split('Gonad')[2].strip().split()[0]
                elif 'Hypodermis' in line:
                    tempDict['Hypodermis']=line.split('Hypodermis')[2].strip().split()[0]
                elif 'Body wall muscle' in line:
                    tempDict['Body wall muscle']=line.split('Body wall muscle')[2].strip().split()[0]
                elif 'Glia' in line:
                    tempDict['Glia']=line.split('Glia')[2].strip().split()[0]
                elif 'Pharynx' in line:
                    tempDict['Pharynx']=line.split('Pharynx')[2].strip().split()[0]
                elif 'Neurons' in line:
                    tempDict['Neurons']=line.split('Neurons')[2].strip().split()[0]
                elif 'Intestine' in line:
                    tempDict['Intestine']=line.split('Intestine')[2].strip().split()[0]
    aa.append({geneName:tempDict})
    return aa

def getColor(someNum):
    ##
    if someNum<=10:
        return color.cmyk(0,0,0,1)
    logged=math.log(someNum,10)
    if 1<=logged<=2:
        return color.cmyk(1*(logged-1),0.5*(logged-1),0,1-(logged-1))
    elif 2<logged<=3:
        return color.cmyk(1-0.9*(logged-2),0.5-0.45*(logged-2),0.9*(logged-2),0)
    elif 3<logged<=4:
        return color.cmyk(0,0.05+0.75*(logged-3),0.9+0.1*(logged-3),0)
    elif logged>4:
        return color.cmyk(0,0.8,1,0)

def main(args):
    inFile,outPrefix=args[0:]
    ##
    theData=parse(inFile)
    ##
    c=canvas.canvas()
    labels=['Gonad','Hypodermis','Body wall muscle','Pharynx','Intestine','Glia','Neurons']
    ##write labels across the x-axis
    for ii in range(len(labels)):
        c.text(ii+1.5,0.5,labels[ii],[text.halign.boxleft,text.valign.middle,
            trafo.rotate(90)])
    ##
    ct=0
    for entry in theData:
        ct+=1
        for geneName,tempDict in entry.items():
            ct2=0
            c.text(0.5,-ct+0.5,geneName,[text.halign.boxright,text.valign.middle])
            for label in labels:
                ct2+=1
                theColor=getColor(float(tempDict[label]))
                c.stroke(path.rect(ct2,-ct,1,1),[style.linewidth.Thick,
                                            color.cmyk(0,0,0,0),
                                            deco.filled([theColor])])
    ##
    ##add the key along the right side
    for ii in range(1,4):
        c.text(len(labels)+2.75,-ii,ii,[text.halign.boxleft,text.valign.middle])
        for jj in range(10):
            theNum=ii+jj/10.
            theColor=getColor(10**theNum)
            c.stroke(path.rect(len(labels)+1.5,-theNum,1,0.1),
                [style.linewidth.Thick,theColor,deco.filled([theColor])])
    ##
    c.writePDFfile(outPrefix)


if __name__=='__main__':
    Tee()
    main(sys.argv[1:])
