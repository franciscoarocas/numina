#
# Copyright 2008-2010 Sergio Pascual
# 
# This file is part of PyEmir
# 
# PyEmir is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyEmir is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyEmir.  If not, see <http://www.gnu.org/licenses/>.
# 


def to_json(obj):
    if hasattr(obj, '__getstate__'):
        dparam = obj.__getstate__()
    else:
        dparam = obj.__dict__
    return {'__class__': obj.__class__.__name__,
            '__module__': obj.__class__.__module__,
            '__value__': dparam,
            }

def from_json(obj):
    if '__class__' in obj and '__module__' in obj and '__value__' in obj:
        clsname = obj['__class__']
        modname = obj['__module__']
        _mod = __import__(modname, globals(), locals(), [clsname], -1)
        cls = getattr(_mod, clsname)
        result = super(type(cls), cls).__new__(cls)
        
        dparam = deunicode_json(obj['__value__'])
        if hasattr(result, '__setstate__'):
            result.__setstate__(dparam)
        else:
            result.__dict__ = dparam
        return result
    return obj

def deunicode_json(obj):
    '''Convert unicode strings into plain strings recursively.'''
    if isinstance(obj, dict):
        newobj = {}
        for key, value in obj.iteritems():
            newobj[str(key)] = deunicode_json(value)
        return newobj
    elif isinstance(obj, list):
        newobj = []
        for i in obj:
            newobj.append(deunicode_json(i))
        return newobj
    elif isinstance(obj, unicode):
        val = str(obj)
        if val.isdigit():
            val = int(val)
        else:
            try:
                val = float(val)
            except ValueError:
                val = str(val)
        return val
    
    return obj

