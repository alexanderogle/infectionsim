import yaml
import numpy as np


def unload_inputs(input_file=None):
    # Validate
    assert input_file != None, 'Provide an input file.'
    suffix = input_file.split('.')[-1]
    assert suffix == 'yaml', 'Invalid input file type. Should be ".yaml".'
    with open('model_params.yaml') as _inputs:
        inputs = yaml.load(_inputs, Loader=yaml.FullLoader)

    # TODO: Validate all keys are present and that values are of the
    #       correct type.

    return inputs


def set_defaults(inputs):
    _defaults = {
        'read_in_data': False,
        'path_in': '',
        'write_out_data': True,
        'path_out': 'data',
        'seed_num': np.random.randint(1, high=10000),
        'population_name': 'cityville',
        'population': 10000,
        'connection_min': 1,
        'connection_max': 15,
        'recovery_period': 14,
        'recovery_probability': 0.3,
        'death_probability': 0.01,
        'infection_probability': 0.03,
        'max_days': 80,
        'plot_results': False

    }

    for key, value in _defaults.items():
        if key not in inputs:
            inputs[key] = _defaults[key]

    return inputs


def validate_inputs(inputs):
    _types = {
        'read_in_data': bool,
        'path_in': str,
        'write_out_data': bool,
        'path_out': str,
        'seed_num': int,
        'population_name': str,
        'population': int,
        'connection_min': int,
        'connection_max': int,
        'recovery_period': int,
        'recovery_probability': float,
        'death_probability': float,
        'infection_probability': float,
        'max_days': int,
        'plot_results': bool

    }

    for key, value in inputs.items():
        assert type(value) == _types[key], '{} should be of type {} but got {}'.format(
            key, _types[key], value
        )

    return inputs


if __name__ == '__main__':
    inputs = unload_inputs(input_file='model_params.yaml')
    print(inputs)
#    with open('model_params.yaml') as inputs:
#        _inputs = yaml.load(inputs, Loader=yaml.FullLoader)
#
#    for key, value in _inputs.items():
#        print('{}: {}'.format(key, value))
