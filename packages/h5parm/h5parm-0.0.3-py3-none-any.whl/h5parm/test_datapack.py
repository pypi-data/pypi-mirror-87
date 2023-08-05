from h5parm.utils import make_example_datapack
import numpy as np
import pytest

def test_datapack():
    datapack = make_example_datapack(4,5,6,["X"],clobber=True)
    phase,axes = datapack.phase
    datapack.phase = phase+1.
    phasep1, axes = datapack.phase
    assert np.all(np.isclose(phasep1, phase+1.))
    datapack.select(ant='RS509', time=slice(0,1,1))
    phase,axes = datapack.phase
    assert phase.shape == (1, 4, 1, 5, 1)
    datapack.select(ant='CS')
    phase, axes = datapack.phase
    assert phase.shape == (1, 4, 48, 5, 6)
    datapack.select(ant='RS*', time=slice(0, 1, 1))
    phase, axes = datapack.phase
    for  a in axes['ant']:
        assert b'RS' in a
    assert len(axes['ant']) == 14
    datapack.select(time=[1,3], dir=[0,1,3])
    phase, axes = datapack.phase
    with pytest.raises(IndexError):
        datapack.select(time=[0, 1, 3], dir=[0, 1, 3])
        phase, axes = datapack.phase
