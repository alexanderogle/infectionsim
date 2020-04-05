# New files:

- `model_params.yaml`:
    +  Default input file for model run
- `model_engine.py`:
    + Created a `InfectionRun` class for an instance run of Infection Sim.
        - These methods are an example draft for `luigi.Task` instances
    + Can execute with `python model_engine.py` from command line as well.
    + Uses `model_params.yaml`
- `pipeline.py`:
    + Functional `luigi` pipeline that consists of four tasks:
        - `ReadInputs`: Reads YAML file if one is provided.
        - `SetDefaults`: Sets default values for any missing parameters.
        - `ValidateInputs`: Validates that inputs passed are of proper type.
        - `RunModel`: Runs an instance of the model

# Submitting Luigi Task

Execute at command line:

    python -m luigi --module pipeline RunModel --RunModel-input-file model_params.yaml --local-scheduler

The pipeline data is stored in `.pipeline_data`, and if you want to rerun, that data will have to be deleted first, or else `luigi` will skip the previously completed tasks. (NOTE: Because of this, we should come up with a way to autogenerate a unique ID for each model run.)

# Run Model as Standalone Process

Execute at command line:

    python model_engine.py
