#  PyTransit: fast and easy exoplanet transit modelling in Python.
#  Copyright (C) 2010-2019  Hannu Parviainen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import timeit
from typing import Tuple, Callable, Union, List, Optional

from numpy import ndarray, array, squeeze, atleast_2d, atleast_1d, zeros, asarray, linspace, sqrt, pi, ones, log, exp
from scipy.integrate import trapz

from .numba.ldmodels import *
from .numba.ptmodel import pt_model_direct_s, pt_model_interpolated_s, \
    pt_model_direct_s_simple, pt_model_direct_v, \
    pt_model_interpolated_v

from .numba.ptmodel import create_z_grid, calculate_weights_3d
from .transitmodel import TransitModel

__all__ = ['SwiftModel']


class SwiftModel(TransitModel):
    ldmodels = {'uniform': (ld_uniform, ldi_uniform),
                'linear': (ld_linear, ldi_linear),
                'quadratic': (ld_quadratic, ldi_quadratic),
                'quadratic_tri': ld_quadratic_tri,
                'nonlinear': ld_nonlinear,
                'general': ld_general,
                'square_root': ld_square_root,
                'logarithmic': ld_logarithmic,
                'exponential': ld_exponential,
                'power2': ld_power2}

    def __init__(self, ldmodel: Union[str, Callable, Tuple[Callable, Callable]] = 'quadratic',
                 interpolate: bool = True, klims: tuple = (0.005, 0.5), nk: int = 256,
                 nzin: int = 20, nzlimb: int = 20, zcut=0.7, ng: int = 50, parallel: bool = False,
                 small_planet_limit: float = 0.05):
        """The ridiculously fast transit model by Parviainen (2020).

        Parameters
        ----------
        interpolate : bool, optional
            Use the interpolation method presented in Parviainen (2015) if true.
        klims : tuple, optional
            Radius ratio limits (kmin, kmax) for the interpolated model.
        nk : int, optional
            Radius ratio grid size for the interpolated model.
        nz : int, optional
            Normalized distance grid size for the interpolated model.
        """
        super().__init__()
        self.interpolate = interpolate
        self.parallel = parallel
        self.is_simple = False
        self.splimit = small_planet_limit

        # Set up the limmb darkening model
        # --------------------------------
        if isinstance(ldmodel, str):
            try:
                if isinstance(self.ldmodels[ldmodel], tuple):
                    self.ldmodel = self.ldmodels[ldmodel][0]
                    self.ldmmean = self.ldmodels[ldmodel][1]
                else:
                    self.ldmodel = self.ldmodels[ldmodel]
                    self.ldmmean = None
            except KeyError:
                print(
                    f"Unknown limb darkening model: {ldmodel}. Choose from [{', '.join(self.ldmodels.keys())}] or supply a callable function.")
                raise

        # Set the basic variable
        # ----------------------
        self.klims = klims
        self.nk = nk
        self.ng = ng
        self.nzin = nzin
        self.nzlimb = nzlimb
        self.zcut = zcut

        # Declare the basic arrays
        # ------------------------
        self.ze = None
        self.zm = None
        self.mu = None
        self.dk = None
        self.dg = None
        self.weights = None

        self._m_direct_s = None
        self._m_direct_v = None
        self._m_interp_s = None
        self._m_interp_v = None

        self._ldmu = linspace(1, 0, 200)
        self._ldz = sqrt(1 - self._ldmu ** 2)

        self.init_integration(nzin, nzlimb, zcut, ng, nk)

    def set_data(self, time: Union[ndarray, List],
                 lcids: Optional[Union[ndarray, List]] = None,
                 pbids: Optional[Union[ndarray, List]] = None,
                 nsamples: Optional[Union[ndarray, List]] = None,
                 exptimes: Optional[Union[ndarray, List]] = None,
                 epids: Optional[Union[ndarray, List]] = None) -> None:
        super().set_data(time, lcids, pbids, nsamples, exptimes, epids)
        self.set_methods()


    def set_methods(self):

        if self.npb == 1 and all(self.nsamples == 1):
            self.is_simple = True
        else:
            self.is_simple = False

        if self.interpolate:
            self._m_interp_s = self.choose_m_interp_s()
            self._m_interp_v = pt_model_interpolated_v
        else:
            self._m_direct_s = self.choose_m_direct_s()
            self._m_direct_v = pt_model_direct_v


    def init_integration(self, nzin, nzlimb, zcut, ng, nk=None):
        self.nk = nk
        self.ng = ng
        self.nzin = nzin
        self.nzlimb = nzlimb
        self.zcut = zcut
        self.ze, self.zm = create_z_grid(zcut, nzin, nzlimb)
        self.mu = sqrt(1 - self.zm ** 2)
        if self.interpolate:
            self.dk, self.dg, self.weights = calculate_weights_3d(nk, self.klims[0], self.klims[1], self.ze, ng)

    def choose_m_direct_s(self):
        time = linspace(-0.1, 0.1, self.npt)
        ldc = array([0.24, 0.12])
        ldp = ld_quadratic(self.mu, ldc)
        istar = 2 * trapz(self._ldz * ld_quadratic(self._ldmu, ldc), self._ldz)
        k = asarray([0.1])

        model = pt_model_direct_s
        ds = """rrmodel_direct_s(time, k, 0.0, 1.0, 4.0, 0.5*pi, 0., 0., ldp, istar, self.ze, self.zm, self.ng, self.splimit,
                                  self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae,
                                  True)"""
        tparallel = timeit.repeat(ds, repeat=3, number=50, globals={**globals(), **locals()})[-1]

        ds = """rrmodel_direct_s(time, k, 0.0, 1.0, 4.0, 0.5*pi, 0., 0., ldp, istar, self.ze, self.zm, self.ng, self.splimit,
                                  self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae,
                                  False)"""
        tserial = timeit.repeat(ds, repeat=3, number=50, globals={**globals(), **locals()})[-1]
        if tparallel < tserial:
            self.parallel = True
        tmin = min(tparallel, tserial)

        if self.is_simple:
            ds = """rrmodel_direct_s_simple(time, k, 0.0, 1.0, 4.0, 0.5*pi, 0., 0., ldp, istar, self.ze, self.zm, self.ng, 
                                             self.splimit, self.lcids, self.pbids, self.nsamples, self.exptimes, 
                                             self._es, self._ms, self._tae, False)"""
            tsimple = timeit.repeat(ds, repeat=3, number=50, globals={**globals(), **locals()})[-1]
            if tsimple < tmin:
                model = pt_model_direct_s_simple

        return model

    def choose_m_interp_s(self):
        time = linspace(-0.1, 0.1, self.npt)
        ldc = array([0.24, 0.12])
        ldp = ld_quadratic(self.mu, ldc)
        istar = 2 * trapz(self._ldz * ld_quadratic(self._ldmu, ldc), self._ldz)
        k = asarray([0.1])

        model = pt_model_interpolated_s
        ds = """rrmodel_interpolated_s(time, k, 0.0, 1.0, 4.0, 0.5*pi, 0., 0., ldp, istar, self.weights, self.zm, self.dk, 
                                        self.klims[0], self.dg, self.splimit, self.lcids, self.pbids, self.nsamples, self.exptimes, 
                                        self._es, self._ms, self._tae, True)"""
        tparallel = timeit.repeat(ds, repeat=3, number=50, globals={**globals(), **locals()})[-1]

        ds = """rrmodel_interpolated_s(time, k, 0.0, 1.0, 4.0, 0.5*pi, 0., 0., ldp, istar, self.weights, self.zm, self.dk, 
                                        self.klims[0], self.dg, self.splimit, self.lcids, self.pbids, self.nsamples, self.exptimes, 
                                        self._es, self._ms, self._tae, False)"""
        tserial = timeit.repeat(ds, repeat=3, number=50, globals={**globals(), **locals()})[-1]

        if tparallel < tserial:
            self.parallel = True

        return model


    def evaluate(self, k: Union[float, ndarray], ldc: Union[ndarray, List], t0: Union[float, ndarray],
                 p: Union[float, ndarray],
                 a: Union[float, ndarray], i: Union[float, ndarray], e: Optional[Union[float, ndarray]] = None,
                 w: Optional[Union[float, ndarray]] = None, copy: bool = True) -> ndarray:
        """Evaluate the transit model for a set of scalar or vector parameters.

        Parameters
        ----------
        k
            Radius ratio(s) either as a single float, 1D vector, or 2D array.
        ldc
            Limb darkening coefficients as a 1D or 2D array.
        t0
            Transit center(s) as a float or a 1D vector.
        p
            Orbital period(s) as a float or a 1D vector.
        a
            Orbital semi-major axis (axes) divided by the stellar radius as a float or a 1D vector.
        i
            Orbital inclination(s) as a float or a 1D vector.
        e : optional
            Orbital eccentricity as a float or a 1D vector.
        w : optional
            Argument of periastron as a float or a 1D vector.

        Notes
        -----
        The model can be evaluated either for one set of parameters or for many sets of parameters simultaneously. In
        the first case, the orbital parameters should all be given as floats. In the second case, the orbital parameters
        should be given as a 1D array-like.

        Returns
        -------
        ndarray
            Modelled flux either as a 1D or 2D ndarray.
        """

        # Scalar parameters branch
        # ------------------------
        if isinstance(t0, float):
            if e is None:
                e, w = 0.0, 0.0
            return self.evaluate_ps(k, ldc, t0, p, a, i, e, w, copy)

        # Parameter population branch
        # ---------------------------
        else:
            k, t0, p, a, i = asarray(k), asarray(t0), asarray(p), asarray(a), asarray(i)

            if k.ndim == 1:
                k = k.reshape((k.size, 1))

            npv = t0.size
            if e is None:
                e, w = zeros(npv), zeros(npv)

            ldp = evaluate_ld(self.ldmodel, self.mu, ldc)

            istar = zeros((npv, self.npb))
            for ipv in range(npv):
                for ipb in range(self.npb):
                    if self.ldmmean is not None:
                        istar[ipv, ipb] = self.ldmmean(ldc[ipv, ipb])
                    else:
                        istar[ipv, ipb] = 2 * trapz(self._ldz * self.ldmodel(self._ldmu, ldc[ipv, ipb]), self._ldz)

            if self.interpolate:
                flux = self._m_interp_v(self.time, k, t0, p, a, i, e, w, ldp, istar, self.weights, self.dk,
                                       self.klims[0], self.dg, self.lcids, self.pbids, self.nsamples,
                                       self.exptimes, self.npb, self._es, self._ms, self._tae)
            else:
                flux = self._m_direct_v(self.time, k, t0, p, a, i, e, w, ldp, istar, self.ze, self.ng,
                                       self.lcids, self.pbids, self.nsamples,
                                       self.exptimes, self.npb, self._es, self._ms, self._tae)
        return squeeze(flux)

    def evaluate_ps(self, k: Union[float, ndarray], ldc: ndarray, t0: float, p: float, a: float, i: float,
                    e: float = 0.0, w: float = 0.0, copy: bool = True) -> ndarray:
        """Evaluate the transit model for a set of scalar parameters.

        Parameters
        ----------
        k : array-like
            Radius ratio(s) either as a single float or an 1D array.
        ldc : array-like
            Limb darkening coefficients as a 1D array.
        t0 : float
            Transit center as a float.
        p : float
            Orbital period as a float.
        a : float
            Orbital semi-major axis divided by the stellar radius as a float.
        i : float
            Orbital inclination(s) as a float.
        e : float, optional
            Orbital eccentricity as a float.
        w : float, optional
            Argument of periastron as a float.

        Notes
        -----
        This version of the `evaluate` method is optimized for calculating a single transit model (such as when using a
        local optimizer). If you want to evaluate the model for a large number of parameters simultaneously, use either
        `evaluate` or `evaluate_pv`.

        Returns
        -------
        ndarray
            Modelled flux as a 1D ndarray.
        """

        ldc = asarray(ldc)
        k = asarray(k)

        ldp = self.ldmodel(self.mu, ldc)
        if self.ldmmean is not None:
            istar = self.ldmmean(ldc)
        else:
            istar = 2 * trapz(self._ldz * self.ldmodel(self._ldmu, ldc), self._ldz)

        if self.interpolate:
            flux = self._m_interp_s(self.time, k, t0, p, a, i, e, w, ldp, istar, self.weights, self.zm,
                                    self.dk, self.klims[0], self.dg, self.splimit, self.lcids, self.pbids, self.nsamples,
                                    self.exptimes, self._es, self._ms, self._tae, self.parallel)
        else:
            flux = self._m_direct_s(self.time, k, t0, p, a, i, e, w, ldp, istar, self.ze, self.zm, self.ng, self.splimit,
                                    self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae,
                                    self.parallel)

        return squeeze(flux)
