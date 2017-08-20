#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import sys
from glob import glob
from time import time


if len(sys.argv) == 3:
    path = sys.argv[1]
    hist = int(sys.argv[2])
    if not os.path.isdir(path):
        sys.exit("Not a valid path to the directory")
else:
    path = os.getcwd()
    hist = 666  # 60 * 60 * 24 * 7

past = time() - hist

mask = "????????-????-????-????-????????????"
cone = glob(os.path.join(path, "static", mask+".fits.gz"))
fits = glob(os.path.join(path, "static", mask+".fits.fz"))
pngs = glob(os.path.join(path, "static", mask+".png"))
svgs = glob(os.path.join(path, "static", mask+".svg"))

garbage = cone + fits + pngs + svgs

for waste in garbage:
    if os.path.getmtime(waste) < past:
        os.remove(waste)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
