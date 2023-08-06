"""TLCPack sphinx add on"""
import os

__version__ = "0.1.2"

__BASEDIR__ = os.path.dirname(os.path.realpath(os.path.expanduser(__file__)))


def get_static_path():
    """Get list of static path"""
    return os.path.join(__BASEDIR__, "_static")


def get_templates_path():
    """Get list of templates path"""
    return os.path.join(__BASEDIR__, "_templates")
