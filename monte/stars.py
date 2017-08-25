#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
from time import time
from flask import session, redirect, render_template
from astropy.io import fits
import numpy as np
import matplotlib as mpl; mpl.use("Cairo")
import matplotlib.pyplot as plt


def stars():
    """Plot star chart from catalogue data"""
    id = session.get("id", "")
    svg = "static/{}.svg".format(id)
    sess = session.get("data", {})
    if os.path.exists(svg):
        return render_template("stars.html", data=sess)
    if sess.get("name", "Random") != "Random" and len(id) > 0:
        co = "static/{}.fits.gz".format(id)
        if os.path.exists(co):
            data = fits.getdata(co)
            mask = np.isnan(data["Bmag"]) + np.isnan(data["Vmag"])
            plt.figure(figsize=(8, 8))
            plt.xlabel("$\\alpha$")
            plt.ylabel("$\\delta$")
            plt.grid(True)
            plt.gca().invert_xaxis()
            plt.scatter(data["RAJ2000"][mask], data["DEJ2000"][mask],
                        s=32*pow(10, 0.11*(13-data["f.mag"])),
                        c="gray", alpha=0.75)  # ,marker="+")
            plt.scatter(data["RAJ2000"], data["DEJ2000"],
                        s=32*pow(10, 0.11*(13-data["f.mag"])),
                        c=data["Bmag"]-data["Vmag"])
            plt.savefig("static/{}.svg".format(id), bbox_inches="tight",
                        transparent=True)
            session["data"]["svg"] = "static/{}.svg?{}".format(id, int(time()))
            session.modified = True
            return render_template("stars.html", data=session.get("data", {}))
        return redirect("/debug")
    return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
