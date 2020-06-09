# TODO(aogle): Implement the following for execution time, CPU utilization, and memory profiling:
# https://stackoverflow.com/questions/13507205/finding-memory-usage-cpu-utilization-execution-time-for-running-a-python-scrip

import cProfile
import pstats, math
import os
import io
import pandas as pd

from timing_test import TimingTest
 
test = TimingTest(runs=2, pop_size=1000, cpp=True)
pr = cProfile.Profile()
pr.enable()
test.run_test()
pr.disable()
 
result = io.StringIO()

pstats.Stats(pr,stream=result).sort_stats('cumulative').print_stats()
result=result.getvalue()
# chop the string into a csv-like buffer
result='ncalls'+result.split('ncalls')[-1]
result='\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])
# save it to disk

# Make sure the results folder exists
results_dir = './results/'
if(not os.path.isdir(results_dir)):
    os.mkdir('./results/')
with open('./results/test.csv', 'w+') as f:
    #f=open(result.rsplit('.')[0]+'.csv','w')
    f.write(result)
    f.close()