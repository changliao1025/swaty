import os,stat
import sys
import glob
import shutil

import numpy as np
from pathlib import Path
import tarfile
import subprocess
from shutil import copyfile
from abc import ABCMeta, abstractmethod
import datetime
from shutil import copy2
import json
from json import JSONEncoder
from swaty.classes.swatpara import swatpara


class pyhru(object):
    __metaclass__ = ABCMeta

    lIndex=-1
    nSoil_layer = 1
    

    def  __init__(self):
        return