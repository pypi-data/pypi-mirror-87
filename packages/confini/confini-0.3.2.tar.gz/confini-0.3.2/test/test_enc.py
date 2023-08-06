#!/usr/bin/python

import os
import unittest
import logging

from confini import Config
from confini.error import DecryptError

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

script_dir = os.path.dirname(os.path.realpath(__file__))
gnupg_dir = os.path.join(script_dir, 'gnupg')

class TestBasic(unittest.TestCase):

    wd = os.path.dirname(__file__)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_enc(self):
        inidir = os.path.join(self.wd, 'files/crypt')
        c = Config(inidir, decrypt=True)
        c.process()
        with self.assertRaises(DecryptError):
            c.get('FOO_BAZ')
        os.environ['GNUPGHOME'] = gnupg_dir
        c.get('FOO_BAZ')
    
if __name__ == '__main__':
    unittest.main()
