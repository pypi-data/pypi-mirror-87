import penvy.logger.colorlog as colorlog


def get_logger(name: str, level: int):
    logger = colorlog.getLogger(name)
    logger.setLevel(level)

    cformat = "%(log_color)s" + "%(asctime)s - %(message)s"
    formatter = colorlog.ColoredFormatter(cformat, "%H:%M:%S")

    ch = colorlog.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level)

    logger.handlers = [ch]

    return logger
