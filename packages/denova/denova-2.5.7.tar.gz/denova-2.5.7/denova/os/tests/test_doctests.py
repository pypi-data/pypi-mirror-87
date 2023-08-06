#!/usr/bin/env python3
'''
    Tests the doctests for denova.os.

    The tests starting with xtest aren't being
    maintained so have been disabled.

    Copyright 2019-2020 DeNova
    Last modified: 2020-10-14
'''

import os
import sys
from doctest import testmod
from unittest import main, TestCase

import denova.os.cli
import denova.os.command
import denova.os.drive
import denova.os.fs
import denova.os.lock
import denova.os.osid
import denova.os.process
import denova.os.profile_addons
import denova.os.user


class TestDoctests(TestCase):

    def test_cli(self):
        ''' Test cli doctests. '''

        test_result = testmod(denova.os.cli, report=True)
        self.assertEqual(test_result[0], 0)

    def test_command(self):
        ''' Test command doctests. '''

        test_result = testmod(denova.os.command, report=True)
        self.assertEqual(test_result[0], 0)

    def test_drive(self):
        ''' Test drive doctests. '''

        test_result = testmod(denova.os.drive, report=True)
        self.assertEqual(test_result[0], 0)

    def test_fs(self):
        ''' Test fs doctests. '''

        test_result = testmod(denova.os.fs, report=True)
        self.assertEqual(test_result[0], 0)

    def test_lock(self):
        ''' Test lock doctests. '''

        test_result = testmod(denova.os.lock, report=True)
        self.assertEqual(test_result[0], 0)

    def test_osid(self):
        ''' Test osid doctests. '''

        test_result = testmod(denova.os.osid, report=True)
        self.assertEqual(test_result[0], 0)

    def test_process(self):
        ''' Test process doctests. '''

        test_result = testmod(denova.os.process, report=True)
        self.assertEqual(test_result[0], 0)

    def test_profile_addons(self):
        ''' Test profile_addons doctests. '''

        test_result = testmod(denova.os.profile_addons, report=True)
        self.assertEqual(test_result[0], 0)

    def test_user(self):
        ''' Test user doctests. '''

        test_result = testmod(denova.os.user, report=True)
        self.assertEqual(test_result[0], 0)



if __name__ == "__main__":

    success = main()
    # exit with a system return code
    code = int(not success)
    sys.exit(code)

