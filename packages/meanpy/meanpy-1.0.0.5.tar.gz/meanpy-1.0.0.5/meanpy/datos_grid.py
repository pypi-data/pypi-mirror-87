# Copyright 2020 by Erick Alexis Alvarez Sanchez, The national meteorological and hydrological service of Peru (SENAMHI).
# All rights reserved.
# This file is part of the MEANpy package,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import xarray as xray
import pandas as pd
import numpy as np
from .convertible import pre_rea
from .convertible_e import pre_rea_station
from .ploteos import convertido
import os.path

def open_observed_and_models(obs,modelo,proy,var,f_clim,f_pro,anual=False):
    obs=xray.open_dataset(obs)
    obs=obs[var].sel(time=slice(f_clim[0],f_clim[1]))
    #PARA ANUAL O MENSUAL
    if anual==True:
        tiempos=pd.date_range(start=f_clim[0],freq='YS',periods=len(obs.time))
    else:
        tiempos=pd.date_range(start=f_clim[0],freq='MS',periods=len(obs.time))
    ################################################################
    obs['time']=tiempos
    for la,lo in zip(['latitud','latitude','Latitude'],['longitud','longitude','Longitude']):
        if ((la in obs.coords.dims) and (lo in obs.coords.dims)):
            print('cambiando nombre de coordenadas a latlon')
            obs=obs.rename({la:'lat',lo:'lon'})
        else:
            print('nombres latlon correcto')
    modelos=[]
    proyecciones=[]
    f=0
    for n,(i,j) in enumerate(zip(modelo,proy)):
        model=xray.open_dataset(i)
        model=model[var].sel(time=slice(f_clim[0],f_clim[1]))
        #PARA ANUAL O MENSUAL
        if anual==True:
            tiempos=pd.date_range(start=f_clim[0],freq='YS',periods=len(model.time))
        else:
            tiempos=pd.date_range(start=f_clim[0],freq='MS',periods=len(model.time))
        ################################################################
        model['time']=tiempos
        proyec=xray.open_dataset(j)
        proyec=proyec[var].sel(time=slice(f_pro[0],f_pro[1]))
        #PARA ANUAL O MENSUAL
        if anual==True:
            tiempos=pd.date_range(start=f_pro[0],freq='YS',periods=len(proyec.time))
        else:
            tiempos=pd.date_range(start=f_pro[0],freq='MS',periods=len(proyec.time))
        ################################################################
        proyec['time']=tiempos
        #--------comprobar nombre en latlon-------------------------------------------
        for model_data,n_dat in zip([model,proyec],['model','proyec']):
            for la,lo in zip(['latitud','latitude','Latitude'],['longitud','longitude','Longitude']):
                if ((la in model_data.coords.dims) and (lo in model_data.coords.dims)):
                    if n_dat=='model':
                        print('cambiando nombre de coordenadas a latlon')
                        model=model.rename({la:'lat',lo:'lon'})
                    if n_dat=='proyec':
                        print('cambiando nombre de coordenadas a latlon')
                        proyec=proyec.rename({la:'lat',lo:'lon'})
                else:
                    print('nombres latlon correcto')
        #_---------------------------------------------------------------------------
        new_lat=obs['lat'].values
        new_lon=obs['lon'].values
        #---------interpolacion---------------------------------------------------
        if not (np.array_equal(new_lat,model['lat'].values) and np.array_equal(new_lon,model['lon'].values)):
            print('interpolando latlon')
            model=model.interp(lat=new_lat,lon=new_lon)
        if not (np.array_equal(new_lat,proyec['lat'].values) and np.array_equal(new_lon,proyec['lon'].values)):
            print('interpolando latlon')
            proyec=proyec.interp(lat=new_lat,lon=new_lon)
        #------------------------------------------------------------------------
        f+=1
        if f==1:
            modelos=model.copy()
            proyecciones=proyec.copy()
        else:
            modelos=xray.concat([modelos,model],dim='modelo')
            proyecciones=xray.concat([proyecciones,proyec],dim='modelo')
    return pre_rea(obs,modelos,proyecciones,anual)

def open_station_and_models(estaciones,observados,modelo,proy,var,f_clim,f_pro):
    cnj_datos=dict()
    coords=pd.read_csv(estaciones,delimiter=';',index_col=0)
    observados=pd.read_csv(observados,delimiter=';',index_col=0)
    observados.index=pd.to_datetime(observados.index,format='%d/%m/%Y')
    observados=observados.loc[f_clim[0]:f_clim[1]]
    modelos=[]
    proyecciones=[]
    f=0
    for n,(i,j) in enumerate(zip(modelo,proy)):
        model=xray.open_dataset(i)
        model=model[var].sel(time=slice(f_clim[0],f_clim[1]))
        tiempos=pd.date_range(start=f_clim[0],freq='MS',periods=len(model.time))
        model['time']=tiempos
        proyec=xray.open_dataset(j)
        proyec=proyec[var].sel(time=slice(f_pro[0],f_pro[1]))
        tiempos=pd.date_range(start=f_pro[0],freq='MS',periods=len(proyec.time))
        proyec['time']=tiempos
        #------------comprobar nombre en latlon---------------------------------
        for model_data,n_dat in zip([model,proyec],['model','proyec']):
            for la,lo in zip(['latitud','latitude','Latitude'],['longitud','longitude','Longitude']):
                if ((la in model_data.coords.dims) and (lo in model_data.coords.dims)):
                    if n_dat=='model':
                        print('cambiando nombre de coordenadas a latlon')
                        model=model.rename({la:'lat',lo:'lon'})
                    if n_dat=='proyec':
                        print('cambiando nombre de coordenadas a latlon')
                        proyec=proyec.rename({la:'lat',lo:'lon'})
                else:
                    print('nombres latlon correcto')
        #------------------------------------------------------------------------
        f+=1
        if f==1:
            new_lat=model['lat'].values
            new_lon=model['lon'].values
            modelos=model.copy()
            proyecciones=proyec.copy()
        else:
            #----------interpolacion--------------------------------------------------
            if not (np.array_equal(new_lat,model['lat'].values) and np.array_equal(new_lon,model['lon'].values)):
                print('interpolando latlon')
                model=model.interp(lat=new_lat,lon=new_lon)
            if not (np.array_equal(new_lat,proyec['lat'].values) and np.array_equal(new_lon,proyec['lon'].values)):
                print('interpolando latlon')
                proyec=proyec.interp(lat=new_lat,lon=new_lon)
            #------------------------------------------------------------------------
            modelos=xray.concat([modelos,model],dim='modelo')
            proyecciones=xray.concat([proyecciones,proyec],dim='modelo')
    #MOMENTANEO-----------------------------------------------------
    #if modelos['lon'].max()>180:
    #    modelos['lon']=modelos['lon']-360.0
    #if proyecciones['lon'].max()>180:
    #    proyecciones['lon']=proyecciones['lon']-360.0
    #-------------------------------------------------------------
    return pre_rea_station(coords,observados,modelos,proyecciones)
