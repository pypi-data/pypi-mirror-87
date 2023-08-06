import os
import shutil
from .loghelper import LOG_INFO

def get_config_template(framework):
    """get config template"""
    template = framework + "_config.py"
    path = os.path.join(os.path.dirname(__file__), template)
    assert os.path.exists(path), "{} is not supported".format(framework)
    shutil.copy(path, "./")
    cwd = os.getcwd()
    LOG_INFO("{} is located in {}".format(template, cwd))
