# interp2d

Fast bilinear interpolation in Python. Only to be used on a regular 2D grid, where it is more efficient than `scipy.interpolate.RectBivariateSpline` in the case of a continually changing interpolation grid (see Comparison with `scipy.interpolate` below).

## Usage

There is only one function (defined in `__init__.py`), `interp2d`. This works much like the `interp` function in `numpy`.

Given a *regular* coordinate grid and gridded data defined as follows:
```python
import numpy as np
from interp2d import interp2d

# define coordinate grid, xp and yp both 1D arrays
xp = np.linspace(0, 1, 200)
yp = np.linspace(-6 * np.pi, 6 * np.pi, 200)

# gridded data, zp is 2D array
zp = xp[:, None]**2 * np.sin(yp[None])
```
Subsequently, one can then interpolate within this grid. The interpolation points can either be single scalars or arrays of points.
```python
>>> interp2d(0.5, 0.78*np.pi, xp, yp, zp)
0.15866472278446267

>>> x = np.linspace(0.1, 0.2, 5)
>>> y = 0.5 * np.pi * np.ones_like(x)
>>> interp2d(x, y, xp, yp, zp)
array([0.00997272, 0.01558158, 0.02243672, 0.03053814, 0.03988582])
```
Interpolation points outside the given coordinate grid will be evaluated on the boundary.

## Comparison with `scipy.interpolate`

The standard way to do two-dimensional interpolation in the Python scientific ecosystem is with the various interpolators defined in the `scipy.interpolate` sub-package. If one is interpolating on a regular grid, the fastest option there is the object `RectBivariateSpline`. To use this, you first construct an instance of `RectBivariateSpline` feeding in the coordinate grids and data. This then provides a function, which can be called to give interpolated values. While these function calls are cheap, setting up the grid is less so. So, if one is interpolating from a continually changing grid (e.g. interpolating density from a grid in a time-evolving simulation), the `scipy` options are not ideal. To see this consider the following example, where `x`, `y`, `xp`, `yp`, `zp` are defined as in the previous example (in Usage above).
```python
>>> %timeit interp2d(x, y, xp, yp, zp)
31.2 µs ± 197 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

>>> %timeit RectBivariateSpline(xp, yp, zp, kx=1, ky=1)(x, y, grid=False)
1.14 ms ± 5.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```
Thus, we have a 40x speedup.

## Prerequisites

The only prerequisite is `numpy`. My code was developed and tested using version 1.20.3, but earlier/later versions likely to work also.
