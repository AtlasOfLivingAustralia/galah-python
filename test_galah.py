'''
This is a script that contains tests
'''

import sys,os
import galah
import pandas as pd
from galah import atlas as a
from galah import search as s
from galah import galah as g

# class for the options for the script
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

# function that parses the options the user passes to the script
def option_parser(args,options):

    # create the options list
    options = dict([i for i in options if not type(i) == str])
    #print(options)

    # Check whether there is a request for help
    if '-h' in args or '--help' in args:
        for item in options:
            if type(item) == str:
                print(item)
        for item in options:
            if type(item) != str:
                print("%10s  %s" % (item[0], item[1].description))
        print()
        sys.exit()

    # get the arguments
    while args:
        ar = args.pop(0)
        if ar in options and options[ar].func == bool:
            options[ar].value = True
        else:
            ar = args.pop(0)
            options[ar].setvalue([args.pop(0) for i in range(options[ar].num)])

    return options

# options for the testing script
options = [
    ("-all",           Option(bool, 0, False, "Runs all tests.")),
    ("-taxa",          Option(bool, 0, False, "Runs all tests for the taxa function.")),
    ("-counts",        Option(bool, 0, False, "Runs all tests for the counts function.")),
    ("-testALA",       Option(bool, 0, False, "Runs all tests for checking if ALA is working.")),
    ("-occurrences",   Option(bool, 0, False, "Runs all tests for the occurrences function.")),
    ("-showAllFields", Option(bool, 0, False, "Runs all tests for the showAllFields function.")),
    ("-groupBy",       Option(bool, 0, False, "Runs all tests for the groupBy function.")),
    ("-showAllValues", Option(bool, 0, False, "Runs all tests for the showAllValues function.")),
    ("-select",        Option(bool, 0, False, "Runs all tests for the select function.")),
]
'''
        # how to get taxonConceptIDs
        print("testing taxonConceptID (code is data[\'taxonConceptID\'][1]")
        print(data['taxonConceptID'][1])
        print()
        print("print all taxon concept IDs (code is data[\'taxonConceptID\'][:])")
        print(dataMultiple['taxonConceptID'][:])
        print()
        print("print the first one (code is data[\'taxonConceptID\'][0])")
        print(dataMultiple['taxonConceptID'][0])
        print()
'''
# main function that includes all the tests Amanda has done to get the package running so far
def main(options):

    email = "amanda.buyan@csiro.au"

    # check if taxa is working for Vulpes vulpes and multiple enquiries
    if options['-taxa'].value or options['-all'].value:

        data=s.taxa("Vulpes vulpes")
        print("data from the single Vulpes vulpes query")
        print(data)

        dataMultiple = s.taxa(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
        print("data from multiple queries")
        print(dataMultiple)
        print()

    # check if counts is working, including filters
    if options['-counts'].value or options['-all'].value:
        print("First, test that we can get the counts from the entire ALA")
        totalCounts=a.counts()
        print("Total counts of the ALA is: {}".format(totalCounts))

        print("Great, now test this for the species Vulpes vulpes")
        totalCountsVV=a.counts("Vulpes vulpes")
        print("Total counts for Vulpes vulpes: {}".format(totalCountsVV))
        print()
        print("Now, test it out for multiple species")
        totalCountsMultiple = a.counts(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"])
        print("Total counts for multiple species: \n{}".format(totalCountsMultiple))

        print("\nNow, test it out for multiple species with each species separate")
        totalCountsMultiple = a.counts(["Osphranter rufus","Vulpes vulpes","Macropus giganteus","Phascolarctos cinereus"],
                                       separate=True)
        print("Total counts for multiple species: \n{}".format(totalCountsMultiple))

        print("\nTest if 2020 filters in counts is working for the Vulpes vulpes species")
        totalCountsVV2020 = a.counts(species="Vulpes vulpes", filters=["year=2020"])
        print(totalCountsVV2020)

        print("\nTest if 2019 and 2020 filters in counts are working for the Vulpes vulpes species")
        totalCountsVV20202019 = a.counts(species="Vulpes vulpes", filters=["year=2020", "year=2019"])
        print(totalCountsVV20202019)

        print("\nTest if 2020 filters in counts is working for the species array")
        occurrences = a.counts(
            species=["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"],
            filters=["year=2020"])
        print(occurrences)
        print("\nTest if 2019 and 2020 filters in counts are working for the species array")
        occurrences = a.counts(
            species=["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"],
            filters=["year=2020", "year=2019"])
        print(occurrences)
        print("\nTest if 2019 and 2020 filters  are working for the species array and separate")
        occurrences = a.counts(
            species=["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"],
            filters=["year=2020", "year=2019"], separate=True)
        print(occurrences)

    # check if showAllFields is working
    if options['-showAllFields'].value or options['-all'].value:
        fields = s.showAllFields()
        print(fields)
        sys.exit()

    if options['-testALA'].value or options['-all'].value:
        print("test if the ALA is working")
        a.occurrences(test=True)
        print("If no error occurs, we are good")
        print()

    if options['-occurrences'].value or options['-all'].value:
        print("\nTest if occurrences is working for Vulpes vulpes")
        occurrences = a.occurrences(species="Vulpes vulpes",email=email)
        print(occurrences.columns)
        print(occurrences)
        print("\n\n\nTest if occurrences is working for multiple species")
        occurrences = a.occurrences(
            species=["Osphranter rufus", "Vulpes vulpes", "Macropus giganteus", "Phascolarctos cinereus"],email=email)
        print(occurrences.columns)
        print(occurrences)
        print()

    if options['-groupBy'].value or options['-all'].value:
        print("Test this is working for all counts (no species yet)")
        counts=a.counts(filters=["year>2010",'basisOfRecord=HUMAN_OBSERVATION'],groups="year",expand=False)
        print(counts)
        print()
        print("Test this is working for multiple groups, expand=False")
        counts=a.counts(filters=["year>2018","basisOfRecord=HUMAN_OBSERVATION"],groups=["year","basisOfRecord"],expand=False)
        counts = a.counts(filters=["year>2010"], groups=["year", "basisOfRecord"],expand=False)
        print(counts)
        print("Test this is working for multiple groups, expand=True")
        counts=a.counts(filters=["year>2018"],groups=["year","basisOfRecord"],expand=True)
        print(counts)

    if options['-showAllValues'].value or options['-all'].value:
        print("Test this is working for basisOfRecord")
        values=s.showAllValues("basisOfRecord")
        print(values)

    if options['-select'].value or options['-all'].value:
        print("Test this is working for select")
        values=a.occurrences(species="Vulpes vulpes",fields=['decimalLatitude','decimalLongitude'],email="amanda.buyan@csiro.au") #,verbose=True)
        print(values)

if __name__=="__main__":
    args = sys.argv[1:]
    options = option_parser(args,options)
    main(options)