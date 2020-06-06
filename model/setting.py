

settings = {
    # Pathogen settings
    'infection_rate': 0.4,
    'recovery_rate': 0.1,
    'death_rate': 0.00,
    'spontaneous_rate': 0.0,
    'testing_accuracy': None,
    'immunity_period': 10**2,
    'contagious_period': 99,
    'incubation_period': 0
    # PopulationEngine settings
    'num_people': 100,
    'initial_states': {'inf': 0.2},
    # ConnectionEngine settings
    'mean_connections': 10,
    'std': 10,
    'size': 10**5,
    # SimulationRun settings
    'num_days': 15,
    'verbose': False,
    'previous_run': False,

}
