#
# Copyright 2015-2016 Universidad Complutense de Madrid
#
# This file is part of Numina
#
# Numina is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Numina is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Numina.  If not, see <http://www.gnu.org/licenses/>.
#

"""Store the solution of a wavelength calibration"""

from __future__ import division, print_function

from numpy.polynomial import Polynomial


class CrLinear(object):

    def __init__(self, crpix, crval, crmin, crmax, cdelt):
        self.crpix = crpix
        self.crval = crval
        self.cdelt = cdelt
        self.crmin = crmin
        self.crmax = crmax

    def __getstate__(self):
        state = self.__dict__.copy()
        for k in state:
            state[k] = float(state[k])
        return state


class WavecalFeature(object):
    """Store information concerning a particular line identification.

    Parameters
    ----------
    line_ok : bool
        True if the line has been properly identified.
    category : char
        Line identification type (A, B, C, D, E, R, T, P, K, I, X).
        See documentation embedded within the arccalibration_direct
        function for details.
    lineid : int
        Number of identified line within the master list.
    xpos : float
        Pixel x-coordinate of the peak of the line.
    ypos : float
        Pixel y-coordinate of the peak of the line.
    flux : float
        Flux of the line.
    fwhm : float
        FWHM of the line.
    wv : float
        Wavelength of the identified line in the master list.

    Attributes
    ----------

    """

    def __init__(self, line_ok, category, lineid, funcost, xpos, ypos,
                 flux, fwhm, reference, wavelength=0.0):
        self.line_ok = line_ok
        self.category = category
        self.lineid = lineid
        self.funcost = funcost
        self.xpos = xpos
        self.ypos = ypos
        self.flux = flux
        self.fwhm = fwhm
        self.reference = reference
        self.wavelength = wavelength

    def __getstate__(self):
        state = self.__dict__.copy()
        float_keys = ['funcost', 'xpos', 'ypos', 'flux', 'fwhm', 'reference', 'wavelength']
        for k in state:
            if k in float_keys:
                state[k] = float(state[k])
            elif k in ['lineid']:
                state[k] = int(state[k])
            else:
                pass
        return state

    def __str__(self):
        if self.line_ok:
            sline_ok = 'True '
        else:
            sline_ok = 'False'
        output = "<WavecalFeature instance>  " + \
                 "line_ok: " + sline_ok + "  " + \
                 "category: " + str(self.category) + "  " + \
                 "id: " + str(self.lineid) + "  " + \
                 "xpos: " + str(self.xpos) + "  " + \
                 "ypos: " + str(self.ypos) + "  " + \
                 "flux: " + str(self.flux) + "  " + \
                 "fwhm: " + str(self.fwhm) + "  " + \
                 "reference: " + str(self.reference) + "  " + \
                 "wavelength: " + str(self.wavelength) + "  " + \
                 "funcost: " + str(self.funcost)

        return output


class SolutionArcCalibration(object):
    """Auxiliary class to store the arc calibration solution.

    Note that this class only stores the information concerning the
    arc lines that have been properly identified. The information
    about all the lines (including those initially found but at the
    end discarded) is stored in the list of WavecalFeature instances
    'list_of_wvfeatures'.

    Parameters
    ----------
    features : list (of WavecalFeature instances)
        A list of size equal to the number of identified lines, which
        elements are instances of the class WavecalFeature, containing
        all the relevant information concerning the line
        identification.
    coeff : 1d numpy array (float)
        Coefficients of the wavelength calibration polynomial.
    residual_std : float
        Residual standard deviation of the fit.
    crpix1_linear : float
        CRPIX1 value employed in the linear wavelength calibration.
    crval1_linear : float
        CRVAL1 value corresponding to the linear wavelength
        calibration.
    crmin1_linear : float
        CRVAL value at pixel number 1 corresponding to the linear
        wavelength calibration.
    crmax1_linear : float
        CRVAL value at pixel number NAXIS1 corresponding to the linear
        wavelength calibration.
    cdelt1_linear: float
        CDELT1 value corresponding to the linear wavelength
        calibration.

    Attributes
    ----------
    nlines_arc : int
        Total number of identified arc lines.
    xpos : list of floats
        Pixel coordinate of the peak of all the arc lines.
    ypos : lsit of floats
        Pixel y-coordinate of the peak of the line.
    flux : list of floats
        Flux of the line.
    fwhm : list of floats
        FWHM of the line.
    reference : list of floats
        Wavelength of the identified lines in the master list.
    wavelength : list of floats
        Wavelength of the identified lines from fitted polynomial.
    funcost : list of floats
        Cost function corresponding to each identified arc line.
    category : list of characters
        Line identification type (A, B, C, D, E, R, T, P, K, I, X).
        See documentation embedded within the arccalibration_direct
        function for details.
    id : list of integers
        Number of identified arc line within the wv_master array.
    coeff : list of floats
        Coefficients of the wavelength calibration polynomial.
    residual_std : float
        Residual standard deviation of the fit.
    crpix1_linear : float
        CRPIX1 value employed in the linear wavelength calibration.
    crval1_linear : float
        CRVAL1 value corresponding to the linear wavelength
        calibration.
    crmin1_linear : float
        CRVAL value at pixel number 1 corresponding to the linear
        wavelength calibration.
    crmax1_linear : float
        CRVAL value at pixel number NAXIS1 corresponding to the linear
        wavelength calibration.
    cdelt1_linear: float
        CDELT1 value corresponding to the linear wavelength
        calibration.

    """
    # TODO: update previous attribute list after introducing the new class
    #       cr_linear

    def __init__(self, features, coeff, residual_std, cr_linear):

        self.features = features

        self.coeff = [float(tmpcoeff) for tmpcoeff in coeff]
        # force residual_std to be a float and not an scalar numpy array
        self.residual_std = float(residual_std)
        self.cr_linear = cr_linear

        # use fitted polynomial to predict wavelengths at the line
        # locations given by xpos
        self.update_features(poly=Polynomial(coeff))

    def update_features(self, poly):
        for feature in self.features:
            feature.wavelength = poly(feature.xpos)

    @property
    def nlines_arc(self):
        return len([wvfeature for wvfeature in self.features if wvfeature.line_ok])

    def __eq__(self, other):
        return self.__getstate__() == other.__getstate__()

    def __str__(self):
        """Printable representation of a SolutionArcCalibration instance."""

        output = "<SolutionArcCalibration instance>\n" + \
                 "Number arc lines: " + str(self.nlines_arc) + "\n" + \
                 "Coeff...........: " + str(self.coeff) + "\n" + \
                 "Residual std....: " + str(self.residual_std) + "\n" + \
                 "CRPIX1_linear...: " + str(self.crpix1_linear) + "\n" + \
                 "CRVAL1_linear...: " + str(self.crval1_linear) + "\n" + \
                 "CDELT1_linear...: " + str(self.cdelt1_linear) + "\n" + \
                 "CRMIN1_linear...: " + str(self.crmin1_linear) + "\n" + \
                 "CRMAX1_linear...: " + str(self.crmax1_linear) + "\n"

        for i in range(self.nlines_arc):
            output += "xpos: {0:9.3f},  ".format(self.xpos[i])
            output += "ypos: {0:9.3f},  ".format(self.ypos[i])
            output += "flux: {0:g},  ".format(self.flux[i])
            output += "fwhm: {0:g},  ".format(self.fwhm[i])
            output += "reference: {0:10.3f},  ".format(self.reference[i])
            output += "wavelength: {0:10.3f},  ".format(self.wavelength[i])
            output += "category: {0:1s},  ".format(self.category[i])
            output += "id: {0:3d},  ".format(self.id[i])
            output += "funcost: {0:g},  ".format(self.funcost[i])
            output += "\n"

        # return string with all the information
        return output

    def __getstate__(self):
        result = self.__dict__.copy()
        result['features'] = [
            feature.__getstate__() for feature in self.features
            ]
        result['cr_linear'] = result['cr_linear'].__getstate__()
        return result

    def __setstate__(self, state):
        self.__dict__ = state.copy()
        features = []
        for feature in state['features']:
            newf = WavecalFeature.__new__(WavecalFeature)
            newf.__dict__ = feature
            features.append(newf)

        self.features = features
        self.cr_linear = CrLinear(**state['cr_linear'])