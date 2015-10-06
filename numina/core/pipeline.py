#
# Copyright 2011-2014 Universidad Complutense de Madrid
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

"""DRP loader and related classes"""

import warnings
import pkg_resources


class Pipeline(object):
    """Base class for pipelines."""
    def __init__(self, name, recipes, version=1):
        self.name = name
        self.recipes = recipes
        self.version = version

    def get_recipe(self, mode):
        return self.recipes[mode]


class InstrumentConfiguration(object):
    """Configuration of an Instrument."""
    def __init__(self, values):
        self.values = values


class Instrument(object):
    """Description of an Instrument."""
    def __init__(self, name, configurations, modes, pipelines, products=None):
        self.name = name
        self.configurations = configurations
        self.modes = modes
        self.pipelines = pipelines
        self.products = products
        if products is None:
            self.products = []


class ObservingMode(object):
    """Observing modes of an Instrument."""
    def __init__(self):
        self.name = ''
        self.uuid = ''
        self.key = ''
        self.url = ''
        self.instrument = ''
        self.summary = ''
        self.description = ''
        self.status = ''
        self.date = ''
        self.reference = ''
        self.tagger = None


class LoadableDRP(object):
    """Container for the loaded DRP."""
    def __init__(self, instruments):
        self.instruments = instruments


class DrpSystem(object):
    """Load DRPs from the system."""

    ENTRY = 'numina.pipeline.1'

    def __init__(self):

        # Store queried DRPs
        self._drp_cache = {}

    def query_by_name(self, name):
        """Cached version of 'query_drp_system'"""
        if name in self._drp_cache:
            return self._drp_cache[name]
        else:
            drp = self._query_by_name(name)
            if drp is None:
                return drp
            else:
                self._drp_cache[name] = drp
                return drp

    def _query_by_name(self, name):
        """Load a DRPs in 'numina.pipeline' entry_point by name"""

        for entry in pkg_resources.iter_entry_points(group=DrpSystem.ENTRY):
            if entry.name == name:
                drp_loader = entry.load()
                mod = drp_loader()

                if mod:
                    return mod.instruments[name]
                else:
                    warnings.warn('Module {0} does not contain a valid DRP'.format(mod), RuntimeWarning)
        else:
            return None

    def query_all(self):
        """Return all available DRPs in 'numina.pipeline' entry_point."""

        drp = {}

        for entry in pkg_resources.iter_entry_points(group=DrpSystem.ENTRY):
            drp_loader = entry.load()
            mod = drp_loader()
            if mod:
                drp.update(mod.instruments)
            else:
                warnings.warn('Module {0} does not contain a valid DRP'.format(mod), RuntimeWarning)

        # Update cache
        self._drp_cache = drp

        return drp


def init_store_backends(backend='default'):
    """Load storage backends."""

    for entry in pkg_resources.iter_entry_points(group='numina.storage.1'):
        store_loader = entry.load()
        store_loader()


init_dump_backends = init_store_backends
