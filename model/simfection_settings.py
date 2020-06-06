class SimFectionSettings:

    default_settings = {
        # Pathogen settings
        'infection_rate': 0.4,
        'recovery_rate': 0.1,
        'death_rate': 0.00,
        'spontaneous_rate': 0.0,
        'testing_accuracy': None,
        'immunity_period': 10**2,
        'contagious_period': 99,
        'incubation_period': 0,
        'pathogen_keys': [
            'infection_rate',
            'recovery_rate',
            'death_rate',
            'spontaneous_rate',
            'testing_accuracy',
            'immunity_period',
            'contagious_period',
            'incubation_period',
        ],
        # PopulationEngine settings
        'num_people': 100,
        'initial_states': {'inf': 0.2},
        # ConnectionEngine settings
        'mean_connections': 10,
        'std': 10,
        'size': 10**5,
        'experiment': False,
        # SimulationRun settings
        'num_days': 15,
        'verbose': False,
        'previous_run': None,
    }

    def __init__(self, settings=None):
        self.settings = self.default_settings
        # Set custom settings
        if settings is not None:
            for key, value in settings.items():
                self.set_setting(key, value)

    def get_setting(self, setting: str):
        if setting not in self.settings.keys():
            print('Setting "{}" not found.'.format(setting))
            return None
        return self.settings[setting]

    def set_setting(self, setting: str, value: Any):
        if setting not in self.settings.keys():
            print('Setting "{}" not found.'.format(setting))
            return None
        self.settings[setting] = value
        return value
