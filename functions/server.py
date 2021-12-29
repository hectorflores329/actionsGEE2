import ee 
import geemap
import pandas as pd
import numpy as np
import glob
from datetime import date
from datetime import datetime
from datetime import timedelta
from urllib.request import urlopen

file = 'functions/data/ciudades/*.json'
files = glob.glob(file)
filenames = np.array(files)

print('CANTIDAD: ' + str(len(filenames)))          

Map = geemap.Map()

def gases_img1():
    count = 1
    startDate = date(2021, 1, 1) # PERÍODO: 2019-01-01 a 2021-11-30
    # TRY: si no encuentra datos, pass.
    salida = []

    # for i in range(730): # 2 AÑOS
    for i in range(1):
        salida = []
        
        for j in filenames:
            try: 
                fechaInicial = startDate + timedelta(days=i)
                fechaFinal = startDate + timedelta(days=(i + 1))

                fechaI = fechaInicial.strftime('%Y-%m-%d')
                fechaF = fechaFinal.strftime('%Y-%m-%d')

                dataset = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2') \
                              .filter(ee.Filter.date(fechaI, fechaF))

                col_final = dataset.mean().select('NO2_column_number_density')

                geom = geemap.geojson_to_ee(j)
                geom = geom.select('id_ciud_N', 'NO2_column_number_density')

                Datos_Mediana = col_final.reduceRegions (
                  collection = geom,
                  crs = 'EPSG:4326',
                  reducer = ee.Reducer.mean(),
                  scale = 500

                )

                # Asegurarse de que sea un solo valor
                diccionarioParcial = Datos_Mediana.getInfo()['features'][0]['properties']
                diccionarioParcial['Fecha'] = fechaI

                # print(diccionarioParcial)
                salida.append(diccionarioParcial.copy())
                
                df = pd.DataFrame(salida)
                df = df[['Fecha','id_ciud_N','mean']]

                # df.to_excel('functions/descarga/' + str(fechaI) + '.xlsx', index=False)
                df.to_excel(str(fechaI) + '.xlsx', index=False)
                print('Fecha: ' + str(fechaI))

            except:
                print('ERROR')
                
                df = pd.DataFrame(salida)
                df['mean'] = ''
                df = df[['Fecha','id_ciud_N','mean']]
                

                # df.to_excel('functions/descarga/' + str(fechaI) + '.xlsx', index=False)
                df.to_excel(str(fechaI) + '.xlsx', index=False)
                print('Fecha: ' + str(fechaI))



if __name__ == '__main__':
    gases_img1()
            