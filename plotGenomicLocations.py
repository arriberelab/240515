"""
Joshua Arribere, Apr 27, 2024

Script to plot genomic locations of a list of genes.

Input: chrSizes.txt - lengths of each chr in tab-delimited format, i.e.:
    chrI\tsize
    chrII\tsize
    ...
    wbgeneList.txt - line-delimited list of WBGene names
    annotations.gtf - gtf-formatted annotations. Will arbitrarily take
        the left-most point for each gene.

Output: will draw lines for each chr with ticks every million bases.
    Will probably scale chrs by a factor of five. Will draw circles
    for each gene.

run as python3 plotGenomicLocations.py chrSizes.txt wbgeneList.txt
    annots.gtf outPrefix
"""
import sys, common, collections
from logJosh import Tee
from pyx import *

def getChrSizes(inFile):
    aa={}
    with open(inFile,'r') as f:
        for line in f:
            if 'MtDNA' not in line:
                line=line.strip().split('\t')
                aa[line[0]]=int(line[1])
    return aa

def getLocations(annotFile,wbgeneList):
    aa=collections.defaultdict(lambda:
        collections.defaultdict(list))
    ##
    with open(annotFile,'r') as f:
        for line in f:
            if not line.startswith('#'):
                line=line.strip().split('\t')
                geneID=line[8]
                geneID=geneID.split('gene_id "')[1].split('"')[0]
                if geneID in wbgeneList:
                    aa[line[0]][geneID].append(int(line[3]))
    ##
    bb={}
    for k,v in aa.items():
        bb[k]={}
        for k2,vList in v.items():
            bb[k][k2]=min(vList)
    ##
    return bb

def main(args):
    chrSizeFile,wbgeneListFile,annotFile,outPrefix=args[0:]
    ##
    chrSizes=getChrSizes(chrSizeFile)
    ##
    wbgeneList=common.parseGeneList(wbgeneListFile)
    ##
    chrLocations=getLocations(annotFile,wbgeneList)
    ##
    c=canvas.canvas()
    xScale=5*1000000
    yScale=0.5
    c.stroke(path.line(0,1,10000000/xScale,1))
    ii=0
    for theChr,theLength in chrSizes.items():
        print(theChr,theLength)
        c.stroke(path.line(0,ii,theLength/xScale,ii))##draw the axis
        ##
        for wbgene,site in chrLocations[theChr].items():
            c.fill(path.circle(site/xScale,ii+yScale/3.,0.1),
                [deco.filled([color.transparency(0.75)])])
        ii-=yScale
    ##
    c.writePDFfile(outPrefix)

if __name__=='__main__':
    Tee()
    main(sys.argv[1:])

