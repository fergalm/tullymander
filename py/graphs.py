# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 07:23:15 2021

@author: fergal
"""

import matplotlib.collections as mcollect
import matplotlib.pyplot as plt
from anygeom import AnyGeom
import plots as fplots


def updatePlot(geoms, mapper, report_df, highschool_geoms=None):

    # import ipdb; ipdb.set_trace()
    fig = plt.gcf()
    if len(fig.axes) > 0:
        axl = fig.axes[0].axis()
    else:
        axl = None

    plt.clf()

    #So many inches for map
    #So many inches for graphs
    ax1 =fig.add_axes([.05, .6, .9, .35], frameon=False)
    ax2 =fig.add_axes([.05, .05, .9, .55], frameon=False)

    for ax in [ax1, ax2]:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.sca(ax1)

    if axl:
        ax1.axis(axl)
    platPrecincts(geoms, mapper)

    if highschool_geoms is not None:
        addLayer(highschool_geoms, 'r-', lw=1)

    plt.sca(ax2)
    plotReport(report_df)


def platPrecincts(geoms, mapper):
    axl = plt.axis()

    patchList = []
    for i in range(len(geoms)):
        name = geoms.NAME.iloc[i]
        geom = geoms.geom.iloc[i]

        if geom.IsEmpty():
            continue

        district = mapper.getDistrict(name)[0]
        clr = 'C%i' %(district)

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



def plotReport(df):
    df = df.sort_values('NAME').reset_index()
    nrows = len(df)

    bbox=dict(backgroundcolor='w')

    # plt.gca().axes.get_yaxis().set_visible(False)
    # cols = list(set(df.columns) - set("NAME Pop index".split()))
    cols = "Biden2020 Jealous2018 JohnnyO2018 Clinton2016".split()

    xMax = 0
    y0 = len(cols) * nrows
    for i in range(len(df)):

        name = df.loc[i, 'NAME']
        pop = df.loc[i, 'Pop']
        text = "District %s (Pop: %i)" %(name, pop)
        plt.text(0, y0+2,
             text,
             ha="center",
             fontsize=12,
             fontweight='bold',
             fontdict=bbox
        )

        for col in cols:
            val = df.loc[i, col]
            xMax = max(xMax, abs(val))
            addRect(y0, val, col)
            y0 -= 1

        y0 -= 6

    plt.axvline(0, color='k')
    plt.xlim(-xMax, xMax)

def addRect(y, val, name):

    # pprint(locals())
    # idebug()
    if val > 0:
        clr = 'b'
        ha = 'left'
        offset = +1000
    else:
        clr = 'r'
        ha = 'right'
        offset = -1000

    bbox=dict(color='k', backgroundcolor='#FFFFFF88')

    plt.plot([0, val], [y, y], '-', color=clr, lw=2)
    text = "%s %+i" %(name, val)
    plt.text(val+offset, y, text, ha=ha, fontdict=bbox)


def addLayer(geoms, *args, **kwargs):
    for g in geoms:
        fplots.plot_shape(g, *args, **kwargs)