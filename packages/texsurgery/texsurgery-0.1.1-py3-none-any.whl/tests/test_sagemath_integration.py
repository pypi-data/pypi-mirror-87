#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging

from texsurgery.texsurgery import TexSurgery

class TestSagemathIntegration(unittest.TestCase):
    """ Tests TexSurgery.code_surgery for the sagemath kernel"""

    def test_sagemath_example_1(self):
        """ Tests a full blown example of code_surgery"""
        with open('tests/test_sagemath_1.tex','r') as f:
            tex_source = f.read()
        ts = TexSurgery(tex_source).code_surgery()
#        #uncomment to "reset" the test
#        with open('tests/test_sagemath_1_out.tex','w') as f:
#            tex_out = f.write(ts.src)

        with open('tests/test_sagemath_1_out.tex','r') as f:
            tex_out = f.read()
        self.maxDiff = None
        self.assertEqual(ts.src, tex_out)
        del ts
