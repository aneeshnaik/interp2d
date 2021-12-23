#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bilinear interpolation.

Created: December 2021
Author: A. P. Naik
"""
import numpy as np


def interp_array(x, y, xp, yp, zp):

    # grid spacings and sizes
    hx = xp[1] - xp[0]
    hy = yp[1] - yp[0]
    Nx = xp.size
    Ny = yp.size

    # snap beyond-boundary points to boundary
    x[x < xp[0]] = xp[0]
    y[y < yp[0]] = yp[0]
    x[x > xp[-1]] = xp[-1]
    y[y > yp[-1]] = yp[-1]

    # find indices of surrounding points
    i1 = np.floor((x - xp[0]) / hx).astype(int)
    i1[i1 == Nx - 1] = Nx - 2
    j1 = np.floor((y - yp[0]) / hy).astype(int)
    j1[j1 == Ny - 1] = Ny - 2
    i2 = i1 + 1
    j2 = j1 + 1

    # get coords and func at surrounding points
    x1 = xp[i1]
    x2 = xp[i2]
    y1 = yp[j1]
    y2 = yp[j2]
    z11 = zp[i1, j1]
    z21 = zp[i2, j1]
    z12 = zp[i1, j2]
    z22 = zp[i2, j2]

    # interpolate
    t11 = z11 * (x2 - x) * (y2 - y)
    t21 = z21 * (x - x1) * (y2 - y)
    t12 = z12 * (x2 - x) * (y - y1)
    t22 = z22 * (x - x1) * (y - y1)
    z = (t11 + t21 + t12 + t22) / (hx * hy)
    return z
