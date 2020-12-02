import logging
import os


def make_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-5.5s] [%(threadName)s]  %(message)s"
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def make_target_dir_from_path(abs_path):
    make_target_dir(os.path.dirname(abs_path))


def make_target_dir(target_dir):
    os.makedirs(target_dir, 0o0755, exist_ok=True)


def make_registration_decorator():
    """
    returns a (decorator, list). any function decorated with
    the returned decorator will be appended to the list
    """
    registered = []

    def _register(fn):
        registered.append(fn)
        return fn

    return _register, registered
