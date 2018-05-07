#
# tborg/tests/test_tborg.py
#
from __future__ import absolute_import

import os
import logging
import unittest

from tborg import ConfigLogger, ThunderBorgException, ThunderBorg

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', 'logs'))
not os.path.isdir(LOG_PATH) and os.mkdir(LOG_PATH, 0o0775)


class BaseTest(unittest.TestCase):

    def __init__(self, name, filename=None):
        super(BaseTest, self).__init__(name)
        cl = ConfigLogger(log_path=LOG_PATH)
        cl.config(logger_name='thunder-borg', filename=filename,
                  level=logging.DEBUG)


class TestClassMethods(BaseTest):
    _LOG_FILENAME = 'tb-class_method.log'

    def __init__(self, name):
        super(TestClassMethods, self).__init__(
            name, filename=self._LOG_FILENAME)

    def setUp(self):
        # Reset board address to default.
        tb = ThunderBorg()
        tb._write(tb.COMMAND_SET_I2C_ADD, [tb._I2C_ID_THUNDERBORG])
        tb.close_streams()

    def test_find_board(self):
        """
        Test that the ThunderBorg.find_board() method finds a board.
        """
        found = ThunderBorg.find_board()
        found = found[0] if found else None
        msg = "Found address '{}', should be address '{}'.".format(
            found, ThunderBorg._I2C_ID_THUNDERBORG)
        self.assertEqual(found, ThunderBorg._I2C_ID_THUNDERBORG, msg)

    def test_set_i2c_address_without_current_address(self):
        """
        Test that the ThunderBorg.set_i2c_address() can set a different
        address. Scans address range to find current address.
        """
        # Set a new address
        new_addr = 0x70
        ThunderBorg.set_i2c_address(new_addr)
        found = ThunderBorg.find_board()
        found = found[0] if found else None
        msg = "Found address '{}', should be '{}'.".format(found, new_addr)
        self.assertEqual(found, new_addr, msg)

    def test_set_i2c_address_with_current_address(self):
        """
        Test that the ThunderBorg.set_i2c_address() can set a different
        address. The current address is provided.
        """
        # Set a new address
        new_addr = 0x70
        cur_addr = ThunderBorg._I2C_ID_THUNDERBORG
        ThunderBorg.set_i2c_address(new_addr, cur_addr=cur_addr)
        found = ThunderBorg.find_board()
        found = found[0] if found else None
        msg = "Found address '{}', should be '{}'.".format(found, new_addr)
        self.assertEqual(found, new_addr, msg)




class TestThunderBorg(BaseTest):
    _LOG_FILENAME = 'tb-instance.log'

    def __init__(self, name):
        super(TestThunderBorg, self).__init__(
            name, filename=self._LOG_FILENAME)

    def setUp(self):
        self._log.debug("Processing")
        self._tb = ThunderBorg()

    def tearDown(self):
        self._tb.halt_motors()
        self.close_streams()




