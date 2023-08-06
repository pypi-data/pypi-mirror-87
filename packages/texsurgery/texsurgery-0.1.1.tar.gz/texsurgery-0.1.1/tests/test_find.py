#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
#import logging

from texsurgery.texsurgery import TexSurgery

class TestFind(unittest.TestCase):
    """ Tests TexSurgery.find and  TexSurgery.findall"""

    def __init__(self, methodName='runTest'):
        super(TestFind, self).__init__(methodName=methodName)
        with open('tests/test_find.tex','r') as f:
            self.sample_tex = f.read()

    def test_find_one_environment(self):
        """finds all apperances of one non nested environment
        that appears only once.
        """
        tex_source = self.sample_tex
        expected_res = [('run', "print('The random seed is ', seed)\n")]
        res = TexSurgery(tex_source).findAll('run')
        self.assertEqual(res, expected_res)

    def test_find_all(self):
        """finds all apperances of a non nested environment
        that appears a few times.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('runsilent', """seed = 1\nset_random_seed(seed)\n"""),
            ('runsilent', """a = randint(1,10)\n"""),
            ('runsilent', """a = randint(2,10)\nf = sin(a*x)\nfd = f.derivative(x)\n"""),
        ]
        res = TexSurgery(tex_source).findAll('runsilent')
        self.assertEqual(res, expected_res)

    def test_find_nested(self):
        """finds all apperances of a command nested inside
        an environment that appears once.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('choices', [('\correctchoice', '$\sage{fd}$')]),
        ]
        res = TexSurgery(tex_source).findAll(r'choices \correctchoice')
        self.assertEqual(res, expected_res)

    def test_find_nested_2(self):
        """finds all apperances of a command nested inside
        an environment which is nested inside
        another environment that appears once.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('question', [
               ('choices', [('\correctchoice', '$\sage{fd}$')])
               ]),
        ]
        res = TexSurgery(tex_source).findAll(r'question choices \correctchoice')
        self.assertEqual(res, expected_res)

    def test_find_comma_nested(self):
        """finds all apperances of a command nested inside an environment
        nested inside another environment which can be of two different types.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('question', [
               ('choices', [('\correctchoice', '$\sage{fd}$')])
               ]),
        ]
        res = TexSurgery(tex_source).findAll(r'question,questionmultx choices \correctchoice')
        self.assertEqual(res, expected_res)

    def test_find_nested_comma_nested_mult(self):
        """finds all apperances of a command nested inside an environment
        which is nested inside another environment which can be of two different types.
        It matches the tex twice.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx', [('runsilent', 'a = randint(1,10)\n')]),
            ('question',
             [('runsilent', 'a = randint(2,10)\nf = sin(a*x)\nfd = f.derivative(x)\n')])
        ]
        res = TexSurgery(tex_source).findAll('question,questionmultx runsilent')
        self.assertEqual(res, expected_res)

    def test_find_comma_alternatives(self):
        """tests a selector consisting of two selectors separated by a comma.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('question', [('choices', [('\correctchoice', '$\sage{fd}$')])]),
            ('questionmultx', [('\\AMCnumericChoices', '\\eval{8+a}')])
        ]
        res = TexSurgery(tex_source).findAll(r'question choices \correctchoice, questionmultx \AMCnumericChoices')
        self.assertEqual(res, expected_res)

    def test_find_command_with_two_arguments(self):
        """tests a selector consisting of a command with two mandatory arguments in braces {}.
        """
        tex_source = self.sample_tex
        expected_res = [
            ('questionmultx',
             [('\\AMCnumericChoices', ['\\eval{8+a}', 'digits=2,sign=false,scoreexact=3'])])
        ]
        res = TexSurgery(tex_source).findAll(r'questionmultx \AMCnumericChoices[2]')
        self.assertEqual(res, expected_res)
