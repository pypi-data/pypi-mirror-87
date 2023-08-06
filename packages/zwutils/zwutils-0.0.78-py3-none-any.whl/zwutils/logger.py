import os
import json
import logging
import logging.config
from pathlib import Path

def logger(name=__name__, cfg=None, filesuffix=None):
    '''Get logger with name'''
    cfg = cfg  or 'conf/log.json'
    if os.path.exists(cfg):
        with open(cfg, 'r') as f:
            config = json.load(f)
            handlers = config['handlers']
            # create parent dir if needed
            for h,o in handlers.items():
                if 'filename' in o and not Path(o['filename']).parent.exists():
                    Path(o['filename']).parent.mkdir(parents=True, exist_ok=True)
            # add filename suffix is needed
            if filesuffix and handlers['logfile']:
                logpath = Path(handlers['logfile']['filename'])
                logpath = logpath.parent / ('%s_%s%s'%(logpath.stem, filesuffix, logpath.suffix))
                handlers['logfile']['filename'] = str(logpath)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    return logger
