#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import subprocess as sub
from uuid import uuid4
from string import capwords
from time import time, gmtime, strftime
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from flask import flash, request, session, redirect, render_template


def coordination(name):
    """Get object coordination from Simbad database by the name."""
    try:
        coord = SkyCoord.from_name(name)
    except NameResolveError:
        return None
    else:
        return coord


def catalogue(coord, id):
    """Get catalogue from VO server."""
    if not os.path.isdir("cone"):
        os.mkdir("cone")
    ret = sub.run("munipack cone --output=cone/{}.fits ".format(id) +
                  "--verbose --cat=UCAC4 -r 0.5 -- '{}' '{}'"
                  .format(coord.ra.deg, coord.dec.deg), shell=True,
                  stdout=sub.PIPE, stderr=sub.STDOUT, universal_newlines=True)
    return {"retcode": ret.returncode, "args": ret.args, "stdout": ret.stdout}


def artificial(coord, setup, id):
    """Generate artificial frame."""
    cmd = ["munipack", "artificial", "--verbose", "--mask=static/{}.fits.gz"
           .format(id)]
    if coord is not None:
        cmd.append("--cat=cone/{}.fits".format(id))
        cmd.append("--rcen={}".format(coord.ra.deg))
        cmd.append("--dcen={}".format(coord.dec.deg))

    for key in setup:
        if setup[key]:
            if key == "atmosphere":
                cmd.append("--{}".format(key))
            else:
                cmd.append("--{}={}".format(key, setup[key]))

    if "date" not in setup or not setup["date"]:
        cmd.append("--date={}".format(strftime("%Y-%m-%d", gmtime())))

    if "time" not in setup or not setup["time"]:
        cmd.append("--time={}".format(strftime("%H:%M:%S", gmtime())))

    ret = sub.run(cmd, stdout=sub.PIPE, stderr=sub.STDOUT,
                  universal_newlines=True)
    return {"retcode": ret.returncode, "args": ret.args, "stdout": ret.stdout}


def fitspng(id):
    """Convert fits frame to png image."""
    if time() - os.path.getmtime("static/{}.fits.gz".format(id)) > 1:
        flash("Not found new artificial frame. " +
              "Have a look at debug page for more information. " +
              "Instead of staring at this not actual image.")
        return {"retcode": "", "args": "", "stdout": ""}
    ret = sub.run("fitspng --verbose -o static/{}.png static/{}.fits.gz"
                  .format(id, id),
                  stdout=sub.PIPE, stderr=sub.STDOUT, shell=True,
                  universal_newlines=True)
    return {"retcode": ret.returncode, "args": ret.args, "stdout": ret.stdout}


def result():
    """Show Result page with artificial frame."""
    if request.method == "POST":
        if request.form["type"] == "random":  # random frame
            id = str(uuid4())
            click = False
            search = False
            random = True
            name = "Random"
            coor = None

        elif request.form["type"] == "search":  # search widget
            id = str(uuid4())
            search = True
            click = False
            random = False
            name = request.form["name"]

            coor = coordination(name)
            if coor is None:
                flash("Can't find required object. Please try another one.")
                return redirect("/index")

            session["cat"] = catalogue(coor, id)
            session.modified = True
            if session["cat"]["retcode"] != 0:
                flash("This is really bad :-( " +
                      "Looks like zombies shutdown the server.")
                return redirect("/index")

        elif request.form["type"] == "button":  # click on button
            id = session["id"]
            click = True
            search = False
            random = False
            name = session["data"]["name"]
            if name == "Random":
                coor = None
            else:
                ra = session["data"]["ra"]["deg"]
                dec = session["data"]["dec"]["deg"]
                coor = SkyCoord(ra=ra, dec=dec, unit=u.degree)

        if search or random or (click and session.get("reset", False)):
            session["id"] = id
            session["art"] = artificial(coor, session.get("config", {}), id)
            session["png"] = fitspng(id)
            session["reset"] = False
            session.modified = True

        # update stored data in session
        data = {}
        data["ra"] = {}
        data["dec"] = {}
        if name == "Random":
            data["ra"]["str"] = "00:00:00"
            data["dec"]["str"] = "00:00:00"
        else:
            data["ra"]["deg"] = coor.ra.deg
            data["ra"]["str"] = coor.ra.to_string(unit=u.hourangle, sep=":")
            data["dec"]["deg"] = coor.dec.deg
            data["dec"]["str"] = coor.dec.to_string(unit=u.degree, sep=":")
        data["name"] = capwords(name)
        if os.path.exists("static/{}.png".format(id)):
            data["img"] = "/static/{}.png?{}".format(id, int(time()))
        else:
            data["img"] = "/static/images/moffat.png"
        if os.path.exists("static/{}.fits.gz".format(id)):
            data["fit"] = "/static/{}.fits.gz?{}".format(id, int(time()))
        else:
            data["fit"] = "#"
        session["data"] = data
        session.modified = True

        return render_template("result.html", data=data)

    elif request.method == "GET":
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
