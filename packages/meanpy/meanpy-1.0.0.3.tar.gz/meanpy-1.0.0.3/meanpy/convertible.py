# Copyright 2020 by Erick Alexis Alvarez Sanchez, The national meteorological and hydrological service of Peru (SENAMHI).
# All rights reserved.
# This file is part of the MEANpy package,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import xarray as xray
import numpy as np
from .ploteos import convertido

class pre_rea(object):
    def __init__(self,obs,mod,pro,anual=False):
        self.observados=obs
        self.modelos=mod
        self.proyecciones=pro
        self.anual=anual
    def rea_perform(self,anual=self.anual):
        obs=self.observados
        modelos=self.modelos
        proyecciones=self.proyecciones
        if anual==True:
            iter_time=[1]
        else:
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
            detrended_rol=detrended.rolling(time=10).mean()
            detrended_rol_max=detrended_rol.max('time')
            detrended_rol_min=detrended_rol.min('time')
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
            #print(rea_change[:,30,30].values[6:12])
        #-----------------------------------------------------------
        serie_rea_his=((r_fc*modelos_guardar.groupby('time.month')).sum('modelo')).groupby('time.month')/r_fc.sum('modelo')
        serie_rea_pro=((r_fc*proyecciones_guardar.groupby('time.month')).sum('modelo')).groupby('time.month')/r_fc.sum('modelo')#---2
        #serie_rea.to_netcdf('serie_rea_'+var+'.nc')#------------2
        #---------------------------------------------------------------
        #serie_incertidumbre=(((r_fc*((proyecciones_guardar-serie_rea)**2).groupby('time.month').mean('time')).sum('modelo')/r_fc.sum('modelo'))**0.5)*2
        rango_incertidumbre=(((r_fc*(distance_mod-rea_change)**2).sum('modelo')/r_fc.sum('modelo'))**0.5)*2
        return convertido(rea_change,rango_incertidumbre,r_fc,serie_rea_pro,serie_rea_his)
