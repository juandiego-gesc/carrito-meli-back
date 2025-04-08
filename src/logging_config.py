import logging.config
import os
from datetime import datetime

if not os.path.exists('logs'):
    os.makedirs('logs')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {  # Define a 'simple' formatter
            'format': '%(levelname)s: \t %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join('logs', f'app_{datetime.now().strftime("%Y_%m_%d")}.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # Use the 'simple' formatter
        },
    },
    'root': {
        'handlers': ['default', 'console'],
        'level': 'DEBUG',
        'propagate': True
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
