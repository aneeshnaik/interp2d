#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Init file of interpy. See README for more details.

Created: December 2021
Author: A. P. Naik
"""
import numpy as np


def interp2d(x, y, xp, yp, zp):
    """
    Bilinearly interpolate over regular 2D grid.

    `xp` and `yp` are 1D arrays defining grid coordinates of sizes :math:`N_x`
    and :math:`N_y` respectively, and `zp` is the 2D array, shape
    :math:`(N_x, N_y)`, containing the gridded data points which are being
    interpolated from. Note that the coordinate grid should be regular, i.e.
    uniform grid spacing. `x` and `y` are either scalars or 1D arrays giving
    the coordinates of the points at which to interpolate. If these are outside
    the boundaries of the coordinate grid, the resulting interpolated values
    are evaluated at the boundary.

    Parameters
    ----------
    x : 1D array or scalar
        x-coordinates of interpolating point(s).
    y : 1D array or scalar
        y-coordinates of interpolating point(s).
    xp : 1D array, shape M
        x-coordinates of data points zp. Note that this should be a *regular*
        grid, i.e. uniform spacing.
    yp : 1D array, shape N
        y-coordinates of data points zp. Note that this should be a *regular*
        grid, i.e. uniform spacing.
    zp : 2D array, shape (M, N)
        Data points on grid from which to interpolate.

    Returns
    -------
    z : 1D array or scalar
        Interpolated values at given point(s).

    """
    # if scalar, turn into array
    scalar = False
    if not isinstance(x, (list, np.ndarray)):
        scalar = True
        x = np.array([x])
        y = np.array([y])

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
    if scalar:
        z = z[0]
    return z
