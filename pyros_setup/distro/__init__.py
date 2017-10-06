# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

"""
Forcing import from jade distro
"""

import os
import types
import sys

# Configuring logging default handler
import logging
_logger = logging.getLogger(__name__)

from pyros_setup.common.utils import deprecated
from pyros_config import ConfigHandler


# This field has to be set before importing this :
from pyros_setup import distro, distro_path


_config_handler = ConfigHandler(
                __name__,
                instance_path=None,
                instance_relative_config=False,
                root_path=os.path.join(distro_path, '/etc'),
                default_config={
                    'WORKSPACES': [],
                },
            )


def configure(distro, config=None):
    """
    load configuration
    :param config:
        if string, it is assumed to be a path to a python configuration file
        else if dict, it is assumed to directly contain the configuration settings
        otherwise the object passed will be introspected to attempt to set the configuration settings.
    :return: self
    """
    config = config or 'workspaces.pyros.cfg'

    _config_handler.configure_file(config=config, create_if_missing="""
# default configuration generated by pyros_setup.distro
# Usage from python :
# import pyros_setup
# pyros_setup.configure().activate()
#
# Fill in your workspaces here, if you want pyros_setup to dynamically import ROS packages from it.
WORKSPACES=[]
""")


def show_config():
    # TODO improve this...
    print(_config_handler)
    print("import name: {0}".format(_config_handler.import_name))
    print("root path: {0}".format(_config_handler.root_path))
    print("instance path: {0}".format(_config_handler.instance_path))
    print("config: {0}".format(_config_handler.config))



# TODO : add "is ROS setup.bash sourced?" check method
# to allow client to raise ImportError directly instead of attempting emulation.

def activate():
    """
    Activate import relay (via setting sys.modules[])
    """

    # TODO : put that in context to allow deactivation... ( but HOWTO mix deactivation with module import ?)

    # The actual trick
    _logger.warning("Dynamic PyROS setup starting...")
    from pyros_setup.common.ros_setup import ROS_emulate_setup
    # we want this to except in case of bad config, because default_config has to have these fields.
    ROS_emulate_setup(distro, *_config_handler.config['WORKSPACES'])

    # Main relay
    # CAREFUL this doesn't work sometimes (had problem when using from celery bootstep...)
    # sys.modules[self.config_handler.import_name] = self

    _logger.warning("Dynamic PyROS setup done.")



# TODO : activate_import : use ros_importer to allow importing from ros modules
# but only importing python module, it is not a full setup like activate().
# It is much cleaner and the only necessary setup in many cases...

__all__ = [
    '__version__',
    'deprecated',
    'configure',
    'activate',
]
