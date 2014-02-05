#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['rosh_desktop_plugins'],
    package_dir={'': 'src'},
    requires=['genmsg', 'genpy', 'roslib', 'rospkg']
)

setup(**d)