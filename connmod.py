#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:47:41 2020

@author: jmurray
"""
# connection model function
# return number of connections/(person*day)
# parameters: population density (popdens), interaction area (intarea)
# interaction area = 12 ft wide by distance walked in one day
# average steps walked is ~4800 steps
#   Althoff, T., Sosič, R., Hicks, J. et al. Large-scale physical activity 
#   data reveal worldwide activity inequality. Nature 547, 336–339 (2017). 
#   https://doi.org/10.1038/nature23018
# average distance is ~2.2 miles (based on a 2.5 ft stride and the # of steps above)
# interaction area is units of square miles 
# 0.005 mi^2=12ft*2.2mi*1mi/5280ft
# population density numbers (people/mi^2)
# NYC:270,000; San Fran: 17,000; Chicago: 12,000; Ketchikan: 2,300
#   https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population_density
#   based on 2010 census
# later: demographics, social distancing and policy modifications
# UPDATE 4.30 - changed input to average number of steps (avdist) & 
#               interaction distance (intdist)
#               where the interaction distance is the maximum distance between
#               a susceptible individual and an infected one with a 
#               chance of transmission - currently this assumption is 6ft = 
def connmod(popdens,avdist,intdist):
    intarea = avdist*intdist
    numconn = intarea*popdens
    return round(numconn)
