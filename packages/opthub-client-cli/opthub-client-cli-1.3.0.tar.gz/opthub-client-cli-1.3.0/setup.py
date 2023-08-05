# coding: utf-8

from setuptools import setup
import os

# Remove old config file to avoid incompatibility issues
config_path = os.path.expanduser('~/.opt.yml')
if os.path.exists(config_path):
    os.remove(config_path)

setup()
