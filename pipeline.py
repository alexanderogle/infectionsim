import luigi
import os
import time
import pickle as pkl
from process_inputs import unload_inputs, set_defaults, validate_inputs
from model_engine import InfectionRun


class ReadInputs(luigi.Task):
    input_file = luigi.Parameter(default='None')
    run_id = int(time.time())
    path_target = os.path.join('.pipeline_data', str(run_id))
    target = os.path.join(path_target, 'read_inputs.pkl')

    def run(self):
        # Make pipeline_data dir if doesn't exist
        os.makedirs(os.path.join('.pipeline_data', str(self.run_id)), exist_ok=True)
        inputs = unload_inputs(input_file=self.input_file)

        with open(self.target, 'wb') as file_:
            pkl.dump(inputs, file_)

    def output(self):
        return luigi.LocalTarget(self.target)


class SetDefaults(luigi.Task):
    input_file = luigi.Parameter(default='None')
    path_target = ReadInputs.path_target
    target = os.path.join(path_target, 'set_defaults.pkl')

    def requires(self):
        return ReadInputs(input_file=self.input_file)

    def run(self):
        with open(ReadInputs.target, 'rb') as _file:
            inputs = pkl.load(_file)

        inputs = set_defaults(inputs)

#        self.target = os.path.join(
#            inputs['path_pipeline_data'],
#            inputs['run_id'],
#            'set_defaults.pkl'
#        )

        with open(self.target, 'wb') as file_:
            pkl.dump(inputs, file_)

    def output(self):
        return luigi.LocalTarget(self.target)


class ValidateInputs(luigi.Task):
    input_file = luigi.Parameter(default=None)
    target = '.pipeline_data/{}/read_inputs.pkl'

    def requires(self):
        return SetDefaults(input_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.target)

    def run(self):
        with open(SetDefaults.target, 'rb') as _file:
            inputs = pkl.load(_file)

        inputs = validate_inputs(inputs)
        self.target = self.target.format(inputs['run_id'])

        with open(self.target, 'wb') as file_:
            pkl.dump(inputs, file_)


class RunModel(luigi.Task):
    input_file = luigi.Parameter(default=None)
    target = '.pipeline_data/{}/read_inputs.pkl'

    def requires(self):
        return ValidateInputs(input_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.target)

    def run(self):
        self.target = self.target.format(ValidateInputs.inputs['run_id'])
        run = InfectionRun()
        run.setup_population()
        run.setup_network()
        run.run_model()

        with open(self.target, 'wb') as file_:
            pkl.dump(run, file_)
