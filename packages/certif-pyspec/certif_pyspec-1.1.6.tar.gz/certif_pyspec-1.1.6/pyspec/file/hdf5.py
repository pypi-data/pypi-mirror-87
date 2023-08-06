
import h5py

class H5Writer(object):
    def __init__(self):
        self._ofd = None
   
    def h5_open(self, filename, metadata=None, overwrite=False, append=True):
        pass
     
    def h5_save(self, data, filename, metadata=None):
        with self.h5_open(filename) as _ofd:
             _ofd.create_dataset("/entry/data/data")
