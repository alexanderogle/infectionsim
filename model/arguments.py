import argparse
from settings import SimfectionSettings

settings = SimfectionSettings()


def _get_parser(arguments):
    parser = argparse.ArgumentParser()
    for names, args in arguments.items():
        parser.add_argument(*names, **args)
    return parser


simfection_args = {
    ('-nd', '--num-days'): {
        'help': (
            'number of days to simulate (default: {})'
            .format(settings.get_setting('num_days'))
        ),
        'type': int,
        'required': False
    },
    ('-bp', '--base-path'): {
        'help': (
            'base path for simfection run (default: {})'
            .format(settings.get_setting('base_path'))
        ),
        'type': str,
        'required': False
    },
    # TODO Make previous run setting a path and load restart instance
    ('-v', '--verbose'): {
        'help': (
            'whether or not to print extra info to stream (default: {})'
            .format(settings.get_setting('verbose'))
        ),
        'type': ,
        'required': False
    },
    ('-np', '--num-people'): {
        'help': (
            'how many people tp simulation in population (default: {})'
            .format(settings.get_setting('num_people'))
        ),
        'type': int,
        'required': False
    },
    ('-if', '--initial_infected'): {
        'help': (
            'ratio of population that is initiall infected (default: {})'
            .format(settings.get_setting('initial_states')['inf'])
        ),
        'type': float,
        'required': False
    },
    ('-ir', '--infection-rate'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('infection_rate'))
        ),
        'type': float,
        'required': False
    },
    ('-rr', '--recovery-rate'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('recovery_rate'))
        ),
        'type': float,
        'required': False
    },
    ('-dr', '--death-rate'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('death_rate'))
        ),
        'type': float,
        'required': False
    },
    ('-sr', '--spontaneous-rate'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('spontaneous_rate'))
        ),
        'type': float,
        'required': False
    },
    ('-ip', '--immunity-period'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('immunity_period'))
        ),
        'type': int,
        'required': False
    },
    ('-cr', '--contagious-period'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('contagious_period'))
        ),
        'type': int,
        'required': False
    },
    ('-ir', '--incubation-period'): {
        'help': (
            '(default: {})'
            .format(settings.get_setting('incubation_period'))
        ),
        'type': int,
        'required': False
    },

}
