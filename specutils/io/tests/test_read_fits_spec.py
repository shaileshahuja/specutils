import os
import pytest
import astropy.io.ascii as ascii
from astropy import units as u
import numpy as np


from specutils.io import read_fits



def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)

def test_multispec_legendre():
    iraf = ascii.read(data_path('TRES.dat'), data_start = 127, Reader = ascii.NoHeader, names = ['wave', 'flux'])
    spectra = read_fits.read_fits_spectrum1d(data_path('TRES.fits'))
    spec = spectra[10]
    for specx in spectra:
        dic = specx.wcs.meta
        x1 = dic['dispersion0']
        x2 = specx.wcs(dic['pmin'])
        # np.testing.assert_allclose(x, y)
        y1 = dic['average_dispersion_delta']
        all = specx.wcs(np.arange(dic['pmin'], dic['pmax']+1))
        y2 = (all[1:] - all[:-1]).mean()
        kewlness = 100
        # np.testing.assert_allclose(x, y)

    np.testing.assert_allclose(iraf['wave'], spec.dispersion.value)
    assert spec.dispersion.unit == u.Angstrom

def test_multispec_chebyshev():
    iraf = ascii.read(data_path('AAO_11.txt'), data_start = 175, Reader = ascii.NoHeader, names = ['wave', 'flux'])
    spectra = read_fits.read_fits_spectrum1d(data_path('AAO.fits'))
    spec = spectra[10]
    for specx in spectra:
        dic = specx.wcs.meta
        x1 = dic['dispersion0']
        x2 = specx.wcs(dic['pmin'])
        # np.testing.assert_allclose(x, y)
        y1 = dic['average_dispersion_delta']
        all = specx.wcs(np.arange(dic['pmin'], dic['pmax']+1))
        y2 = (all[1:] - all[:-1]).mean()
        kewlness = 100
        # np.testing.assert_allclose(x, y)
    np.testing.assert_allclose(iraf['wave'], spec.wavelength.value)

def test_1dspec_UVES():
    spec = read_fits.read_fits_spectrum1d(data_path('UVES.fits'))
    iraf = ascii.read(data_path('uves_iraf_read_'
                                'truncated.dat'), names=['index', 'wave', 'flux'])
    np.testing.assert_allclose(spec.dispersion[iraf['index']], iraf['wave'])

    assert not hasattr(spec.dispersion, 'unit')

def test_1dspec_vrad():
    iraf = ascii.read(data_path('gbt_1d_iraf_read.dat'), names=['wave', 'flux'])
    spec = read_fits.read_fits_spectrum1d(data_path('gbt_1d.fits'))
    np.testing.assert_allclose(iraf['wave'], spec.dispersion.value)
    assert spec.dispersion.unit == u.Unit('km/s')
