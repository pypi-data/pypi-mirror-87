import unittest
from thornpy.plotting import plot_3d
import matplotlib.pyplot as plt

class Test_Plotting(unittest.TestCase):

    def setUp(self):
        return

    def test_plot_3d(self):
        x = [1,2,3,4,5]
        y = [10, 15, 20, 15, 10]
        z = [0, 0, 0, 0, 0]
        figure = plot_3d(x, y, z)
        plt.show()
        
        self.assertEqual(0,1)

    def tearDown(self):
        return