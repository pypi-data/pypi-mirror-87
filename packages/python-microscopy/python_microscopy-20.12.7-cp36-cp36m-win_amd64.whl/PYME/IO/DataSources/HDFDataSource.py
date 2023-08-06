#!/usr/bin/python

##################
# HDFDataSource.py
#
# Copyright David Baddeley, 2009
# d.baddeley@auckland.ac.nz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################

from PYME.IO.FileUtils.nameUtils import getFullExistingFilename
import tables
from .BaseDataSource import BaseDataSource
import numpy as np

try:
    from PYME.IO import PZFFormat
except ImportError:
    pass

class DataSource(BaseDataSource):
    moduleName = 'HDFDataSource'
    def __init__(self, h5Filename, taskQueue=None):
        self.h5Filename = getFullExistingFilename(h5Filename)#convert relative path to full path
        self.h5File = tables.open_file(self.h5Filename)
        
        self._pzf_index = None

        
        if getattr(self.h5File.root, 'PZFImageIndex', False):
            self.usePZFFormat = True
            try:
                self.framesize = self.h5File.root.PZFImageData.attrs.framesize
            except AttributeError:
                self.framesize = PZFFormat.loads(self.h5File.root.PZFImageData[0])[0].squeeze().shape
        else:
            self.usePZFFormat = False

    def getSlice(self, ind):
        if self.usePZFFormat:
            if ind >= self.h5File.root.PZFImageData.shape[0]:
                self.reloadData() #try
                
            if not self.pzf_index is None:
                ind = self.pzf_index['Position'][np.searchsorted(self.pzf_index['FrameNum'], ind)]
            
            return PZFFormat.loads(self.h5File.root.PZFImageData[ind])[0].squeeze() 
        else:       
            if ind >= self.h5File.root.ImageData.shape[0]:
                    self.reloadData() #try reloading the data in case it's grown
            
            return self.h5File.root.ImageData[ind, :,:]

    @property
    def pzf_index(self):
        if self._pzf_index is None:
            try:
                pi = getattr(self.h5File.root, 'PZFImageIndex')[:]
                self._pzf_index = np.sort(pi, order='FrameNum')
            except AttributeError:
                pass
    
        return self._pzf_index


    def getSliceShape(self):
        if self.usePZFFormat:
            return self.framesize
        else:
            return self.h5File.root.ImageData.shape[1:3]

    def getNumSlices(self):
        if self.usePZFFormat:
            return self.h5File.root.PZFImageData.shape[0]
        else:
            return self.h5File.root.ImageData.shape[0]

    def getEvents(self):
        try:
            return self.h5File.root.Events[:]
        except AttributeError:
            return []

    def release(self):
        self.h5File.close()

    def reloadData(self):
        self.h5File.close()
        self.h5File = tables.open_file(self.h5Filename)
