"""
Joshua Arribere, Apr 26, 2024

Script to plot a table of
    WBGene\tCts
    for only one library. Will also have the ability to highlight genes of interest.

Input: inFile.txt - tab-delimited file of the format
    WBGene\tct1\t...ctN
        Will average across ct1...ctN. There may be only one library.
    minCt - minimum number of reads/gene
    highlights.txt - line-delimited list of files like this:
        groupName1\tfileName1.txt
        groupName2\tfileName2.txt
        ...
        where each fileNamei.txt is a line-delimited list of WBGenes

run as python3 plotGeneExpressionOneDimensional.py inFile.txt minCt highlights.txt
    outPrefix
"""
import sys, common, numpy
from logJosh import Tee
from pyx import *

def parseGeneCtsFile(inFile,minCts):
    aa={}
    with open(inFile,'r') as f:
        f.readline()#skip header
        for line in f:
            line=line.strip().split('\t')
            val=numpy.average(list(map(float,line[1:])))
            if val>=minCts:
                aa[line[0]]=val
    ##
    return aa

def parse(highlightsFile):
    aa=[]
    with open(highlightsFile,'r') as f:
        for line in f:
            line=line.strip().split('\t')
            aa.append((line[0],common.parseGeneList(line[1])))
    ##
    return aa

def main(args):
    geneCtFile,minCts,highlightsFile,outPrefix=args[0:]
    ##
    geneCts2=parseGeneCtsFile(geneCtFile,float(minCts))
    geneCts=dict((k,[numpy.random.normal(0,0.1),v]) for k,v in geneCts2.items())
    print('eL28',geneCts['WBGene00004442'])
    ##
    highlights=parse(highlightsFile)
    ##
    g=graph.graphxy(width=1,height=4,
        x=graph.axis.linear(min=-0.5,max=0.5),
        y=graph.axis.log(min=int(minCts),title='Log Expression'),
        key=graph.key.key(pos='tr',hinside=0))
    ##
    g.plot(graph.data.points([entry for entry in geneCts.values()],x=1,y=2),
            [graph.style.symbol(graph.style.symbol.circle,
                symbolattrs=[color.cmyk.black,deco.filled,color.transparency(0.8)],
                size=0.01)])
    ##
    ii=0
    for entry in highlights:
        ##
        print(entry[0])
        for k,v in geneCts.items():
            if k in entry[1]:
                print(k,v)
        ##
        temp=[v for k,v in geneCts.items() if k in entry[1]]
        g.plot(graph.data.points(temp,x=1,y=2,title=entry[0]),
                [graph.style.symbol(graph.style.symbol.circle,
                    symbolattrs=[common.colors(ii),deco.filled],
                    size=0.05)])
        if ii==0:
            for k,v in geneCts.items():
                if k in entry[1] and v[1]<=2000:
                    ##print(k,v)
                    pass
        ii+=1
    #
    g.writePDFfile(outPrefix)

if __name__=='__main__':
    Tee()
    main(sys.argv[1:])
