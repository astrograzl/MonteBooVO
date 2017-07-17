#!python
# coding: utf-8
# @uthor: janak
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""

import os
import subprocess as sub
from time import time, strftime
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError


def coordination(name):
    """Get object coordination from Simbad database by the name"""
    try:
        coord = SkyCoord.from_name(name)
    except NameResolveError:
        return None
    else:
        return coord


def catalogue(coord):
    """Get catalogue from VO server"""
    ret = sub.run("munipack cone --cat=UCAC4 --radius=0.2 -- '{}' '{}'"
                  .format(coord.ra.deg, coord.dec.deg),
                  shell=True)
    return ret.returncode


def artificial(coord, setup):
    """Generate artificial frame"""
    cmd = ["munipack", "artificial", "--verbose", "--cat=cone.fits"]
    for key in setup:
        if setup[key]:
            if key == "atmosphere":
                cmd.append("--{}".format(key))
            else:
                cmd.append("--{}={}".format(key, setup[key]))
    cmd.append("--rcen={}".format(coord.ra.deg))
    cmd.append("--dcen={}".format(coord.dec.deg))
    if "date" not in setup or not setup["date"]:
        cmd.append("--date={}".format(strftime("%Y-%m-%d")))
    if "time" not in setup or not setup["time"]:
        cmd.append("--time={}".format(strftime("%H:%M:%S")))
    ret = sub.run(cmd, stdout=sub.PIPE, stderr=sub.STDOUT,
                  universal_newlines=True)
    return ret.stdout


def fitspng():
    """Generate unique name for static images"""
    os.rename("artificial.fits", "static/artificial.fits")
    sub.run("fitspng -o static/fitspng.png static/artificial.fits", shell=True)
    imname = "/static/fitspng.png?{}".format(int(time()))
    finame = "/static/artificial.fits?{}".format(int(time()))
    return imname, finame


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
