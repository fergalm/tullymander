# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:50:34 2020

@author: fergal
"""

from ipdb import set_trace as idebug
from pdb import set_trace as debug
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


import frm.census


def main():
    """Query census for population and demographic data.

    Note quite working, only age and total population values are
    available for some reason. I need to debug that,
    But the data is enough to proceced to the next step.
    """
    # cols = dict(
    #     B01001_001E =  'Total Populaton',
    #     B01001A_001E = 'Population White',
    #     B01001B_001E = 'Population Black',
    #     B01002_001E = 'Median Age',
    #     B01003_001E = 'Total Pop again',
    #     B06012_004E = 'Income less than 150% of poverty line',
    #     B07011_001E = 'Median Income',
    #     B05002_013E = 'Foreign born',
    # )


    balco_fips = '24005'  #FIPS for baltimore county
    cols = dict(
        P003001 = 'Total Population',
        P003002 = 'White Population',
        P003003 = 'Black Populatin',
    )

    # #Get demographics
    cq = frm.census.CensusQuery(frm.census.DEFAULT_KEY)
    demo = cq.query_block(2010, 'dec', 'sf1', balco_fips, list(cols.keys()))

    tq = frm.census.TigerQueryDec('/home/fergal/data/elections/shapefiles/tiger')
    geom = tq.query_block(2010, balco_fips)
    geom = geom[ ['GEOID10', 'geoms'] ]

    # return demo, geom
    df = pd.merge(demo, geom, left_on='fips', right_index=True)
    df = df.drop('state county tract block GEOID10'.split(), axis=1)
    df.to_csv('censusdata.csv')
    return df

