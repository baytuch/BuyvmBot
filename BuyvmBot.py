#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import sys
import json
from time import sleep
from BuyvmAPI import *


class BuyvmBot:

  data_dir = 'data'
  conf_name = 'config.json'
  app_name = 'BuyvmBot'
  app_ver = '0.1'

  conf_status = False
  conf_data = {}
  buyvm = None

  def __init__(self):
    print('Init')
    self.conf_load()
    if (self.conf_status):
      print('-> ok')
      user_agent = self.app_name + '/' + self.app_ver
      self.buyvm = BuyvmAPI(self.conf_data['api']['key'],
                            self.conf_data['api']['hash'],
                            self.data_dir,
                            user_agent,
                            self.conf_data['site'])
      self.buyvm.get_info()
    else:
      print('-> error')

  def conf_load(self):
    conf_path = self.data_dir + '/' + self.conf_name
    try:
      fd = open(conf_path, 'r')
      read_data = fd.read()
      self.conf_data = json.loads(read_data)
      fd.close()
      self.conf_status = True
    except Exception as e:
      self.conf_data = {}
      self.conf_status = False
      print('Config load error: ' + str(e))

if __name__ == '__main__':
  bot = BuyvmBot()

