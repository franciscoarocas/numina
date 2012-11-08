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

import unittest

import numpy

from numina.array.nirproc import ramp_array

class FollowUpTheRampTestCase(unittest.TestCase):
    def setUp(self):
        self.ramp = numpy.empty((1, 1, 10))
        self.sdt = 1.0
        self.sgain = 1.0
        self.sron = 1.0
    
    def test_exception(self):
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, -1.0, self.sron)
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, 0, self.sron)
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, self.sgain, -1.0)
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, self.sgain, self.sron, nsig=-1.0)
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, self.sgain, self.sron, nsig=0)
        self.assertRaises(ValueError, ramp_array, self.ramp, -1.0, self.sgain, self.sron, nsig=-1.0)
        self.assertRaises(ValueError, ramp_array, self.ramp, 0.0, self.sgain, self.sron, nsig=-1.0)
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, self.sgain, self.sron, saturation=-100)
        self.assertRaises(ValueError, ramp_array, self.ramp, self.sdt, self.sgain, self.sron, saturation=0)

class RampReadoutAxisTestCase(unittest.TestCase):
    
    def setUp(self):
        rows = 3
        columns = 4
        self.emptybp = numpy.zeros((rows, columns), dtype='uint8')
        self.data = numpy.arange(10, dtype='int32')
        self.data = numpy.tile(self.data, (rows, columns, 1))

        self.saturation = 65536
        self.dt = 1.0
        self.gain = 1.0
        self.ron = 1.0
        self.nsig = 4.0
        self.blank = 0

    def test_saturation0(self):        
        '''Test we count correctly saturated pixels in RAMP mode.'''
        
        MASK_SATURATION = 3
    
        # Nno points 
        self.data[:] = 50000 #- 32768
        saturation = 40000 #- 32767
        
        res = ramp_array(self.data, self.dt, self.gain, self.ron,
                    saturation=saturation, 
                    nsig=self.nsig, 
                    blank=self.blank)

        for nn in res[2].flat:
            self.assertEqual(nn, 0)

        for n in res[3].flat:
            self.assertEqual(n, MASK_SATURATION)
            
        for v in res[1].flat:
            self.assertEqual(v, 0)
            
        for v in res[0].flat:
            self.assertEqual(v, self.blank)
            

    def test_saturation1(self):        
        '''Test we count correctly saturated pixels in RAMP mode.'''
        
        MASK_GOOD = 0
            
        saturation = 50000
        self.data[..., 7:] = saturation 
        
        res = ramp_array(self.data, self.dt, self.gain, self.ron,
                    saturation=saturation, 
                    nsig=self.nsig, 
                    blank=self.blank)

        for nn in res[2].flat:
            self.assertEqual(nn, 7)

        for n in res[3].flat:
            self.assertEqual(n, MASK_GOOD)
            
        for v in res[1].flat:
            self.assertEqual(v, 0.2142857142857143)
            
        for v in res[0].flat:
            self.assertEqual(v, 1)
            
            
        
    def test_badpixel(self):
        '''Test we ignore badpixels in RAMP mode.'''
        self.emptybp[...] = 1

        res = ramp_array(self.data, self.dt, self.gain, self.ron,
                    saturation=self.saturation, 
                    nsig=self.nsig, 
                    badpixels=self.emptybp,
                    blank=self.blank)

        for nn in res[2].flat:
            self.assertEqual(nn, 0)

        for n in res[3].flat:
            self.assertEqual(n, 1)
            
        for v in res[1].flat:
            self.assertEqual(v, 0)
            
        for v in res[0].flat:
            self.assertEqual(v, self.blank)
            
    def test_results1(self):
        '''Test we obtain correct values in RAMP mode'''
        
        res = ramp_array(self.data, self.dt, self.gain, self.ron,
                    saturation=self.saturation, 
                    nsig=self.nsig, 
                    blank=self.blank)

        for nn in res[2].flat:
            self.assertEqual(nn, 10)

        for n in res[3].flat:
            self.assertEqual(n, 0)
            
        for v in res[1].flat:
            self.assertEqual(v, 0.13454545454545455)
            
        for v in res[0].flat:
            self.assertEqual(v, 1.0)
            
    def test_results2(self):
        '''Test we obtain correct values in RAMP mode'''

        self.data *= 12
        self.data[1,1,:] = 70000
        self.data[2,2,5:] += 1300

        self.emptybp[0,0] = 1
        
        res = ramp_array(self.data, self.dt, self.gain, self.ron,
                    dtype='float32',
                    saturation=self.saturation, 
                    badpixels=self.emptybp,
                    nsig=self.nsig, 
                    blank=self.blank)

        res0 = 12 * numpy.ones((3,4), dtype='float32')
        res0[0,0] = 0
        res0[1,1] = 0
        res1 = 1.4812121212 * numpy.ones((3,4), dtype='float32')
        res1[0,0] = 0
        res1[1,1] = 0
        res1[2,2] = 1.61
        res2 = 10 * numpy.ones((3,4), dtype='uint8')
        res2[0,0] = 0
        res2[1,1] = 0
        res3 = numpy.zeros((3,4), dtype='uint8')
        res3[0,0] = 1
        res3[1,1] = 3
        res4 = numpy.zeros((3,4), dtype='uint8')
        res4[2,2] = 5

        for xx,yy in zip(res[0].flat, res0.flat):
            self.assertAlmostEqual(xx, yy)
        for xx,yy in zip(res[1].flat, res1.flat):
            self.assertAlmostEqual(xx, yy)
        for xx,yy in zip(res[2].flat, res2.flat):
            self.assertEqual(xx, yy)
        for xx,yy in zip(res[3].flat, res3.flat):
            self.assertEqual(xx, yy)
        for xx,yy in zip(res[4].flat, res4.flat):
            self.assertEqual(xx, yy)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FollowUpTheRampTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
