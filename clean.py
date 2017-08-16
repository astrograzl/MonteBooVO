#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
import sys
import glob
import time


if len(sys.argv) > 1:
    path = sys.argv[1]
    if not os.path.isdir(path):
        sys.exit("Not a valid path to the directory")
else:
    path = os.getcwd()

now = time.time()
old = now - 60 * 60 * 24 * 7

mask = "????????-????-????-????-????????????"
cone = glob.glob(os.path.join(path, "cone", mask+".fits"))
fits = glob.glob(os.path.join(path, "static", mask+".fits"))
pngs = glob.glob(os.path.join(path, "static", mask+".png"))

garbage = cone + fits + pngs

for waste in garbage:
    if os.path.getmtime(waste) < old:
        os.remove(waste)
