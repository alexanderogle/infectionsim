import luigi
import pickle as pkl
from read_yaml import unload_inputs
from model_engine import InfectionRun


class ReadInputs(luigi.Task):
    input_file = luigi.Parameter(default='model_params.yaml')

    def output(self):
        return luigi.LocalTarget('.pipeline_data/inputs.pkl')

    def run(self):
        inputs = unload_inputs(input_file=self.input_file)

        with open('.pipeline_data/inputs.pkl', 'wb') as file_:
            pkl.dump(inputs, file_)


class RunModel(luigi.Task):
    input_file = luigi.Parameter(default='model_params.yaml')

    def requires(self):
        return ReadInputs(input_file=self.input_file)

    def output(self):
        return luigi.LocalTarget('.pipeline_data/done.pkl')

    def run(self):
        run = InfectionRun()
        run.setup_population()
        run.setup_network()
        run.run_model()

        with open('.pipeline_data/done.pkl', 'wb') as file_:
            pkl.dump('Done.', file_)
