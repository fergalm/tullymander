# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:15:49 2020

Create the input file to tully.py with the populations
and vote counts for each precinct.
@author: fergal
"""

from ipdb import set_trace as idebug
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import matplotlib.collections as mcollect

from geomcollect import GeomCollection
from frm.anygeom import AnyGeom
import frm.plots as fplots
from tqdm import tqdm
import itertools
import shapeio
import rtree


def main():
    # pop = compute_precinct_population()
    out = pd.read_csv('precinct_pop.csv')
    mapper = dict(P003001='Pop', P003002='WhitePop', P003003='BlackPop')
    out = out.rename(mapper, axis=1)
    out = out[['NAME', 'Pop']]  #Drop demographic info

    fn = "/home/fergal/data/elections/baltco-results/2020G/balco-precinct-results2020.csv"
    votes = pd.read_csv(fn)
    demName = 'Biden-Harris (DEM)'
    gopName = 'Trump-Pence (REP)'
    outName = 'Biden2020'
    out = merge_vote_difference(out, votes, demName, gopName, outName)

    fn = "/home/fergal/data/elections/baltco-results/2018G/balco-precinct-results2018.csv"
    votes = pd.read_csv(fn)

    demName = 'Jealous-Turnbull (DEM)'
    gopName = 'Hogan-Rutherford (REP)'
    outName = 'Jealous2018'
    out = merge_vote_difference(out, votes, demName, gopName, outName)

    demName = 'John "Johnny O" Olszewski Jr (DEM)'
    gopName = 'Al Redmer Jr (REP)'
    outName = 'JohnnyO2018'
    out = merge_vote_difference(out, votes, demName, gopName, outName)

    fn = "/home/fergal/data/elections/baltco-results/2016G/2016G.csv"
    votes = pd.read_csv(fn)
    demName = 'Clinton-Kaine (DEM)'
    gopName = 'Trump-Pence (REP)'
    outName = 'Clinton2016'
    out = merge_vote_difference(out, votes, demName, gopName, outName)

    out.to_csv('tully_input.csv')
    return out

def merge_vote_difference(pop, votes, demName, gopName, outName):
    """Append the per-precinct vote difference between two candidates to pop
    """
    votes.precinct = votes.precinct.apply(format_precinct)
    diff = compute_vote_difference(votes, demName, gopName, outName)
    df = pd.merge(pop, diff, left_on='NAME', right_index=True)


    return df


def format_precinct(precinct):
    """Format a precinct string so it looks like 12-123"""
    left, right = precinct.split('-')
    return "%s-%s" %(left[-2:], right[-3:])

def compute_vote_difference(df, demName, gopName, outColName):
    gr = df.groupby('candidate')
    dfd = gr.get_group(demName)
    dfg = gr.get_group(gopName)

    merge = pd.merge(dfd, dfg, on='precinct')
    diff = merge.votes_x - merge.votes_y

    diff = diff.to_frame(outColName)
    diff.index = merge.precinct
    return diff


def compute_precinct_population():
    """Take the population in each block group and add to population per precinct

    There's a bug somewhere, because some of my blocks aren't contained
    within Baltimore County
    """
    blocks = pd.read_csv('censusdata.csv')

    fn = '/home/fergal/data/elections/shapefiles/precinct2014/BaCoPrecinct-wgs84.shp'
    precincts = shapeio.loadShapefile(fn)
    precinct_tree = GeomCollection(precincts)
    # plt.clf()
    # plot(blocks, precincts)

    cols = ['P003001', 'P003002', 'P003003']
    out = pd.DataFrame(index=precincts.NAME, columns=cols)
    for c in cols:
        out[c] = 0

    error_count = 0
    for i in tqdm(range(len(blocks))):
    # for i in tqdm(range(10)):
        # fplots.plot_shape(blocks.geoms.iloc[0], 'r-', lw=2)
        prow = precinct_tree.find_geom_that_contains(blocks.geoms.iloc[i])

        if prow is None:
            error_count += 1
            continue

        pname = prow.NAME
        #Append counts to this precinct
        for c in cols:
            out.loc[pname, c] += blocks[c].iloc[i]

    print("error count is %i" %(error_count))
    out = out.groupby('NAME').sum()
    return out

def create_precinct_tree(precincts):
    index = rtree.index.Index()

    for i, row in precincts.iterrows():
        name = row.NAME
        env = row.geom.GetEnvelope()
        index.insert(i, env, obj=(name, row.geom))
    return index

def match_block_to_precinct(block_geom, precinct_tree):
    block_geom = AnyGeom(block_geom).as_geometry()
    env = block_geom.GetEnvelope()
    idx = precinct_tree.intersection(env)

    for n in idx:
        name, pgeom = n.object
        print(name, pgeom.Contains(block_geom))
    idebug()
    assert False

    # for each block:
    #     Match to precinct
    #     Add each col to precinct's values


def plot(blocks, precincts):
    plt.clf()
    for g in blocks.geoms:
        fplots.plot_shape(g, color='k', lw=.4)

    cycler = itertools.cycle('rgbmck')
    patchList = []
    for g in precincts.geom:
        clr = next(cycler)
        patches = AnyGeom(g).as_patch(fc=clr, lw=0, alpha=.2)
        patchList.extend(patches)

    pc = mcollect.PatchCollection(patchList,
                                  match_original=True)
    plt.gca().add_collection(pc)

