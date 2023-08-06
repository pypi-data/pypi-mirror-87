
import unittest
# import unittest2 as unittest # for versions of python < 2.7

"""
        Method                            Checks that
self.assertEqual(a, b)                      a == b   
self.assertNotEqual(a, b)                   a != b   
self.assertTrue(x)                          bool(x) is True  
self.assertFalse(x)                         bool(x) is False     
self.assertIs(a, b)                         a is b
self.assertIsNot(a, b)                      a is not b
self.assertIsNone(x)                        x is None 
self.assertIsNotNone(x)                     x is not None 
self.assertIn(a, b)                         a in b
self.assertNotIn(a, b)                      a not in b
self.assertIsInstance(a, b)                 isinstance(a, b)  
self.assertNotIsInstance(a, b)              not isinstance(a, b)  
self.assertAlmostEqual(a, b, places=5)      a within 5 decimal places of b
self.assertNotAlmostEqual(a, b, delta=0.1)  a is not within 0.1 of b
self.assertGreater(a, b)                    a is > b
self.assertGreaterEqual(a, b)               a is >= b
self.assertLess(a, b)                       a is < b
self.assertLessEqual(a, b)                  a is <= b

for expected exceptions, use:

with self.assertRaises(Exception):
    blah...blah...blah

with self.assertRaises(KeyError):
    blah...blah...blah

Test if __name__ == "__main__":
    def test__main__(self):
        # loads and runs the bottom section: if __name__ == "__main__"
        runpy = imp.load_source('__main__', os.path.join(up_one, 'filename.py') )


See:
      https://docs.python.org/2/library/unittest.html
         or
      https://docs.python.org/dev/library/unittest.html
for more assert options
"""

import sys, os
import imp


from rocketisp.rocket_isp import RocketThruster
from rocketisp.geometry import Geometry
from rocketisp.stream_tubes import CoreStream
from rocketisp.efficiencies import Efficiencies
import rocketisp.rocket_isp

class MyTest(unittest.TestCase):


    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass


    def test_overall_Isp_efficiency(self):
        """test overall Isp efficiency"""
        
        R = RocketThruster(name='overall_Isp_efficiency' )
        R.set_eff_model( eff_name='Div', model_name='simple fit')
        R.scale_Rt_to_Thrust( ThrustLbf=400.0, Pamb=0.0, use_scipy=False)
        #R.summ_print()
        self.assertAlmostEqual(R.coreObj.effObj('Isp'), 0.96889, places=3)
        self.assertAlmostEqual(R.coreObj.effObj('BL'), 0.992297, places=3)
        
        self.assertAlmostEqual(R('pulse_quality'), 0.8, places=3)
        
        R.scale_Rt_to_Thrust( ThrustLbf=500.0, Pamb=0.0, use_scipy=False)
        self.assertAlmostEqual(R.coreObj.Fambient, 500, places=3)
        
        R.scale_Rt_to_Thrust( ThrustLbf=500.0, Pamb=0.0, use_scipy=True)
        self.assertAlmostEqual(R.coreObj.Fambient, 500, places=3)

        R.set_eff_model( eff_name='BL', model_name='NASA-SP8120')
        R.noz_regen_eps = 6
        R.scale_Rt_to_Thrust( ThrustLbf=400.0, Pamb=0.0, use_scipy=False)
        #R.summ_print()
        self.assertAlmostEqual(R.coreObj.effObj('Isp'), 0.969825, places=3)
        self.assertAlmostEqual(R.coreObj.effObj('BL'), 0.993258, places=3)

    
    def test__main__(self):
        old_sys_argv = list(sys.argv)
        sys.argv = list(sys.argv)
        sys.argv.append('suppress_show')
        
        try:
            #runpy = imp.load_source('__main__', os.path.join(up_one, 'rocket_isp.py') )
            if 'TRAVIS' not in os.environ:
                runpy = imp.load_source('__main__',  rocketisp.rocket_isp.__file__)
        except:
            raise Exception('ERROR... failed in __main__ routine')
        finally:
            sys.argv = old_sys_argv


        

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

