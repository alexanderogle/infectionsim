import logging
import logging.config
import yaml


class SimfectionLogger:
    def __init__(self):
        # Config and init logger
        with open('logger.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logger = logging.getLogger('simfection')
        logger.setLevel(logging.DEBUG)
        self.logger = logger

    def get_logger(self):
        return self.logger
