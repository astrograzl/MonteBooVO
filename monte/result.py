#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""


import os
import subprocess as sub
from string import capwords
from time import time, strftime
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from flask import flash, request, session, redirect, render_template


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
    ret = sub.run("munipack cone --verbose --cat=UCAC4 -r 0.5 -- '{}' '{}'"
                  .format(coord.ra.deg, coord.dec.deg), shell=True,
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
    else:
        flash("Not found new artificial frame. " +
              "Have a look at debug page for more information. " +
              "Intead of staring at this not actual image.")
    imname = "/static/fitspng.png?{}".format(int(time()))
    finame = "/static/artificial.fits?{}".format(int(time()))
    return imname, finame


def result():
    """Result page with artificial frame"""
    if request.method == "POST":
        if request.form["type"] == "search":  # search widget
            search = True
            click = False
            name = request.form["name"]

            coor = coordination(name)
            if coor is None:
                flash("Can't find required object. Please try another one.")
                return redirect("/index")

            session["cat"] = catalogue(coor)
            session.modified = True
            if session["cat"]["retcode"] != 0:
                flash("This is really bad :-( " +
                      "Looks like zombies shutdown the server.")
                return redirect("/index")

        elif request.form["type"] == "button":  # click on button
            click = True
            search = False
            ra = session["data"]["ra"]["deg"]
            dec = session["data"]["dec"]["deg"]
            name = session["data"]["name"]
            coor = SkyCoord(ra=ra, dec=dec, unit=u.degree)

        if search or (click and session.get("reset", False)):
            session["art"] = artificial(coor, session.get("config", {}))
            session["reset"] = False
            session.modified = True

        imname, finame = fitspng()  # always reload saved image

        # update stored data in session
        data = {"name": capwords(name),
                "ra": {"deg": coor.ra.deg,
                       "str": coor.ra.to_string(unit=u.hourangle, sep=":")},
                "dec": {"deg": coor.dec.deg,
                        "str": coor.dec.to_string(unit=u.degree, sep=":")},
                "img": imname,
                "fit": finame}
        session["data"] = data
        session.modified = True

        return render_template("result.html", data=data)

    if request.method == "GET":
        data = session.get("data", {})
        if data.get("name", False):
            return render_template("result.html", data=data)
        return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
