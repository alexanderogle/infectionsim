# New files:

- `model_params.yaml`:
    +  Default input file for model run
- `model_engine.py`:
    + Created a `InfectionRun` class for an instance run of Infection Sim.
        - These methods are an example draft for `luigi.Task` instances
    + Can execute with `python model_engine.py` from command line as well.
    + Uses `model_params.yaml`
- `pipeline.py`:
    + Functional `luigi` pipeline that consists of the following tasks:
        - `ReadInputs`: Reads YAML file if one is provided.
        -`SyncFromS3`: Sinks S3 bucket to local machine.
        - `SetDefaults`: Sets default values for any missing parameters.
        - `ValidateInputs`: Validates that inputs passed are of proper type.
        - `Model Engine`: Runs the model engine
        - `Run Model`: Run an instance of Infection Sim

# Submitting an InfectionSim Run

- Execute at command line using input file:

        python -m luigi --module pipeline RunModel [--input-file PATH-TO-INPUT-FILE]
        [--send-to-cloud] --local-scheduler

    - Optional Parameters:
        - `--input-file PATH-TO-INPUT-FILE`: Override default parameters with input file.
        - `--send-to-cloud`: Sync with S3 bucket before and after run.

The pipeline data is stored in `.pipeline_data`. Each run creates a unique `run_id` by using the time since epoch in seconds and the process ID both as `IntType`.
