"""Tests functions in the utilities module.

"""
import os
import unittest
from thornpy import utilities
from test import *

class Test_Utilities(unittest.TestCase):

    def setUp(self):
        return

    def test_num_to_ith(self):
        ordinals = [utilities.num_to_ith(num) for num in TEST_INTEGERS]
        self.assertEqual(ordinals, TEST_EXPECTED_ORDINALS)

    def test_read_data_string_with_headers(self):
        data = utilities.read_data_string(TEST_DATA_STRING)
        self.assertListEqual(data, TEST_EXPECTED_DATA_DICT_WITH_HEADERS)

    def test_read_data_string_without_headers(self):
        data = utilities.read_data_string(TEST_DATA_STRING, has_headerline=False)
        self.assertListEqual(data, TEST_EXPECTED_DATA_DICT_WITHOUT_HEADERS)
    
    def test_convert_path_windows(self):
        """Tests that utilities.convert_path works as expected.

        """
        filepath = 'home/thorn241/test'
        converted_filepath = utilities.convert_path(filepath)
        expected_converted_filepath = os.path.join('home', 'thorn241', 'test')
        self.assertEqual(converted_filepath, expected_converted_filepath)        

    def tearDown(self):
        return
        