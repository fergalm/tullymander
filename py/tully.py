# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:40:57 2020

TODO
o Split off all references to matplotlib to dedicated plotting functions
    This will make it easier to port to the web later

x Get Jupyter working
x Add tool tips
o Add heatmaps
    o Get interactive buttons
    o Add plot style selection method
    o Implement plots

o A config file for easy loading
    o Define inputs a bit better (col names etc.)

o Save figures/output result

o Underlying map?
@author: fergal
"""

from ipdb import set_trace as idebug
from pdb import set_trace as debug
import matplotlib.collections as mcollect
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from precinctmapper import PrecinctToDistrictMapper
from frm.anygeom import AnyGeom

import shapeio
import utils
import toml


Timer = utils.Timer

# from ipywidgets import interact
from IPython.display import display




class StdoutConsole():
    """For compatibility with IPython's display context manager"""
    def __enter__(self):
        pass

    def __exit__(self, a, b, c):
        pass

    def clear_output(self):
        pass


class Tullymander():
    def __init__(self, configfile, console=StdoutConsole()):

        self.loadConfig(configfile)
        self.console = console

        #Configure matplotlib to listen for key presses
        self.figure = plt.figure()
        self.figure.canvas.mpl_disconnect('key_press_event')
        self.figure.canvas.mpl_connect('key_press_event', self)

        #Configure tool tips
        self.handle = None  #Used by tool tips
        self.figure.canvas.mpl_disconnect('motion_notify_event')
        self.figure.canvas.mpl_connect('motion_notify_event', self.tooltip)

        self.printReport()
        self.platPrecincts()

    def loadConfig(self, configfile):
        settings = toml.load(configfile)

        df = shapeio.loadShapefile(settings['shapes'])
        idx = np.array(list(map(lambda x: x is not None, df.NAME)))
        self.geoms = df[idx].copy()

        self.mapper = loadMapper(settings['district_mapper'])
        self.votes = pd.read_csv(settings['vote_history'])
        self.pop_col = settings['precinct_population_column']



        # #A list of precincts and which district they belong to
        # #Also, obviously, placeholder code
        # self.mapper = loadMapper('districtmapper.csv')

        # #The expected vote tally per precinct.
        # self.votes = pd.read_csv('tully_input.csv', index_col=0)

    def __del__(self):
        plt.gcf().canvas.mpl_disconnect('key_press_event')
        plt.gcf().canvas.mpl_disconnect('motion_notify_event')

    def __call__(self, event):
        lng = event.xdata
        lat = event.ydata
        key = event.key

        print(lng, lat, key)
        try:
            newDistrict = int(key)
        except ValueError as e:
            print(e)
            return
        self.updateDistrictOnRequest(lng, lat, newDistrict)
        self.platPrecincts()
        self.printReport()

    def tooltip(self, event):
        lng = event.xdata
        lat = event.ydata

        if self.handle is not None:
            self.handle.set_visible(False) #Delete old tool tip
            del(self.handle)

        precinct = self.identifyPrecinctFromLngLat(lng, lat)
        props = self.votes[self.votes.NAME == precinct]

        self.handle = plt.text(lng, lat, str(props), fontsize=8)
        plt.gcf().canvas.draw_idle()

    def updateDistrictOnRequest(self, lng, lat, newDistrict):
        """Identify precinct at lng,lat and set its district number"""

        precinct = self.identifyPrecinctFromLngLat(lng, lat)
        self.setDistrict(precinct, newDistrict)
        # score = computeScore(self.mapper, self.votes, self.votes_col)
        # print(score)
        # return score


    def identifyPrecinctFromLngLat(self, lng, lat):
        #TODO I should create an rtree for the shapes
        #to be searched faster

        # print([lng, lat])

        try:
            point = AnyGeom([lng, lat], 'POINT').as_geometry()
        except TypeError:
            #Mouse is outside the window
            return None

        # print(point)

        for i in range(len(self.geoms)):
            name = self.geoms.NAME.iloc[i]
            geom = self.geoms.geom.iloc[i]

            if geom.Contains(point):
                return name


    def platPrecincts(self):
        axl = plt.axis()

        plt.clf()
        patchList = []
        for i in range(len(self.geoms)):
            name = self.geoms.NAME.iloc[i]
            geom = self.geoms.geom.iloc[i]

            if geom.IsEmpty():
                continue

            district = self.mapper.getDistrict(name)[0]
            clr = 'C%i' %(district)

            # patches = AnyGeom(geom).as_patch(fc="none", ec=clr, lw=2)
            patches = AnyGeom(geom).as_patch(fc=clr, ec=clr, lw=2, alpha=.2)
            patchList.extend(patches)

        pc = mcollect.PatchCollection(patchList,
                                      match_original=True)

        plt.gca().add_collection(pc)
        plt.plot([-76.6, -76.4], [39.2, 39.7], 'w-', zorder=-1)

        #Reset axis
        if axl[0] != 0:
            plt.axis(axl)
        plt.pause(.001)


    def setDistrict(self, precinct, newDistrict):
        oldDistrict = self.mapper.getDistrict(precinct)[0]
        print("Updating %s from %i to %i" %(precinct, oldDistrict, newDistrict))
        self.mapper.updatePrecinct(precinct, oldDistrict, newDistrict)

    def getReport(self):
        districts = self.mapper.getRange()
        out = pd.DataFrame(columns=self.votes.columns, index=districts)

        for dd in districts:
            precincts = self.mapper.getDomainFor(dd)
            idx = self.votes.NAME.isin(precincts)
            series = list(self.votes[idx].sum().drop('NAME').values)
            series.insert(0, dd)
            out.loc[dd,:] = series
        return out

    def printReport(self):
        self.console.clear_output()
        with self.console:
            display(self.getReport())


    def selectPlatStyle(self, selection):
        pass
# def computeScore(districtMapper, votes, votes_col):
#     results = dict()
#     mapper = districtMapper
#     districts = mapper.listDistricts()

#     idebug()
#     for d in districts:
#         precincts = mapper.getPrecincts(d)
#         idx = votes.precinct.isin(precincts)
#         series = votes[votes_col]
#         assert np.any(idx)
#         results[d] = np.sum(series[idx])

#     return results



def loadMapper(fn):
    df = pd.read_csv(fn)
    # print(df.iloc[0])

    precincts = df.precinct.values
    districts = df.district.values

    mapper = PrecinctToDistrictMapper(precincts, districts)
    return mapper



# def parseElectionResults(fn):
#     df = pd.read_csv(fn)
#     tmp = df['precinct'].apply(lambda x: x[1:])
#     df['precinct'] = tmp

#     idx = df['race'] == 'County Executive'
#     assert np.any(idx)
#     df = df[idx]
#     df['party'] = df['candidate'].str.slice(-4, -1)

#     idx = (df.party == 'DEM') | (df.party == 'REP')
#     df = df[idx]

#     dem = df[df.party == 'DEM']
#     rep = df[df.party == 'REP']

#     merge = pd.merge(dem, rep, on='precinct')
#     merge['county_exec'] = merge['votes_x'] - merge['votes_y']

#     merge = merge[ ['precinct', 'county_exec']  ]
#     return merge



# def shrinkGeoms(self):
#     """Shrink the input geometries so their boundary lines don't overlap"""
#     print("Buffering Geometries")
#     geoms = self.geoms
#     # idebug()
#     # print(str(geoms[0])[:100])
#     # geoms = list(map(lambda x: x.Buffer(-0.05), geoms))
#     for i in range(len(geoms)):
#         g = geoms['geom'].iloc[i]
#         h = g.Buffer(-.005)
#         geoms['geom'].iloc[i] = h
#         # idebug()
#     # self.geoms['geoms'] = geoms
#     # print(str(self.geoms.iloc[0])[:100])

