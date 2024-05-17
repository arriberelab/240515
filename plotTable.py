"""
Joshua Arribere, May 1, 2024

Script to plot a tab-delimited table.

Input: inFile.txt of the format:
    val\tcol1\t...colN
    label1\tct1\t...ctN
    ...
    labelZ\tct1\t...ctN
    Will plot as a log-y-scale.

Output: barplot

run as python3 plotTable.py inFile.txt outPrefix
"""
import sys, common
from logJosh import Tee
from pyx import *


def main(args):
    inFile,outPrefix=args[0:]
    ##
    mypainter = graph.axis.painter.bar(nameattrs=[trafo.rotate(45),
                                              text.halign.right],
                                   innerticklength=0.1)
    #
    myaxis = graph.axis.nestedbar(painter=mypainter)
    #
    g=graph.graphxy(width=2.5,height=4,x=myaxis,
        y=graph.axis.log(max=5*(10**6)))
    ##
    g.plot(graph.data.file(inFile,xname="$1, 0",y=2,skiphead=1),
        [graph.style.bar()])
    g.plot(graph.data.file(inFile,xname="$1, 1",y=3,skiphead=1),
        [graph.style.bar()])
    g.plot(graph.data.file(inFile,xname="$1, 2",y=4,skiphead=1),
        [graph.style.bar()])
    ##
    g.writePDFfile(outPrefix)

if __name__=='__main__':
    Tee()
    main(sys.argv[1:])
