# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:15:49 2020

Create the input file to tully.py with the populations
and vote counts for each precinct.
@author: fergal
"""

from ipdb import set_trace as idebug
import pandas as pd



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


