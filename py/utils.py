# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:59:53 2020

@author: fergal
"""

# from ipdb import set_trace as idebug
# from pdb import set_trace as debug
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np

import datetime
import osgeo.ogr as ogr


class Timer(object):
    """Time a section of code.

    Usage:
    ----------------------
    .. code-block:: python

        with Timer("Some text"):
            a = long_computation()
            b = even_longer_computation()

    Prints "Some text" to the screen, then the time taken once the computation
    is complete.
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __enter__(self):
        self.t0 = datetime.datetime.now()
        print (self.msg)

    def __exit__(self, type, value, traceback):
        t1 = datetime.datetime.now()

        if self.msg is None:
            self.msg = "Elapsed Time"

        print ("%s %s" %(self.msg, t1 - self.t0))


def lngLatToGeom(lng, lat):
    wkt = "POINT ((%f %f))" %(lng, lat)
    geom = ogr.CreateGeometryFromWkt(wkt)
    return geom
