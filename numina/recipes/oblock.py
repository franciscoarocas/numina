#
# Copyright 2008-2012 Universidad Complutense de Madrid
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

'''
Results of the Observing Blocks 
'''


class FrameInformation(object):
    def __init__(self):
        self.label = None
        self.object = None
        self.target = None
        self.itype = None
        self.exposure = 0.0
        self.ra = 0.0
        self.dec = 0.0
        self.mdj = 0.0
        self.airmass = 1.0

class ObservingResult(object):
    def __init__(self):
        self.id = None
        self.mode = None
        self.instrument = None
        self.frames = [] # list of FrameInformation
        self.children = [] # other ObservingResult
        

def frameinfo_from_list(values):
    # FIXME: modify when format is changed
    # For this format
    # [r0007.fits, M 33, 10.0, TARGET, 23.4620835, 30.66027777]
    frameinfo = FrameInformation()
    frameinfo.label = values[0]
    frameinfo.object = values[1]
    frameinfo.exposure = values[2]
    frameinfo.itype = values[3]
    frameinfo.ra = values[4]
    frameinfo.dec = values[5]
    return frameinfo

def obsres_from_dict(values):
    
    obsres = ObservingResult()
    
    obsres.id = values['id']
    obsres.mode = values['mode']
    obsres.instrument = values['instrument']
    obsres.frames = [frameinfo_from_list(val) for val in values['frames']]
    
    return obsres
