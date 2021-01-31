# -*- coding: utf-8 -*-
"""
A 2 way dictionary class, for many-to-many mappings
"""



class ManyToManyMapper():
    """Store a quick look up table between two sets of values
    where the mapping can be many to many.
    """
    def __init__(self, domain, rng):
        """
        Inputs
        ------
        domain, rng
            (lists) The ith element of domain maps to the ith
            element of rng, and vice versa. Neither the elements
            of domain nor rng need be unique
        """

        domainDict = {}
        rangeDict = {}

        for d, r in zip(domain, rng):
            if d in domainDict:
                domainDict[d].append(r)
            else:
                domainDict[d] = [r]

            if r in rangeDict:
                rangeDict[r].append(d)
            else:
                rangeDict[r] = [d]

        self.domainDict = domainDict
        self.rangeDict = rangeDict

    def getRange(self):
        return list(self.rangeDict.keys())

    def getDomain(self):
        return list(self.domainDict.keys())

    def getRangeFor(self, domain):
        return self.domainDict[domain]

    def getDomainFor(self, rng):
        return self.rangeDict[rng]



class PrecinctToDistrictMapper(ManyToManyMapper):
    def __init__(self, precincts, districts):
        ManyToManyMapper.__init__(self, precincts, districts)

    def listPrecincts(self):
        return self.getDomain()

    def listDistricts(self):
        return self.getRange()

    def getPrecincts(self, district):
        return self.getDomainFor(district)

    def getDistrict(self, precinct):
        return self.getRangeFor(precinct)

    def updatePrecinct(self, precinct, oldDistrict, newDistrict):
        """Move a precinct from oldDistrict to newDistrict"""
        self.domainDict[precinct] = [newDistrict]

        #Get the list of precincts for the old district
        pcList = self.rangeDict[oldDistrict]
        #Remove this precinct
        i = pcList.index(precinct)
        pcList.pop(i)

        self.rangeDict[newDistrict].append(precinct)
