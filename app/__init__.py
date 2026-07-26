from app.utils import config, logger


def log_setup(name):
    return logger.setup_logger(name, config.LOG_PATH, config.LOG_LEVEL)


__all__ = ["config", "log_setup"]
