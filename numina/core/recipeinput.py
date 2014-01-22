#
# Copyright 2008-2014 Universidad Complutense de Madrid
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

from numina.core import RequirementParser

class RecipeInput(object):
    '''The input of a Recipe'''
    def __init__(self, observation_result, requirements):
        self.observation_result = observation_result
        self.requirements = requirements

class RecipeInputBuilder(object):

    def build(self, klass, observation_result, mreqs):
        rp = RequirementParser(klass)
        requires = rp.parse(mreqs, validate=False)
        return RecipeInput(observation_result, requires)

