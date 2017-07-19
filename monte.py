#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""


import os
import subprocess as sub
from time import time, strftime
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError


default = {
    "psf": {"label": "Point spread function", "place": "", "text": "seeing"},
    "spread": {"label": "Seeing spread method", "place": "", "text": "fft"},
    "hwhm": {"label": "Half width at half of maximum", "place": "1.00", "text": "pix"},
    "airy": {"label": "Radius of Airy spot", "place": "0.10", "text": "pix"},
    "beta": {"label": "Moffat exponent", "place": "2.00", "text": ""},
    "maglim": {"label": "Magnitude limit", "place": "13", "text": ""},
    "back-level": {"label": "Background level", "place": "1000.0", "text": "cts"},
    "back-noise": {"label": "Background noise", "place": "31.6", "text": "cts"},
    "back-grad-x": {"label": "Background gradient in x", "place": "0.0", "text": "cts/pix"},
    "back-grad-y": {"label": "Background gradient in y", "place": "0.0", "text": "cts/pix"},
    "area": {"label": "Area of input aperture", "place": "1.00", "text": "m<sup>2</sup>"},
    "diameter": {"label": "Diameter of input aperture", "place": "1.1", "text": "m"},
    "exptime": {"label": "Exposure time", "place": "1.0", "text": "s"},
    "qeff": {"label": "Quantum efficiency", "place": "1.00", "text": ""},
    "atmosphere": {"label": "Apply atmosphere modelling", "place": "", "text": "extinction, seeing"},
    "extk": {"label": "Extinction coefficient", "place": "0.00", "text": ""},
    "long": {"label": "Geographic longitude of station (-east)", "place": "0.00", "text": "deg"},
    "lat": {"label": "Geographic latitude of station (+north)", "place": "0.00", "text": "deg"},
    "date": {"label": "Initial date", "place": "2000-01-01", "text": "YYYY-MM-DD"},
    "time": {"label": "Initial time", "place": "00:00:00.000", "text": "HH:MM:SS"},
    # "rcen": {"label": "Center of FOV in Right Ascension", "place": "0.0", "text": "deg"},
    # "dcen": {"label": "Center of FOV in Declination", "place": "0.0", "text": "deg"},
    "fov": {"label": "Field of view", "place": "0.2", "text": "deg"},
    "scale": {"label": "Scale", "place": "1/3600", "text": "deg/pix"},
    "angle": {"label": "Angle", "place": "0.0", "text": "deg, clockwise positive"},
    "width": {"label": "Width of output", "place": "666", "text": "pix"},
    "height": {"label": "Height of output", "place": "666", "text": "pix"},
}


def coordination(name):
    """Get object coordination from Simbad database by the name"""
    try:
        coord = SkyCoord.from_name(name)
    except NameResolveError:
        return None
    else:
        return coord


def catalogue(coord, setup):
    """Get catalogue from VO server"""
    fov = setup.get("fov", default["fov"]["place"])
    ret = sub.run("munipack cone --verbose --cat=UCAC4 --radius={} -- '{}' '{}'"
                  .format(fov, coord.ra.deg, coord.dec.deg), shell=True,
                  stdout=sub.PIPE, stderr=sub.STDOUT, universal_newlines=True)
    return {"retcode": ret.returncode, "args": ret.args, "stdout": ret.stdout}


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
    return {"retcode": ret.returncode, "args": ret.args, "stdout": ret.stdout}


def fitspng():
    """Generate unique name for static images"""
    if os.path.exists("artificial.fits"):
        sub.run("fitspng -o static/fitspng.png artificial.fits", shell=True)
        os.rename("artificial.fits", "static/artificial.fits")
    imname = "/static/fitspng.png?{}".format(int(time()))
    finame = "/static/artificial.fits?{}".format(int(time()))
    return imname, finame


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
