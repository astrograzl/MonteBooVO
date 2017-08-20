#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import subprocess as sub
from time import sleep, gmtime, strftime
from astropy import units as u
from astropy.coordinates import SkyCoord
from flask import flash, request, session, redirect, render_template


def artificial(coord, setup, id):
    """Generate artificial frame."""
    cmd = ["munipack", "artificial", "--verbose", "--mask=static/{}.fits.fz"
           .format(id)]
    if session["data"]["name"] != "Random":
        cmd.append("--cat=static/{}.fits.gz".format(id))
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

    std = open("stdout.log", "w")
    pop = sub.Popen(cmd, stdout=std, stderr=sub.STDOUT,
                    universal_newlines=True)
    session["art"] = {"args": "\n".join(pop.args),
                      "retcode": 0,
                      "stdout": ""}
    session.modified = True
    return pop


def fitspng(id):
    """Convert fits frame to png image."""
    ret = sub.run("fitspng --verbose -o static/{}.png static/{}.fits.fz"
                  .format(id, id),
                  stdout=sub.PIPE,
                  stderr=sub.STDOUT,
                  universal_newlines=True,
                  shell=True,)
    return {"retcode": ret.returncode,
            "args": ret.args,
            "stdout": ret.stdout}


def proces():
    """Process request about artificial frame."""
    if request.method == "POST" or session.get("reset", False):
        id = session.get("id", "")
        if not session.get("proces", False) and len(id) > 0:
            ra = session["data"]["ra"]["deg"]
            dec = session["data"]["dec"]["deg"]
            coor = SkyCoord(ra, dec, unit=u.deg)
            sky = "static/{}.fits.fz".format(id)
            if os.path.exists(sky):
                os.remove(sky)
            art = artificial(coor, session.get("config", {}), id)
            session["reset"] = False
            sleep(1)
            if art.poll() == 0 and not os.path.exists(sky):
                flash("Can not create new artificial frame. " +
                      "Have a look at debug page for more information. " +
                      "Instead of staring at this not actual image.")
                session["art"]["stdout"] = open("stdout.log", "r").read()
                session.modified = True
                return redirect("/debug")

            session["proces"] = True
            session.modified = True
            return render_template("proces.html")

    if request.method == "GET":
        id = session.get("id", "")
        if session.get("proces", False) and len(id) > 0:
            sky = "static/{}.fits.fz".format(id)
            if os.path.exists(sky):
                session["proces"] = False
                session["art"]["stdout"] = open("stdout.log", "r").read()
                session["png"] = fitspng(id)
                session.modified = True
                return redirect("/result")
            return render_template("proces.html")
        return redirect("/index")

    return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
