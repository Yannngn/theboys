import logging

formatter = logging.Formatter("%(message)s")


def setup_logger(name: str, log_file: str, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(
        log_file,
        mode="w",
        encoding="utf-8",
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
