"""
How to use NUPACK - Hui 5/8
from mymodule import mymodule as NPK

# To predict mfe structure:
# pseudo: pseudo knot , sodium and magnesium in M,
NPK.mfe(['GGGGATACCCC'],dangles='some',T=37,material='dna',pseudo=False,sodium=0.05,magnesium=0.005)
>>> [('(((....))).', '-2.685')]

To predict multistrand:
concentrations in M, 
NPK.complexes(sequences=[''], concentrations=[1], maxcofoldstrand=2, material='dna',
              dangles='some', T=37, multi=True, pseudo=False,
              sodium=1.0, magnesium=0.0, **kwargs):
return a dict, k:list [sequence,Q,conc, structure, dG ]

"""
from ._NUPACK import *
