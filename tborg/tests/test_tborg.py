#
# tborg/tests/test_tborg.py
#
from __future__ import absolute_import

import os
import logging
import unittest

try:
    from unittest.mock import patch
except:
    from mock import patch

from tborg import ConfigLogger, ThunderBorgException, ThunderBorg

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', 'logs'))
not os.path.isdir(LOG_PATH) and os.mkdir(LOG_PATH, 0o0775)


class BaseTest(unittest.TestCase):
    LOGGER_NAME = 'thunder-borg'

    def __init__(self, name, filename=None):
        super(BaseTest, self).__init__(name)
        cl = ConfigLogger(log_path=LOG_PATH)
        cl.config(logger_name=self.LOGGER_NAME, filename=filename,
                  level=logging.DEBUG)


class TestNoSetUp(BaseTest):
    _LOG_FILENAME = 'tb-no-setup-method.log'

    def __init__(self, name):
        super(TestNoSetUp, self).__init__(
            name, filename=self._LOG_FILENAME)

    @patch.object(ThunderBorg, '_DEFAULT_I2C_ADDRESS', 0x20)
    #@unittest.skip("Temporarily skipped")
    def test_find_address_with_invalid_default_address(self):
        """
        Test that an invalid default address will cause a board to be
        initialized if the `auto_set_addr` argument is `True`.
        """
        default_address = 0x15
        tb = ThunderBorg(logger_name=self.LOGGER_NAME,
                         log_level=logging.DEBUG,
                         auto_set_addr=True)
        boards = ThunderBorg.find_board()
        msg = "Boards found: {}".format(boards)
        self.assertEquals(tb._DEFAULT_I2C_ADDRESS, 0x20, msg)
        self.assertTrue(len(boards) > 0, msg)
        self.assertEqual(boards[0], default_address, msg)


class TestClassMethods(BaseTest):
    _LOG_FILENAME = 'tb-class-method.log'

    def __init__(self, name):
        super(TestClassMethods, self).__init__(
            name, filename=self._LOG_FILENAME)

    def tearDown(self):
        ThunderBorg.set_i2c_address(ThunderBorg._DEFAULT_I2C_ADDRESS)

    #@unittest.skip("Temporarily skipped")
    def test_find_board(self):
        """
        Test that the ThunderBorg.find_board() method finds a board.
        """
        found = ThunderBorg.find_board()
        found = found[0] if found else None
        msg = "Found address '0x{:02X}', should be address '0x{:02X}'.".format(
            found, ThunderBorg._DEFAULT_I2C_ADDRESS)
        self.assertEqual(found, ThunderBorg._DEFAULT_I2C_ADDRESS, msg)

    #@unittest.skip("Temporarily skipped")
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

    #@unittest.skip("Temporarily skipped")
    def test_set_i2c_address_with_current_address(self):
        """
        Test that the ThunderBorg.set_i2c_address() can set a different
        address. The current address is provided.
        """
        # Set a new address
        new_addr = 0x70
        cur_addr = ThunderBorg._DEFAULT_I2C_ADDRESS
        ThunderBorg.set_i2c_address(new_addr, cur_addr=cur_addr)
        found = ThunderBorg.find_board()
        found = found[0] if found else 0
        msg = "Found address '0x{:02X}', should be '0x{:02X}'.".format(
            found, new_addr)
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




