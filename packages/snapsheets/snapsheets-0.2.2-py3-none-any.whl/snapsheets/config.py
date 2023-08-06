"""
snapsheets.config.py
"""
from pathlib import Path
import yaml

_config = "Run set_default_config() first"


def get_config():
    """
    Return config

    Returns
    -------
    dict
        current config
    """
    return _config


def set_config(fname):
    """
    Set config

    Parameters
    ----------
    fname : str
        filename of config in yaml format

    Returns
    -------
    dict
        config
    """
    with open(fname, "r") as f:
        config = yaml.safe_load(f)
    return config


def set_default_config():
    """
    Set default config

    Returns
    -------
    dict
        config
    """
    here = Path(__file__).resolve().parent
    fname = here / "config.yml"
    return set_config(fname)


def add_config(fname):
    """
    Update config

    Parameters
    ----------
    fname : str
        filename of config in yaml format

    Returns
    -------
    dict
        updated config
    """
    config = get_config()
    add = set_config(fname)
    config.update(add)
    return config


def show_config():
    """
    Show config
    """
    import pprint

    config = get_config()
    pprint.pprint(config)
    return


def volumes():
    """
    List volumes

    Returns
    -------
    dict
        list of volumes
    """
    config = get_config()
    return config.get("volumes")


def options():
    """
    List options

    Returns
    -------
    dict
        list of options
    """
    config = get_config()
    return config.get("options")


def sheets():
    """
    List spreadsheets

    Returns
    -------
    list
        list of spreadsheets
    """
    config = get_config()
    return list(config.get("sheets").keys())


def sheet(name):
    """
    Show spreadsheet info

    Parameters
    ----------
    name : str
        name of spreadsheet

    Returns
    -------
    dict
        spreadsheet info
    """
    config = get_config()
    return config.get("sheets").get(name)


## Set default config
_config = set_default_config()
