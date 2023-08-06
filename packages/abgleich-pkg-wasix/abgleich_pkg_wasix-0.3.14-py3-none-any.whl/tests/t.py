#!/usr/bin/python3

import os, unittest

from unittest import TestCase, main
from multiprocessing import Pool, freeze_support, cpu_count

from abgleich_pkg.abgleich import *

class TestJoke(TestCase):
    def test_is_string(self):

        #for windows in combination with pool.map
        freeze_support()

        #define logging
        setlogging()

        # commandline params handling
        prepareParams()

        #debugger-env with defaults
        checkDebugEnv()
        printGlobals()


        s = 'ich bin ein String' 
        self.assertTrue(isinstance(s, str))


if __name__ == '__main__':
    unittest.main()
