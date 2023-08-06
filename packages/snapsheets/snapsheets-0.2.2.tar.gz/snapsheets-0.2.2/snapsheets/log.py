"""
snapsheets.log
"""

import logging
import logging.handlers


def chandler(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # create console handler with a INFO log level
    ch = logging.StreamHandler()
    # ch.setLevel(logging.INFO)
    ch.setLevel(level)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    logger.debug(f"ロガーを用意したよ : {name}")
    return logger


def fhandler(name):
    # logfile = cfg.get('logging').get('logfile')
    # maxbytes = cfg.get('logging').get('maxbytes')
    # backups = cfg.get('logging').get('backups')

    ## Set name of logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even DEBUG messages
    try:
        fh = logging.handlers.RotatingFileHandler(
            logfile, maxBytes=maxbytes, backupCount=backups
        )
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except FileNotFoundError as e:
        print(f"Error : ファイルを作ろう {logfile}")
        sys.exit()
    except:
        print("なにか変だよ")
        sys.exit()

    logger.info(f"Logger name = {name} @ {__file__}")
    return logger
