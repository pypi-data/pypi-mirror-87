import os
import unittest

from pandas import read_csv
import matplotlib.pylab as plt

from thornpy.signal import fft_watefall

DATA_FILENAME = os.path.join(os.getcwd(), 'test', 'files', 'waterfall', 'LC3_aluminum_pt1_accel_X.csv')

class Test_Waterfall(unittest.TestCase):

    # def setUp(self):        
    #     self.wtrfl, self.time, self.rpm, self.sig, self.order_cut_plots = self._make_plots('linear')

    def test_order_plots_human_approval(self):
        plt.show()
        self.assertTrue(True)

    def test_db(self):
        _wtrfl_db, _time_db, _rpm_db, _sig_db, _order_cut_plots_db = self._make_plots('dB')
        plt.show()
        self.assertTrue(False)

    def test_db_vmin_vmax(self):
        vmin = -100
        vmax = -5  
        _wtrfl_db, _time_db, _rpm_db, _sig_db, _order_cut_plots_db = self._make_plots('dB', vmin=vmin, vmax=vmax)
        plt.show()
        self.assertTrue(False)

    def tearDown(self):
        return

    def _make_plots(self, z_scale, vmin=None, vmax=None):
        time, rpm, response = _get_data()
        return fft_watefall(time, response, percent_overlap=75, n_fft=1024, t_min=6.25, t_max=10, z_scale=z_scale, f_range=[0, 500], return_order_cuts=[1, 40, 63, 80], order_lines=[1, 40, 63, 80], input_sig=rpm, input_conversion_factor=1, response_unit='g', vmin=vmin, vmax=vmax)

def _get_data():
    data = read_csv(DATA_FILENAME)
    
    time = list(data['Time (s)'])
    rpm = list(data['Shaft Speed (rpm)'])
    response = list(data['Response (g)'])

    return time, rpm, response