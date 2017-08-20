#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import subprocess as sub
from time import sleep
from uuid import uuid4
from string import capwords
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from flask import flash, request, session, redirect, render_template


def coordination(name):
    """Get object coordination from Simbad database by the name."""
    if name is None:
        return SkyCoord(ra=0, dec=0, unit=u.deg)
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
    session["coord"] = True
    std = open("stderr.log", "w")
    ret = sub.Popen("munipack cone --output=cone/{}.fits ".format(id) +
                    "--verbose --cat=UCAC4 --radius=0.256 -- '{}' '{}'"
                    .format(coord.ra.deg, coord.dec.deg), shell=True,
                    stdout=std, stderr=sub.STDOUT, universal_newlines=True)
    session["cat"] = {"args": ret["args"], "retcode": 0, "stdout": ""}
    session.modified = True
    return ret


def coord():
    """Process coordination question and catalogue download"""
    if request.method == "POST":
        id = str(uuid4())
        if request.form["type"] == "random":
            name = "Random"
            coor = coordination(None)
        if request.form["type"] == "search":
            name = request.form["name"]
            coor = coordination(name)
            if coor is None:
                flash("Can't find required object. Please try another one.")
                return redirect("/index")

        data = {"ra": {"deg": coor.ra.deg,
                       "str": coor.ra.to_string(unit=u.hourangle, sep=":")},
                "dec": {"deg": coor.dec.deg,
                        "str": coor.dec.to_string(unit=u.degree, sep=":")},
                "name": capwords(name)}

        session["id"] = id
        session["data"] = data
        session.modified = True

        if name != "Random":
            co = "cone/{}.fits".format(id)
            if os.path.exists(co):
                os.remove(co)
            cat = catalogue(coor, id)
            sleep(2)
            if cat.poll() is not None and cat.poll() != 0:
                flash("This is really bad :-( " +
                      "Looks like zombies shutdown the server.")
                session["coord"] = False
                session["cat"]["retcode"] = cat.poll()
                session["cat"]["stdout"] = open("stderr.log", "r").read()
                session.modified = True
                return redirect("/debug")
            return render_template("coord.html")
        return redirect("/proces", code=307)

    if request.method == "GET":
        id = session.get("id", "")
        if session.get("coord", False) and len(id) > 0:
            if os.path.exist("cone/{}.fits".format(id)):
                session["coord"] = False
                session["cat"]["retcode"] = 0
                session["cat"]["stdout"] = open("stderr.log", "r").read()
                session.modified = True
                return redirect("/proces", code=307)
            return render_template("coord.html")
        return redirect("/index")

    return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
