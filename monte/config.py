#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import json
from flask import flash, request, session, redirect, render_template, Response


def config():
    """Options configuration."""
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                flash("Select file with saved configuration first.")
                return redirect("/config")
            try:
                setup = json.load(file)
            except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                flash("Select proper file with saved configuration.")
                return redirect("/config")
        else:
            setup = request.form.to_dict()
        setin = 0
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
    return render_template("config.html", form=form)


def reset():
    """Reset configuration."""
    session["setin"] = 0
    session["config"] = {}
    session["reset"] = True
    session.modified = True
    return redirect("/config")


def export():
    """Export configuration to file"""
    head = {}
    head["Content-Type"] = "application/json"
    head["Content-Disposition"] = "attachment; filename='export.json'"
    data = json.dumps(session["config"], indent=1)
    return Response(data, headers=head)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
