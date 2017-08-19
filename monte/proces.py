#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import subprocess as sub
from uuid import uuid4
from string import capwords
from time import time, gmtime, strftime, sleep
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
                  "--verbose --cat=UCAC4 --radius=0.256 -- '{}' '{}'"
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

    session["art"] = {}
    session["art"]["args"] = cmd
    session["art"]["retcode"] = 0
    session["art"]["stdout"] = ""
    stdout = open("stdout.log", "w")
    pop = sub.Popen(cmd, stdout=stdout, stderr=sub.STDOUT,
                    universal_newlines=True)
    return pop


def fitspng(id):
    """Convert fits frame to png image."""
    ret = sub.run("fitspng --verbose -o static/{}.png static/{}.fits.gz"
                  .format(id, id),
                  stdout=sub.PIPE, stderr=sub.STDOUT, shell=True,
                  universal_newlines=True)
    return {"retcode": ret.returncode, "args": ret.args, "stdout": ret.stdout}


def proces():
    """Process request about artificial frame."""
    if request.method == "POST":
        id = str(uuid4())
        if request.form["type"] == "random":  # random frame
            name = "Random"
            coor = None
        elif request.form["type"] == "search":  # search widget
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

        session["id"] = id
        session["data"] = data
        session.modified = True

    if request.method == "GET":
        if session.get("reset", False):  # click
            id = session.get("id", "")
            if not len(id) > 0:
                return redirect("/index")
            name = session["data"]["name"]
            if name == "Random":
                coor = None
            else:
                ra = session["data"]["ra"]["deg"]
                dec = session["data"]["dec"]["deg"]
                coor = SkyCoord(ra=ra, dec=dec, unit=u.degree)
            session["reset"] = False
            session.modified = True
        elif session.get("proces", False):  # wait
            id = session["id"]
            sky = "static/{}.fits.gz".format(id)
            if os.path.exists(sky):
                session["proces"] = False
                session["png"] = fitspng(id)
                session["art"]["stdout"] = open("stdout.log", "r").read()
                session.modified = True
                return redirect("/result")
            else:
                dt = time() - session["time"]
                return render_template("proces.html", dt=dt, pt=dt/666*100)
        else:
            return redirect("/index")

    sky = "static/{}.fits.gz".format(id)
    if os.path.exists(sky):
        os.remove(sky)
    art = artificial(coor, session.get("config", {}), id)
    sleep(1)
    if art.poll() == 0 and not os.path.exists(sky):
        flash("Can not create new artificial frame. " +
              "Have a look at debug page for more information. " +
              "Instead of staring at this not actual image.")
        session["art"] = {"retcode": art.returncode,
                          "args": art.args,
                          "stdout": open("stdout.log", "r").read()}
        session.modified = True
        return redirect("/result")

    session["time"] = time()
    session["proces"] = True
    session.modified = True

    return redirect("/proces")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
