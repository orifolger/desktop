#! /usr/bin/python

import operator
import os
import random
import subprocess
import urllib

from gi.repository import Gio

SCHEMA = 'org.gnome.desktop.background'
KEY = 'picture-uri'
WALLPAPER_DIR = '/home/ori/Wallpaper'

def GetFiles(top_path):
  for root, dirs, files in os.walk(top_path):
    for name in files:
      yield os.path.join(root, name)


def GetDbusSessionBusAddress():
  gnome_session_pid = subprocess.check_output(['/usr/bin/pgrep','gnome-session'])
  # Remove \n suffix
  gnome_session_pid = gnome_session_pid[:-1]

  gnome_session_env_string = open('/proc/' + gnome_session_pid + '/environ').read()

  gnome_session_env = dict([operator.itemgetter(0,2)(item.partition('='))
                            for item in gnome_session_env_string.split('\0')])

  return gnome_session_env['DBUS_SESSION_BUS_ADDRESS']

def ChangeBackground(file_path):
  # Necessary for cron. See http://stackoverflow.com/a/19666729
  os.environ['DBUS_SESSION_BUS_ADDRESS'] = GetDbusSessionBusAddress()
  settings = Gio.Settings.new(SCHEMA)
  settings.set_string(KEY, 'file://' + urllib.quote(file_path))


images = list(GetFiles(WALLPAPER_DIR))
wallpaper = random.choice(images)
ChangeBackground(wallpaper)
