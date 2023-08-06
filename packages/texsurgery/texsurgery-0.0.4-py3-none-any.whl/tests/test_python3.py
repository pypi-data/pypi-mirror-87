#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class TestPython3Surgery(unittest.TestCase):
    """ Tests TexSurgery.code_surgery for the python3 kernel"""

    def test_simple_addition(self):
        """ Tests a simple addition"""
        tex_source = r'\usepackage[python3]{texsurgery}2+2=\eval{2+2}'
        tex_out = r'2+2=4'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel

    def test_division(self):
        """ Tests a simple addition"""
        tex_source = r'\usepackage[python3]{texsurgery}1/2=\eval{1/2}'
        tex_out = r'1/2=0.5'
        ts = TexSurgery(tex_source).code_surgery()
        self.assertEqual(ts.src, tex_out)
        del ts #shutdow kernel
