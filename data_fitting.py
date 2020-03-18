#!/usr/local/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('https://covid.ourworldindata.org/data/full_data.csv')
usa = df.loc[df['location'] == 'United States'].sort_values('date')
date = range(0, len(usa['date']))

plt.plot(date, usa['total_cases'])
plt.show()
