import logging
import logging.config
import yaml


class SimfectionLogger:
    def __init__(self, name=None):
        # Config and init logger
        with open('logger.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        if name == '__main__':
            logger = logging.getLogger('simfection')
        else:
            logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        self.logger = logger

    def get_logger(self):
        return self.logger
