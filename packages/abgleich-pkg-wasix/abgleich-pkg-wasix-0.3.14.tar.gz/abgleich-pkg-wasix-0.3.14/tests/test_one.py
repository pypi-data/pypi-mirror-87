#!/usr/bin/python3
'''test for module'''

import unittest

from unittest import TestCase
from multiprocessing import freeze_support

from abgleich_pkg.abgleich \
    import setlogging, prepareParams, checkDebugEnv, printGlobals


class TestJoke(TestCase):
    ''' test class'''
    def test_is_string(self):
        '''test func'''

        # for windows in combination with pool.map
        freeze_support()

        # define logging
        setlogging()

        # debugger-env with defaults
        checkDebugEnv()
        printGlobals()

        teststr = 'ich bin ein String'
        self.assertTrue(isinstance(teststr, str))


if __name__ == '__main__':
    unittest.main()
