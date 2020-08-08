#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import os.path
from urlparse import urlparse
import ssl
import urllib
import httplib


class BuyvmAPI:

  conn_timeout = 15
  default_user_agent = 'BuyvmAPI/1.0 (+https://ircnow.org)'
  api_path = 'https://manage.buyvm.net/api/client/command.php'
  ca_cert_file = 'cacert.pem'

  api_key = ''
  api_hash = ''
  user_agent = ''
  data_dir = ''
  conn_status = False
  ssl_cx = None

  def __init__(self, api_key, api_hash, data_dir, user_agent = '', bot_site = ''):
    self.api_key = api_key
    self.api_hash = api_hash
    self.data_dir = data_dir
    if (user_agent != '' and bot_site != ''):
      self.user_agent = user_agent + ' (+' + bot_site + ')'
    else:
      self.user_agent = self.default_user_agent
    self.create_ssl_context()

  def create_ssl_context(self):
    ca_cert_path = self.data_dir + '/' + self.ca_cert_file
    if (os.path.exists(ca_cert_path)):
      protocol = ssl.PROTOCOL_SSLv23
      self.ssl_cx = ssl.SSLContext(protocol)
      self.ssl_cx.verify_mode = ssl.CERT_REQUIRED
      self.ssl_cx.load_verify_locations(cafile=ca_cert_path)

  def client(self, data):
    self.resp_body = ''
    headers = {'User-Agent': self.user_agent}
    conn = None
    url_obj = urlparse(self.api_path)
    try:
      if (url_obj.scheme == 'https'):
        conn = httplib.HTTPSConnection(url_obj.hostname,
                                       timeout=self.conn_timeout,
                                       context = self.ssl_cx)
      else:
        conn = httplib.HTTPConnection(url_obj.hostname,
                                      timeout=self.conn_timeout)
      conn.request('GET',
                   url_obj.path + '?' + urllib.urlencode(data),
                   '',
                   headers)
      resp = conn.getresponse()
      if (resp.status == 200):
        self.resp_body = resp.read()
        self.conn_status = True
      resp.close()
    except Exception as e:
      self.conn_status = False
      print('BuyvmAPI error: ' + str(e))

  def get_info(self):
    data = {
                 'key': self.api_key,
                 'hash': self.api_hash,
                 'action': 'info',
                 'bw': 'true',
                 'ipaddr': 'true',
                 'status': 'true'}
    self.client(data)
    if (self.conn_status):
      print(self.resp_body)  

