# Running a Connections Engine Experiment

## Set Up Local Environment
1. Change into the `infection_simulation` directory.
2. Check out the develop branch with `git checkout develop`.
3. Change into the `experiments/connection_engine` directory.

## Submitting a Job

**NOTE:**
- It is best to run the experiment in a TMUX window so that you can close your connection and come back to it later. See TMUX Tutorial for instructions on doing that.

## Determine Parameters

- To see what parameters are available, and their respecitve flags, execute the following:

      python3.7 connections_experiment.py --help

- You should see the following:

```shell
usage: connections_experiment.py [-h] [-np NUM_PEOPLE [NUM_PEOPLE ...]]
                                 [-mc MEAN_CONNECTIONS [MEAN_CONNECTIONS ...]]
                                 [-sd STD] [-s SIZE] [-nr NUM_RUNS]

optional arguments:
  -h, --help            show this help message and exit
  -np NUM_PEOPLE [NUM_PEOPLE ...], --num_people NUM_PEOPLE [NUM_PEOPLE ...]
                        single value or list for number of people
  -mc MEAN_CONNECTIONS [MEAN_CONNECTIONS ...], --mean_connections MEAN_CONNECTIONS [MEAN_CONNECTIONS ...]
                        single value or list for nmean umber of connections
  -sd STD, --std STD    standard deviation for connection distribution
  -s SIZE, --size SIZE  sample size for connection distribution
  -nr NUM_RUNS, --num_runs NUM_RUNS
                        number of times to iterate over
                        (num_people,num_connections) pairs
```

### Parameter Descriptions

| Parameter | Description | Default | Max |
|:-:|---|:-:|---|
| `num_people` | the number of people in the | 100| 10000 |
| `mean_connections` | the average number of connections | 10 |  100 |
|`std` | the standard deviation for the number of connections distribution | 10 | None |
|`size`| the sample size from which number of connections are chosen | 1000000 | None |
|`num_runs`| the number of times to iterate experiment | 3 | 5 |
**NOTE:**
- For each of the `num_people` and `mean_connections` parameters, you can pass a list of values. The experiment engine will automatically run all pairs.
- The max values are suggestions to keep runtimes manageable.


## Run Experiment

Say you decided that you want to run an experiment for the following:
- `num_people = [200,300,400]`
- `mean_connections = [10,20,30]`
- `num_runs = 2`

Execute the following:

    python3.7 connections_experiment.py \
    --num_people 200 300 400 \
    --mean_connections 10 20 30 \
    --num_runs 2 
    
  You can also use the short-hand version of the flags:
  
    python3.7 connections_experiment.py \
    -np 200 300 400 \
    -mc 10 20 30 \
    -nr 2 
