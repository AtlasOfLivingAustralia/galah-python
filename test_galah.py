'''
'''

import sys
import galah
import pandas as pd
from pygalah import atlas as a
from pygalah import search as s

'''
data=s.taxa("Vulpes vulpes")
print("data from the single red fox query")
print(data)
print("testing taxonConceptID (code is data[\'taxonConceptID\'][1]")
print(data['taxonConceptID'][1])
print()
dataMultiple = s.taxa(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
print("data from multiple queries")
print(dataMultiple)
print()
print("print all taxon concept IDs (code is data[\'taxonConceptID\'][:])")
print(dataMultiple['taxonConceptID'][:])
print()
print("print the first one (code is data[\'taxonConceptID\'][0])")
print(dataMultiple['taxonConceptID'][0])
print()

sys.exit()

print("Now, test the counts function")
print("First, test that we can get the counts from the entire ALA")
totalCounts=a.counts()
print("Total counts of the ALA is: {}".format(totalCounts))

sys.exit()
#'''

'''
print()
print("Great, now test this for the species Litoria peronii")
totalCountsVV=a.counts("Litoria peronii")
print("Total counts for Litoria peronii: {}".format(totalCountsVV))
print("Great, now test this for the species Vulpes vulpes")
totalCountsVV=a.counts("Vulpes vulpes")
print("Total counts for Vulpes vulpes: {}".format(totalCountsVV))
print()
print("Now, test it out for multiple species")
totalCountsMultiple = a.counts(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
print("Total counts for multiple species: \n{}".format(totalCountsMultiple))
'''
print("Now, test it out for multiple species with each species separate")
totalCountsMultiple = a.counts(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"],
                               separate=True)
print("Total counts for multiple species: \n{}".format(totalCountsMultiple))
sys.exit()

s.showAllFields()
sys.exit()
# first, test if the ALA is working
print("First, test if the ALA is working")
a.occurrences(test=True)
print("If no error occurs, we are good")
print()

# Now, test if counts is working
print("Test if counts is working")
occurrences = a.occurrences(counts=True)
print("Counts is working for all of ALA: {}".format(occurrences))
print()

# Test if species is working
print("Test if species is working for the Macropus species")
occurrences = a.occurrences(species="Macropus")
print(occurrences)
