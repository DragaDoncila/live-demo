import os
from shutil import make_archive, rmtree
from typing import Any, Dict, List
from napari.qt import thread_worker
from tifffile import imsave
import numpy as np

def write_single_labels(path: str, data: Any, meta: dict):
    if str(path).endswith(".zip"):
        path = str(path)[:-4]
    if not data.ndim == 3:
        return None

    @thread_worker()
    def write_tiffs(data, dir_pth):
        for i, t_slice in enumerate(data):
            tiff_nme = f"seg{str(i).zfill(3)}.tif"
            tiff_pth = os.path.join(dir_pth, tiff_nme)
            imsave(tiff_pth, t_slice)

    def zip_dir():
        make_archive(path, "zip", path)
        rmtree(path)

    os.mkdir(path)
    layer_dir_pth = os.path.join(path, f"01_AUTO/SEG")
    os.makedirs(layer_dir_pth)
    if len(data.shape) == 2:
        data = [data]
    worker = write_tiffs(data, layer_dir_pth)
    worker.start()
    worker.finished.connect(zip_dir)
    return path + ".zip"
