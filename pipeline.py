import luigi
import pickle as pkl
from process_inputs import unload_inputs, set_defaults, validate_inputs
from model_engine import InfectionRun


class ReadInputs(luigi.Task):
    input_file = luigi.Parameter(default=None)
    target = '.pipeline_data/read_inputs.pkl'

    def output(self):
        return luigi.LocalTarget(self.target)

    def run(self):
        inputs = unload_inputs(input_file=self.input_file)

        with open(self.target, 'wb') as file_:
            pkl.dump(inputs, file_)


class SetDefaults(luigi.Task):
    input_file = luigi.Parameter(default=None)
    target = '.pipeline_data/set_defaults.pkl'

    def requires(self):
        return ReadInputs(input_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.target)

    def run(self):
        with open(ReadInputs.target, 'rb') as _file:
            inputs = pkl.load(_file)

        inputs = set_defaults(inputs)

        with open(self.target, 'wb') as file_:
            pkl.dump(inputs, file_)


class ValidateInputs(luigi.Task):
    input_file = luigi.Parameter(default=None)
    target = '.pipeline_data/validate_inputs.pkl'

    def requires(self):
        return SetDefaults(input_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.target)

    def run(self):
        with open(SetDefaults.target, 'rb') as _file:
            inputs = pkl.load(_file)

        inputs = validate_inputs(inputs)

        with open(self.target, 'wb') as file_:
            pkl.dump(inputs, file_)


class RunModel(luigi.Task):
    input_file = luigi.Parameter(default=None)
    target = '.pipeline_data/run_model.pkl'

    def requires(self):
        return ValidateInputs(input_file=self.input_file)

    def output(self):
        return luigi.LocalTarget(self.target)

    def run(self):
        run = InfectionRun()
        run.setup_population()
        run.setup_network()
        run.run_model()

        with open(self.target, 'wb') as file_:
            pkl.dump(run, file_)
