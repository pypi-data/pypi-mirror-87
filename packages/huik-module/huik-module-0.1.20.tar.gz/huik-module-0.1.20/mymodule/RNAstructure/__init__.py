"""
How to use from Hui
from mymodule.RNAstructure import RNA

To get minimal free energy folding:
predict = RNA.fromString('ATCGATCG','rna')

To set temperature:
predict.SetTemperature(298) # unit in Kelvin

predict.PartitionFunction() # this is for generate subopt strucure.

predict.FoldSingleStrand(percent=50,window=0,maximumstructures=10)
predict.GetStructureNumber() # to get structure count
predict.GetFreeEnergy(1) # get minimum free energy
predict.GetPair(position_number,structure_number) # get the pair at position_number for structure_number
"""

import os
datapath = os.path.join(os.path.dirname(__file__),'data_tables')
os.environ["DATAPATH"] = datapath
from ._RNAstructure import RNA,Dynalign_object,Multilign_object #,HybridRNA,Dynalign_object,
