# Copyright 2020 by Erick Alexis Alvarez Sanchez, The national meteorological and hydrological service of Peru (SENAMHI).
# All rights reserved.
# This file is part of the MEANpy package,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

class convertido(object):
    def __init__(self,rea,incertidumbre,r_fc,serie_rea_pro,serie_rea_his):
        self.rea=rea
        self.incertidumbre=incertidumbre
        self.serie_rea_historico=serie_rea_his
        self.serie_rea_proyectado=serie_rea_pro
        self.pesos_por_modelo=r_fc
    def plot(self):
        print('todavia no hay ploteos disponibles')

class convertido_e(object):
    def __init__(self,obs,mod,pro,rea,incertidumbre,serie_rea,cambios,pesos):
        self.obs=obs
        self.mod=mod
        self.pro=pro
        self.rea=rea
        self.incertidumbre=incertidumbre
        self.serie_rea=serie_rea
        self.cambios=cambios
        self.pesos=pesos
    def plot(self):
        print('todavia no hay ploteos disponibles')
