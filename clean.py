#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import sys
from glob import glob
from time import time


if len(sys.argv) > 1:
    path = sys.argv[1]
    if not os.path.isdir(path):
        sys.exit("Not a valid path to the directory")
else:
    path = os.getcwd()

past = time() - 60 * 60 * 24 * 7

mask = "????????-????-????-????-????????????"
cone = glob(os.path.join(path, "cone", mask+".fits"))
fits = glob(os.path.join(path, "static", mask+".fits"))
pngs = glob(os.path.join(path, "static", mask+".png"))

garbage = cone + fits + pngs

for waste in garbage:
    if os.path.getmtime(waste) < past:
        os.remove(waste)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
