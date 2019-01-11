# segmented_dac class 
# Last modification by Marko Kosunen, marko.kosunen@aalto.fi, 16.11.2018 14:15
#Add TheSDK to path. Importing it first adds the rest of the modules
#Simple buffer template
import os
import sys
import numpy as np

from thesdk import *
from verilog import *
from vhdl import *

class segmented_dac(thesdk):
    def __init__(self,*arg): 
        self.proplist=['Dacbits', 'Dacbinbits']
        self.iptr_real_t = IO();    # Pointer for thermometer coded input data
        self.iptr_real_b = IO();    # Pointer for binary coded input data
        self.iptr_imag_t = IO();    # Pointer for thermometer coded input data
        self.iptr_imag_b = IO();    # Pointer for binary coded input data
        self.Dacbits=9
        self.Dacbinbits=4
        self.model='py';                #can be set externally, but is not propagated
        self.par= False                 #By default, no parallel processing
        self.queue= []                  #By default, no parallel processing
        self._Z = IO;             # Pointer for output data
        if len(arg)>=1:
            parent=arg[0]
            self.copy_propval(parent,self.proplist)
            self.parent =parent;
        self.init()
    def init(self):
        pass
    def main(self):
        out=(np.char.count(self.iptr_real_t.Data,'1')*2**self.Dacbinbits
                +self.iptr_real_b.Data-(2**(self.Dacbits-1)-1)
                +1j*(np.char.count(self.iptr_imag_t.Data,'1')*2**self.Dacbinbits
                    +self.iptr_imag_b.Data-(2**(self.Dacbits-1)-1))).reshape(-1,1)
        if self.par:
            self.queue.put(out)
        self._Z.Data=out

    def run(self,*arg):
        if len(arg)>0:
            self.par=True      #flag for parallel processing
            self.queue=arg[0]  #multiprocessing.queue as the first argument
        if self.model=='py':
            self.main()
        else: 
            self.print_log({'type':"F",'msg':"Only Python model available"})

    def write_infile(self):
        pass

    def read_outfile(self):
        pass

if __name__=="__main__":
    import matplotlib.pyplot as plt
    from  segmented_dac import *
    t=thesdk()
    t.print_log({'type':'I', 'msg': "This is a testing template. Enjoy"})
