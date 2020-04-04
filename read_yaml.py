import yaml


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


if __name__ == '__main__':
    inputs = unload_inputs(input_file='model_params.yaml')
    print(inputs)
#    with open('model_params.yaml') as inputs:
#        _inputs = yaml.load(inputs, Loader=yaml.FullLoader)
#
#    for key, value in _inputs.items():
#        print('{}: {}'.format(key, value))
