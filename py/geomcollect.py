# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 13:06:00 2020

@author: fergal
"""

# from ipdb import set_trace as idebug
# import numpy as np


from anygeom import AnyGeom
import plots as fplots
import rtree


class GeomCollection():
    """Quick and dirty code to figure out which of a set of geometries
    contains the requested geometry.

    Ensures a requested geom is considered contained even if they
    share an edge.

    Assumes none of the input geometries overlap (e.g they are
    precincts)
    """
    def __init__(self, geom_df):
        self.geom_df = geom_df
        self.geom_tree = self.create_tree()


    def create_tree(self):
        tree = rtree.index.Index(interleaved=False)
        for i, row in self.geom_df.iterrows():
            geom  = row.geom
            env = geom.GetEnvelope()
            tree.insert(i, env)
        return tree

    def find_geom_that_contains(self, shape):
        geom = AnyGeom(shape).as_geometry()
        env = geom.GetEnvelope()

        idx = self.geom_tree.intersection(env)
        for i in idx:
            pgeom = self.geom_df.geom.iloc[i]

            if self.contains(pgeom, geom):
                return self.geom_df.iloc[i]

    def contains(self, a, b):
        """A contains B, even if they share an edge"""
        area1 = a.Intersection(b).Area()
        area2 = b.Area()

        return area1 / area2 > .9

    def plot(self, *args, **kwargs):
        for geom in self.geom_df.geom:
            fplots.plot_shape(geom, *args, **kwargs)
