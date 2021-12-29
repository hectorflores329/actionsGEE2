import ee 
import geemap
import pandas as pd
import numpy as np
import glob
from datetime import date
from datetime import datetime
from datetime import timedelta
from urllib.request import urlopen

def descargaGEE():
    Map = geemap.Map()

    studyArea = ee.FeatureCollection("users/testHector/Lim_comunas")
    studyArea = studyArea.filterMetadata("COMUNA","equals", "1403")

    Fecha_inicial = "2010-01-01"
    Fecha_final = "2011-01-01"


    FIRMS_colection2 =  ee.ImageCollection('FIRMS')
    FIRMS_colection =  ee.ImageCollection('FIRMS');#focos de incendios

    FIRMS4 =FIRMS_colection2 \
    .select(['T21']) \
    .filterDate(Fecha_inicial,Fecha_final) \
    .filterBounds(studyArea)

    FIRMS =FIRMS_colection \
    .select(['T21']) \
    .filterDate(Fecha_inicial,Fecha_final) \
    .filterBounds(studyArea)

    FIRMScount4  = ee.Image(FIRMS4.count()).clip(studyArea)
    FIRMSbinary4 = FIRMScount4.eq(FIRMScount4).rename('FIRMS_binary_alert_3')

    project_crs   = ee.Image(FIRMS.first()).projection().crs()
    scale = ee.Image(FIRMS.first()).projection().nominalScale()


    FIRMSpoint4 = FIRMSbinary4.reduceToVectors(
    geometry =  studyArea,
    eightConnected = True,
    labelProperty = 'modis_fire',
    maxPixels = 1e16,
    crs = project_crs,
    scale = scale,
    geometryType =  'centroid',
    bestEffort =  True,
    tileScale = 16
    )

    numero_PI = ee.FeatureCollection(FIRMSpoint4).filterBounds(studyArea)

    cantidad_PI = numero_PI.size()
    cantidad =  cantidad_PI.getInfo()

    print(cantidad)
            

if __name__ == '__main__':
    descargaGEE()
            

