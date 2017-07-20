#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""


from secrets import token_urlsafe
from flask import request, session, redirect, render_template


DEFAULT = {
    "psf": {"label": "Point spread function", "place": "SEEING", "text": "seeing"},
    "spread": {"label": "Seeing spread method", "place": "FFT", "text": "fft"},
    "hwhm": {"label": "Half width at half of maximum", "place": "1.00", "text": "pix"},
    "airy": {"label": "Radius of Airy spot", "place": "0.10", "text": "pix"},
    "beta": {"label": "Moffat exponent", "place": "2.00", "text": ""},
    "maglim": {"label": "Magnitude limit", "place": "13", "text": ""},
    "back-level": {"label": "Background level", "place": "1000.0", "text": "cts"},
    "back-noise": {"label": "Background noise", "place": "31.6", "text": "cts"},
    "back-grad-x": {"label": "Background gradient in x", "place": "0.0", "text": "cts/pix"},
    "back-grad-y": {"label": "Background gradient in y", "place": "0.0", "text": "cts/pix"},
    "area": {"label": "Area of input aperture", "place": "1.00", "text": "m<sup>2</sup>"},
    "diameter": {"label": "Diameter of input aperture", "place": "", "text": "m"},
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


def config():
    """Setup parameters with options configuration"""
    if not session.get("config", False):
        session["config"] = {}
    if request.method == "POST":
        setin = 0
        setup = request.form.to_dict()
        del setup["token"]
        for field in setup:
            if setup[field]:
                setin += 1
        if "psf" in setup and setup["psf"] == "SEEING":
            setin -= 1
        if "spread" in setup and setup["spread"] == "FFT":
            setin -= 1
        session["setin"] = setin
        session["config"] = setup
        session["reset"] = True
        session.modified = True
    form = session.get("config", {})
    return render_template("config.html", form=form, default=DEFAULT,
                           token=token_urlsafe(32))


def reset():
    """Setup page after reseting settings"""
    session["setin"] = 0
    session["config"] = {}
    session["reset"] = True
    session.modified = True
    return redirect("/config")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
