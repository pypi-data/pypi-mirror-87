import numpy as np
import logging
logger = logging.getLogger(__name__)
import os
from h5parm.datapack import DataPack
import astropy.time as at
import astropy.coordinates as ac
import astropy.units as au

def wrap(phi):
    """
    Wrap `phi` into (-pi, pi)
    Args:
        phi:

    Returns: wrapped phi
    """
    return (phi + np.pi) % (2 * np.pi) - np.pi

def make_example_datapack(Nd, Nf, Nt, pols=None,
                          save_name='test_datapack.h5',
                          clobber=False,
                          seed=0):
    """
    Create a H5Parm for testing
    Args:
        Nd: number of directions
        Nf: number of frequencies
        Nt: number of times
        pols: list of pols XX,XY,YY, etc.
        save_name: name of file to save to
        clobber: bool, whether to overwrite
        seed: int, numpy seed

    Returns: DataPack
    """
    TEC_CONV = -8.4479745e6  # mTECU/Hz
    np.random.seed(seed)

    logger.info("=== Creating example datapack ===")
    save_name = os.path.abspath(save_name)
    if os.path.isfile(save_name) and clobber:
        os.unlink(save_name)

    datapack = DataPack(save_name, readonly=False)
    with datapack:
        datapack.add_solset('sol000',array_file=datapack.lofar_array_hba)
        time0 = at.Time("2019-01-01T00:00:00.000", format='isot')
        altaz = ac.AltAz(location=datapack.array_center.earth_location, obstime=time0)
        up = ac.SkyCoord(alt=90.*au.deg,az=0.*au.deg,frame=altaz).transform_to('icrs')
        directions = np.stack([np.random.normal(up.ra.rad, np.pi / 180. * 3.5, size=[Nd]),
                               np.random.normal(up.dec.rad, np.pi / 180. * 3.5, size=[Nd])],axis=1)
        datapack.set_directions(None,directions)
        patch_names, _ = datapack.directions
        antenna_labels, _ = datapack.antennas
        _, antennas = datapack.get_antennas(antenna_labels)
        antennas = antennas.cartesian.xyz.to(au.km).value.T
        Na = antennas.shape[0]

        times = at.Time(time0.gps+np.arange(Nt)*30., format='gps').mjd * 86400.  # mjs
        freqs = np.linspace(120, 168, Nf) * 1e6
        if pols is not None:
            use_pols = True
            assert isinstance(pols, (tuple, list))
        else:
            use_pols = False
            pols = ['XX']
        Npol = len(pols)
        tec_conversion = TEC_CONV / freqs  # Nf

        dtecs = np.random.normal(0., 150., size=(Npol, Nd, Na, Nt))
        dtecs -= dtecs[:,:,0:1,:]

        phase = wrap(dtecs[...,None,:]*tec_conversion[:,None])# Npol, Nd, Na, Nf, Nt
        amp = np.ones_like(phase)

        datapack.add_soltab('phase000', values=phase, ant=antenna_labels, dir = patch_names, time=times, freq=freqs, pol=pols)
        datapack.add_soltab('amplitude000', values=amp, ant=antenna_labels, dir = patch_names, time=times, freq=freqs, pol=pols)
        datapack.add_soltab('tec000', values=dtecs, ant=antenna_labels, dir = patch_names, time=times, pol=pols)
        return datapack

def make_soltab(datapack:DataPack, from_solset='sol000', to_solset='sol000', from_soltab='phase000', to_soltab='tec000',
                select=None, directions=None, patch_names=None, remake_solset=False, to_datapack=None):
    """
    Adds a new soltab to the h5parm with a soltab copying over structure from preexisting solset/soltab.
    Args:
        datapack: DataPack to alter, should be writable.
        from_solset: solset to copy from
        to_solset: solset to copy to/create
        from_soltab: soltab to copy structure from
        to_soltab: soltab to copy to
        select: dict, axes section, or None
        directions: ICRS of directions, or None to copy over (useful for adding extra directions but keep else the same)
        patch_names: patch_names corresponding to directions, or None
        remake_solset: bool, whether to forcefully delete the solset and remake.
        to_datapack: output datapack file to make
    """
    if not isinstance(to_soltab, (list, tuple)):
        to_soltab = [to_soltab]
    if select is None:
        select = dict(ant=None, time=None, dir=None, freq=None, pol=slice(0, 1, 1))

    if isinstance(datapack, str):
        datapack = DataPack(datapack)

    with datapack:
        datapack.current_solset = from_solset
        datapack.select(**select)
        axes = getattr(datapack, "axes_{}".format(from_soltab.replace('000', '')))
        antenna_labels, antennas = datapack.get_antennas(axes['ant'])
        _patch_names, _directions = datapack.get_directions(axes['dir'])
        if (directions is None):
            directions = _directions
        if (patch_names is None):
            patch_names = _patch_names
        if len(patch_names) != len(directions):
            patch_names = ['Dir{:02d}'.format(d) for d in range(len(directions))]
        timestamps, times = datapack.get_times(axes['time'])
        freq_labels, freqs = datapack.get_freqs(axes['freq'])
        pol_labels, pols = datapack.get_pols(axes['pol'])
        Npol, Nd, Na, Nf, Nt = len(pols), len(directions), len(antennas), len(freqs), len(times)
    if to_datapack is None:
        to_datapack = datapack.filename
    if isinstance(to_datapack, DataPack):
        to_datapack = to_datapack.filename
    with DataPack(to_datapack) as datapack:
        if remake_solset:
            if to_solset in datapack.solsets:
                datapack.delete_solset(to_solset)
        if to_solset not in datapack.solsets:
            datapack.add_solset(to_solset,
                                array_file=DataPack.lofar_array_hba,
                                directions=np.stack([directions.ra.to(au.rad).value,
                                                     directions.dec.to(au.rad).value], axis=1),
                                patch_names=patch_names)
        if 'tec000' in to_soltab:
            datapack.add_soltab('tec000', weightDtype='f16', time=times.mjd * 86400., pol=pol_labels,
                                ant=antenna_labels,
                                dir=patch_names)
        if 'clock000' in to_soltab:
            datapack.add_soltab('clock000', weightDtype='f16', time=times.mjd * 86400., pol=pol_labels,
                                ant=antenna_labels, dir=patch_names)
        if 'const000' in to_soltab:
            datapack.add_soltab('const000', weightDtype='f16', time=times.mjd * 86400., pol=pol_labels,
                                ant=antenna_labels, dir=patch_names)
        if 'phase000' in to_soltab:
            datapack.add_soltab('phase000', weightDtype='f16', freq=freqs, time=times.mjd * 86400., pol=pol_labels,
                                ant=antenna_labels, dir=patch_names)
        if 'amplitude000' in to_soltab:
            datapack.add_soltab('amplitude000', weightDtype='f16', freq=freqs, time=times.mjd * 86400., pol=pol_labels,
                                ant=antenna_labels, dir=patch_names)