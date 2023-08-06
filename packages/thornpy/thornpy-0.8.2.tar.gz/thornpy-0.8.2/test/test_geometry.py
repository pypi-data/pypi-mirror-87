import os
import unittest

import matplotlib.pyplot as plt
from thornpy import geometry

class Test_GetArcArcPoints2(unittest.TestCase):

    def setUp(self):        
        return

    def test_get_arc_arc_points2(self):
        x_0 = -34
        y_0 = 28
        x_1 = -53
        y_1 = 56
        x_prev = -0
        y_prev = 0
        r_0 = 29
        end_angle = 0.02

        x_arc, y_arc, x_ca, y_ca, x_tan, y_tan, start_angle, i_center, x_cb, y_cb, r_b = geometry.get_arc_arc_points2(x_0, y_0, x_1, y_1, x_prev, y_prev, r_0, end_angle)

        plt.plot(x_arc, y_arc)
        plt.scatter(x_tan, y_tan, c='g')
        plt.scatter(x_prev, y_prev, c='k')
        plt.scatter(x_0, y_0, c='r')
        plt.scatter(x_1, y_1, c='r')
        plt.scatter(x_ca, y_ca, c='k', marker='+')
        plt.scatter(x_cb, y_cb, c='k', marker='+')
        plt.axis('square')
        plt.grid()

        plt.show()
        
        self.assertEqual(0,1)

    def tearDown(self):
        return