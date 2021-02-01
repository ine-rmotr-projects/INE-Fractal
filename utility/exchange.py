from pickle import loads, dumps, dump
from datetime import datetime
from uuid import uuid4
import hashlib
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from gzip import GzipFile


@dataclass
class Fractal:
    canvas: np.ndarray = None
    timestamp: str = None
    uuid: str = None
    description: str = None
    hash_: str = None

    def __str__(self):
        return '\n'.join([
            f"Description: {self.description}",
            f"Timestamp:   {self.timestamp}",
            f"UUID:        {self.uuid}",
            f"Size:        {self.canvas.shape}",
            f"Fingerprint: {self.hash_}"])


def make_archive(canvas, comment="Archived Fractal"):
    if canvas.ndim != 2 or canvas.shape[0] != canvas.shape[1]:
        raise ValueError(f"Canvas must be 2-D and square, not {canvas.shape}")
    fractal = Fractal()
    fractal.canvas = canvas
    fractal.timestamp = datetime.now().isoformat()
    fractal.uuid = uuid4()
    fractal.description = comment
    fractal.hash_ = hashlib.sha1(dumps(canvas)).hexdigest()
    return fractal


def same_image(archive1, archive2):
    # Compare on only hashes if they exist in both archives
    # Use .get to substitute distinct values where missing
    if archive1.get('hash_', "A") == archive2.get('hash', "B"):
        return True
    # If we need to compare NumPy canvases, must use .all()
    elif (archive1.canvas == archive2.canvas).all():
        return True


def write_archive(canvas, comment=None, name=None):
    archive = Fractal(canvas=canvas,
                      timestamp=datetime.now().isoformat(),
                      uuid=uuid4(),
                      description=comment)
    if name is None:
        name = archive.description
    with GzipFile(f"{name}.pkl.gz", 'w') as gz:
        gz.write(dumps(archive))


def read_archive(name):
    with GzipFile(name) as gz:
        return loads(gz.read())