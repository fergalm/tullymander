# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:52:49 2020

@author: fergal
"""

from pdb import set_trace as debug
import pandas as pd
import numpy as np

import osgeo.ogr as ogr

def loadShapefile(fn):
    """
    Load a shapefile from disk

    Inputs
    -------
    fn
        (str) Path to file


    Returns
    -----------
    geoms
        A list of OGR geometry objects
    properties
        A dataframe

    Notes
    --------
    * Assumes only one layer in a shapefile. Is that correct?

    """
    driverName = "ESRI Shapefile"
    drv = ogr.GetDriverByName( driverName )
    if drv is None:
        raise IOError("Can't read shapefiles")

    dataSource = drv.Open(fn, 0) # 0 means read-only. 1 means writeable.
    if dataSource is None:
        raise IOError("Can't open %s" %(fn))

    layer = dataSource.GetLayer()

    fieldNames = getFieldNames(layer)
    geoms = []
    properties = []

    for feature in layer:
        geoms.append(feature.GetGeometryRef().Clone())

        prop = []
        for f in fieldNames:
            prop.append(feature.GetField(f))
        properties.append(prop)

    df = pd.DataFrame(properties, columns=fieldNames)
    df['geom'] = geoms
    return df

def getFieldNames(layer):

    layerDefinition = layer.GetLayerDefn()
    fieldNames = []
    for i in range(layerDefinition.GetFieldCount()):
        fieldNames.append( layerDefinition.GetFieldDefn(i).GetName() )

    return fieldNames
