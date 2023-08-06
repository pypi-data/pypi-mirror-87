from seismic_zfp.read import SgzReader
from seismic_zfp.utils import get_correlated_diagonal_length
import segyio
import time
import os
import sys

from PIL import Image
import numpy as np
from matplotlib import cm

base_path = sys.argv[1]
LINE_NO = int(sys.argv[2])

CLIP = 0.2
SCALE = 1.0/(2.0*CLIP)

with SgzReader(os.path.join(base_path, '0.sgz')) as reader:
    t0 = time.time()
    slice_sgz = reader.read_correlated_diagonal(LINE_NO)
    print("SgzReader took", time.time() - t0)


im = Image.fromarray(np.uint8(cm.seismic((slice_sgz.T.clip(-CLIP, CLIP) + CLIP) * SCALE)*255))
im.save(os.path.join(base_path, 'out_cd-sgz.png'))


with segyio.open(os.path.join(base_path, '0.sgy')) as segyfile:
    t0 = time.time()
    diagonal_length = get_correlated_diagonal_length(LINE_NO, len(segyfile.ilines), len(segyfile.xlines))
    slice_segy = np.zeros((diagonal_length, len(segyfile.samples)))
    if LINE_NO >= 0:
        for d in range(diagonal_length):
            slice_segy[d, :] = segyfile.trace[(d+LINE_NO)*len(segyfile.xlines) + d]
    else:
        for d in range(diagonal_length):
            slice_segy[d, :] = segyfile.trace[d*len(segyfile.xlines) + d - LINE_NO]
    print("segyio took", time.time() - t0)

im = Image.fromarray(np.uint8(cm.seismic((slice_segy.T.clip(-CLIP, CLIP) + CLIP) * SCALE)*255))
im.save(os.path.join(base_path, 'out_cd-sgy.png'))

im = Image.fromarray(np.uint8(cm.seismic(((slice_segy-slice_sgz).T.clip(-CLIP, CLIP) + CLIP) * SCALE)*255))
im.save(os.path.join(base_path, 'out_cd-dif.png'))
