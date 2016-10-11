#! /usr/bin/python

import requests
import sys
from st2actions.runners.pythonrunner import Action

from lib.vadc import Vtm

class VtmGetPoolNodes(Action):

  def run(self, vtm, name):

    vtm = Vtm(self.config, self.logger, vtm)
    result = vtm.getPoolNodes(name)
    return result
