# Copyright 2020 by Erick Alexis Alvarez Sanchez, The national meteorological and hydrological service of Peru (SENAMHI).
# All rights reserved.
# This file is part of the MEANpy package,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import xarray as xray
import numpy as np
import pandas as pd
from .ploteos import convertido_e

class pre_rea_station(object):
    def __init__(self,estaciones,obs,mod,pro):
        self.estaciones=estaciones
        self.observados=obs
        self.modelos=mod
        self.proyecciones=pro

    def rea_perform(self,acu=False):
        print("iniciando rea")
        cnj_obs=pd.DataFrame()
        cnj_mod=pd.DataFrame()
        cnj_pro=pd.DataFrame()
        cnj_rea=pd.DataFrame()
        cnj_incertidumbre=pd.DataFrame()
        cnj_serie_rea=pd.DataFrame()
        cnj_cambios=pd.DataFrame()
        cnj_r_fc=pd.DataFrame()
        coords=self.estaciones
        for name in self.estaciones['nombre']:
            print(name)
            obs=self.observados[name]
            filtro_mes=obs.resample('MS').agg(pd.Series.sum,skipna=False)
            obs=obs.where(~filtro_mes.reindex(obs.index,method='ffill').isna())
            lat=coords.loc[coords['nombre']==name]['lat'].values[0]
            lon=coords.loc[coords['nombre']==name]['lon'].values[0]
            obs=obs.to_xarray()
            obs=obs.rename({'index':'time'})
            if acu==True:
                obs=obs.resample(time='MS').sum('time',skipna=False)
            else:
                obs=obs.resample(time='MS').mean('time',skipna=False)
            #print(obs)
            modelos=self.modelos.interp(lat=lat,lon=lon)
            modelos=modelos.drop(['lat','lon'])
            #print(lat,lon)
            #print(modelos)
            proyecciones=self.proyecciones.interp(lat=lat,lon=lon)
            proyecciones=proyecciones.drop(['lat','lon'])
            #print(proyecciones)
            iter_time=[1,2,3,4,5,6,7,8,9,10,11,12]
            e_fc=obs.groupby('time.month').mean('time')
            for i in iter_time:
                gg=obs.loc[obs['time.month']==i]
                n=gg['time'].shape[0]
                gg['time']=np.arange(1,n+1)
                xstd=gg['time'].std()
                xmean=gg['time'].mean()
                ymean=gg.mean(dim='time')
                cov=((gg['time']-xmean)*(gg-ymean)).mean('time')
                slope=cov/(xstd**2)
                intercept = ymean-xmean*slope
                trend=gg['time']*slope+intercept
                detrended=gg-trend
                detrended_rol=detrended.rolling(time=10,min_periods=2).mean()
                detrended_rol_max=detrended_rol.max('time')
                detrended_rol_min=detrended_rol.min('time')
                if i==2:
                    print(detrended_rol,detrended_rol_max,detrended_rol_min)
                detrended_rol_range=detrended_rol_max-detrended_rol_min
                e_fc.loc[e_fc['month']==i]=detrended_rol_range
            #-------------------------------------------------
            obs_guardar=obs
            modelos_guardar=modelos
            proyecciones_guardar=proyecciones
            #-----------------------------------------------
            obs=obs.groupby('time.month').mean('time')
            modelos=modelos.groupby('time.month').mean('time')
            proyecciones=proyecciones.groupby('time.month').mean('time')
            bias_mod=abs(modelos-obs)
            bias_mod=bias_mod.where(~(bias_mod<0.01),0.01)#PARA EVITAR INFINITOS
            r_bias=e_fc/bias_mod
            r_bias=r_bias.where(bias_mod>e_fc,1)
            distance_mod=proyecciones-modelos
            distance_mean=distance_mod.mean('modelo')
            #_-------------------------------------------------
            for i in range(11):
                if i==0:
                    distance=abs(distance_mod-distance_mean)
                else:
                    distance=abs(distance_mod-rea_change)
                distance=distance.where(~(distance<0.01),0.01)#PARA EVITAR INFINITOS
                r_converg=e_fc/distance
                r_converg=r_converg.where(distance>e_fc,1)
                r_fc=r_bias*r_converg
                r_fc=r_fc.where(~(r_fc<0.01),0.01)#PARA EVITAR INFINITOS
                rea_change=(r_fc*distance_mod).sum('modelo')/r_fc.sum('modelo')
                rango_incertidumbre=(((r_fc*(distance_mod-rea_change)**2).sum('modelo')/r_fc.sum('modelo'))**0.5)*2
                #print(rea_change[:,30,30].values[6:12])
            #-----------------------------------------------------------
            serie_rea=((r_fc*proyecciones_guardar.groupby('time.month')).sum('modelo')).groupby('time.month')/r_fc.sum('modelo')#---2
            #serie_rea.to_netcdf('serie_rea_'+var+'.nc')#------------2
            #---------------------------------------------------------------
            serie_incertidumbre=(((r_fc*((proyecciones_guardar-serie_rea)**2).groupby('time.month').mean('time')).sum('modelo')/r_fc.sum('modelo'))**0.5)*2
            #rango_incertidumbre=(((r_fc*(distance_mod-rea_change)**2).sum('modelo')/r_fc.sum('modelo'))**0.5)*2
            cnj_obs.loc[:,name]=obs_guardar.to_dataframe(name=name).iloc[:,0]
            cnj_mod.loc[:,name]=modelos_guardar.to_dataframe(name=name).iloc[:,0]
            cnj_pro.loc[:,name]=proyecciones_guardar.to_dataframe(name=name).iloc[:,0]
            cnj_rea.loc[:,name]=rea_change.to_dataframe(name=name).iloc[:,0]
            cnj_cambios.loc[:,name]=distance_mod.to_dataframe(name=name).iloc[:,0]
            cnj_incertidumbre.loc[:,name]=rango_incertidumbre.to_dataframe(name=name).iloc[:,0]
            cnj_serie_rea.loc[:,name]=serie_rea.to_dataframe(name=name).iloc[:,0]
            cnj_r_fc.loc[:,name]=r_fc.to_dataframe(name=name).iloc[:,0]
        return convertido_e(cnj_obs,cnj_mod,cnj_pro,cnj_rea,cnj_incertidumbre,cnj_serie_rea,cnj_cambios,cnj_r_fc)
