#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Isit help you to guess your runtime environment in order
to adapt your software in consequences."""
import os
import sys
import platform
import struct
import datetime
from subprocess import Popen
from subprocess import PIPE as _PIPE

if sys.version < '3':
  import codecs
  def _u(x):
    return codecs.unicode_escape_decode(x)[0]
else:
  def _u(x):
    return x

__version__ = '0.3.6'

##########
# Python #
##########
py2 = (sys.version_info[0] == 2)
py3 = (sys.version_info[0] == 3)
py30 = (py3 and sys.version_info[1] == 0)
py31 = (py3 and sys.version_info[1] == 1)
py32 = (py3 and sys.version_info[1] == 2)
py33 = (py3 and sys.version_info[1] == 3)
py34 = (py3 and sys.version_info[1] == 4)
py27 = (py2 and sys.version_info[1] == 7)
py26 = (py2 and sys.version_info[1] == 6)
py25 = (py2 and sys.version_info[1] == 5)
py24 = (py2 and sys.version_info[1] == 4)

if py24 or py25:
  cpython = False
  pypy = ('pypy' in sys.version.lower())
  jython = ('java' in sys.version.lower())
  ironpython = ('iron' in sys.version.lower())
  if not pypy and not jython and not ironpython:
    cpython = True
else:
  pypy = ('pypy' in platform.python_implementation().lower())
  jython = ('jython' in platform.python_implementation().lower())
  ironpython = ('ironpython' in platform.python_implementation().lower())
  cpython = ('cpython' in platform.python_implementation().lower())

########
# Arch #
########
bit32 = struct.calcsize('P') * 8 == 32
bit64 = struct.calcsize('P') * 8 == 64
sparc = platform.processor() == "sparc"

##############
# Endianness #
##############
little_endian = sys.byteorder == 'little'
big_endian = sys.byteorder == 'big'

######
# Os #
######
# Linux
linux = platform.system().lower() == 'linux'
linux_version = None
linux2 = False
linux3 = False
if linux:
  if py3:
    from subprocess import getoutput
    linux_version = _u(getoutput('uname -r'))
  else:
    linux_version = _u(Popen('uname -r', stdout=_PIPE, stderr=_PIPE, shell=True).stdout.read()[:-1])
  linux2 = '2' in linux_version[0]
  linux3 = '3' in linux_version[0]
# Osx
osx = platform.system().lower() == 'darwin'
osx_version = None
if osx:
  osx_version = _u(platform.mac_ver()[0])
# Windows
windows = ('win32' in str(sys.platform).lower())
# Other
hpux = ('hpux' in str(sys.platform).lower()) or ('hp-ux' in str(sys.platform).lower())
solaris = ('sunos' in str(sys.platform).lower())

#################
# Distributions #
#################
# Linux Mint
linuxmint = False
linuxmint_version = None
linuxmint_codename = None
if os.path.exists('/etc/lsb-release'):
  _lsb_release_file = open('/etc/lsb-release')
  _lsb_release_lines = [_line.replace('\n', '') for _line in _lsb_release_file.readlines()]
  _lsb_release_file.close()
  linuxmint = 'linuxmint' in _lsb_release_lines[0].lower()
if linuxmint:
  linuxmint_version = _u((_lsb_release_lines[1].split('=')[-1].replace('"', '')))
  linuxmint_codename =  _lsb_release_lines[2].split('=')[-1]
# ElementaryOS
elementaryos = False
elementaryos_version = None
elementaryos_release = None
elementaryos_codename = None
if os.path.exists('/etc/lsb-release'):
  _lsb_release_file = open('/etc/lsb-release')
  _lsb_release_lines = [_line.replace('\n', '') for _line in _lsb_release_file.readlines()]
  _lsb_release_file.close()
  elementaryos = 'elementary os' in _lsb_release_lines[0].lower()
if elementaryos:
  elementaryos_version = _u((_lsb_release_lines[1].split('=')[-1]))
  elementaryos_version = _u('.'.join(elementaryos_version.split('.')[:2]))
  if len(_lsb_release_lines[1].split('=')[-1].split('.')) == 3:
    elementaryos_release = _u(_lsb_release_lines[1].split('=')[-1].split('.')[2])
  elementaryos_codename = _u(_lsb_release_lines[2].split('=')[1])
# Ubuntu
ubuntu = False
ubuntu_version = None
ubuntu_release = None
ubuntu_lts = None
ubuntu_codename = None
if os.path.exists('/etc/lsb-release'):
  _lsb_release_file = open('/etc/lsb-release')
  _lsb_release_lines = [_line.replace('\n', '') for _line in _lsb_release_file.readlines()]
  _lsb_release_file.close()
  ubuntu = 'ubuntu' in _lsb_release_lines[0].lower()
if ubuntu:
  _ubuntu_version = _u((_lsb_release_lines[3].split('=')[-1].split(' ')[1].replace('"', '')))
  ubuntu_version = _u('.'.join(_ubuntu_version.split('.')[:2]))
  if len(_lsb_release_lines[3].split('=')[-1].split(' ')[1].split('.')) == 3:
    ubuntu_release = _u(_lsb_release_lines[3].split('=')[-1].split(' ')[1].split('.')[2])
  ubuntu_lts = _ubuntu_version.split('.')[1] == "04"
  ubuntu_codename = _u(_lsb_release_lines[2].split('=')[1])
# Debian
debian = os.path.exists('/etc/debian_version') and not ubuntu
debian_version = None
debian_release = None
if debian:
  _debian_version_file = open('/etc/debian_version')
  _debian_version_lines = [_line.replace('\n', '') for _line in _debian_version_file.readlines()]
  _debian_version_file.close()
  debian_version = _u(_debian_version_lines[0])
  debian_release = _u(debian_version.split('.')[-1])
# Archlinux
archlinux = os.path.exists('/etc/arch-release')
archlinux_version = None
archlinux_release = None
# Centos
centos = 'centos' in platform.dist()[0].lower()
centos_version = None
centos_release = None
if centos:
  centos_version = _u(platform.dist()[1].split('.')[0])
  centos_release = _u(platform.dist()[1].split('.')[-1])
# Redhat
redhat = 'redhat' in platform.dist()[0].lower()
redhat_version = None
redhat_release = None
if redhat:
  redhat_version = _u(platform.dist()[1].split('.')[0])
  redhat_release = _u(platform.dist()[1].split('.')[-1])
# Solaris
if solaris:
  solaris_version = platform.release()

#######
# Env #
#######
home = os.path.expanduser("~") == os.getcwd() or False
virtualenv = hasattr(sys, 'real_prefix')
newrelic = 'newrelic' in sys.modules or False
heroku = os.environ.get('PYTHONHOME') == "/app/.heroku/python" or False
in_git = '.git' in os.listdir('.')

############
# Packages #
############
package_deb = ubuntu or debian
package_rpm = centos or redhat
package_pkg = solaris

########
# Date #
########
_now = datetime.datetime.now()
# Weekdays
monday = _now.isoweekday() == 1 or False
tuesday = _now.isoweekday() == 2 or False
wednesday = _now.isoweekday() == 3 or False
thursday = _now.isoweekday() == 4 or False
friday = _now.isoweekday() == 5 or False
saturday = _now.isoweekday() == 6 or False
sunday = _now.isoweekday() == 7 or False
# Months
january = _now.month == 1 or False
february = _now.month == 2 or False
march = _now.month == 3 or False
april = _now.month == 4 or False
may = _now.month == 5 or False
june = _now.month == 6 or False
july = _now.month == 7 or False
august = _now.month == 8 or False
september = _now.month == 9 or False
october = _now.month == 10 or False
november = _now.month == 11 or False
december = _now.month == 12 or False
# Seasons
winter = (december or january or february) or False
spring = (march or april or may) or False
summer = (june or july or august) or False
autumn = (september or october or november) or False
# Others
weekend = (saturday or sunday) or False
