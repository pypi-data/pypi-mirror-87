import unittest
from thornpy.mechanics import contact

class Test_Contact(unittest.TestCase):

    def setUp(self):
        return

    def test_spherical(self):
        k, e = contact.spherical(2, None, 30000000, 30000000, .3, .3)
        self.assertAlmostEqual(k, 31081616.7554, 3)

    def tearDown(self):
        return

