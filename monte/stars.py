#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
from time import time
from flask import session, redirect, render_template
from matplotlib import pyplot as plt
from astropy.io import fits


def stars():
    id = session.get("id", "")
    if len(id) > 0:
        sky = "cone/{}.fits".format(id)
        if os.path.exists(sky):
            data = fits.getdata(sky)
            plt.scatter(data["RAJ2000"], data["DECJ2000"], s=data["MAG"])
            plt.savefig("static/{}.svg".format(id))
            session["data"]["svg"] = "static/{}.svg?{}".format(id, int(time()))
            session.modified = True
            return render_template("stars.html")
        return redirect("/debug")
    return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
