'''
This is a script that contains tests
'''

import sys,os
import galah
import pandas as pd
from galah import atlas as a
from galah import search as s

class Option:
    def __init__(self, func=str, num=1, default=None, description=""):
        self.func        = func
        self.num         = num
        self.value       = default
        self.description = description

    def __nonzero__(self):
        if self.func == bool:
            return self.value != False
        return bool(self.value)

    def __str__(self):
        return self.value and str(self.value) or ""

    def setvalue(self, v):
        if len(v) == 1:
            self.value = self.func(v[0])
        else:
            self.value = [self.func(i) for i in v]

options = [
    ("-counts",    Option(bool,    0,     False, "X")),
]

def main():
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
    
    print("Now, test it out for multiple species with each species separate")
    totalCountsMultiple = a.counts(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"],
                                   separate=True)
    print("Total counts for multiple species: \n{}".format(totalCountsMultiple))
    sys.exit()
    
    fields = s.showAllFields()
    print(fields)
    sys.exit()
    '''
    # first, test if the ALA is working
    #print("First, test if the ALA is working")
    #a.occurrences(test=True)
    #print("If no error occurs, we are good")
    #print()

    # Now, test if counts is working
    #print("Test if counts is working")
    #occurrences = a.occurrences(getCounts=True)
    #print("Counts is working for all of ALA:\n\n{}".format(occurrences))
    #print()

    # Test if species is working
    #'''
    print("Test if counts is working for the Vulpes vulpes species")
    occurrences = a.counts(species="Vulpes vulpes")
    print(occurrences)

    print("\nTest if 2020 filter in counts is working for the Vulpes vulpes species")
    occurrences = a.counts(species="Vulpes vulpes",filter=["year:2020"])
    occurrences = a.counts(species="Vulpes vulpes",filter=["year:2020"])
    print(occurrences)

    print("\nTest if 2019 and 2020 filters in counts are working for the Vulpes vulpes species")
    occurrences = a.counts(species="Vulpes vulpes",filter=["year:2020","year:2019"])
    print(occurrences)

    print("\nTest if 2020 filter in counts is working for the species array")
    occurrences = a.counts(species=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"],
                           filter=["year:2020"])
    print(occurrences)
    print("\nTest if 2019 and 2020 filters in counts are working for the species array")
    occurrences = a.counts(species=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"],
                           filter=["year:2020","year:2019"])
    print(occurrences)
    print("\nTest if 2019 and 2020 filters are working for the species array and separate")
    occurrences = a.counts(species=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"],
                           filter=["year:2020","year:2019"],separate=True)
    print(occurrences)

    print("\nTest if occurrences is working for Vulpes vulpes")
    occurrences = a.occurrences(species="Vulpes vulpes")
    print(occurrences.columns)
    print(occurrences)
    print("\n\n\nTest if occurrences is working for multiple")
    occurrences = a.occurrences(species=["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
    print(occurrences.columns)
    print(occurrences)
    print()
    #'''

if __name__=="__main__":
    args = sys.argv[1:]
    main()