import unittest

import time
from markipy.basic import Atom
from markipy.basic.atom import _atom_

_child_ = {'class': 'Child', 'version': 2}
_nephew_ = {'class': 'Nephew', 'version': 3}


class Child(Atom):
    def __init__(self):
        Atom.__init__(self, _child_['class'], _child_['version'])


class Nephew(Child):
    def __init__(self):
        Child.__init__(self)
        Atom.__init__(self, _nephew_['class'], _nephew_['version'])


class TestAtom(unittest.TestCase):

    def test_atom_creation(self):
        a = Atom('Test', 1)
        self.assertEqual(a._get_class_details(_atom_['class']).version, _atom_['version'])
        self.assertEqual(a._get_class_details('Test').version, 1)

    def test_atom_inherit_equality(self):
        a = Atom('Test', 1)
        b = Atom('Test', 1)
        self.assertNotEqual(hash(a), hash(b))

    def test_atom_inherit_notequality(self):
        a = Atom('Test1', 1)
        b = Atom('Test2', 1)
        self.assertNotEqual(hash(a), hash(b))

    def test_atom_get_classes(self):
        a = Atom('Test', 1)
        self.assertEqual(a._get_classes_name_list(), [_atom_['class'], 'Test'])

    def test_atom_get_versions(self):
        a = Atom('Test', 1)
        self.assertEqual(a._get_classes_versions_list(), [_atom_['version'], 1])

    def test_atom_inheritance(self):
        c = Child()
        self.assertEqual(c._get_class_details(_atom_['class']).version, _atom_['version'])
        self.assertEqual(c._get_class_details(_child_['class']).version, _child_['version'])

    def test_atom_multiple_inheritance(self):
        n = Nephew()
        self.assertEqual(n._get_class_details(_atom_['class']).version, _atom_['version'])
        self.assertEqual(n._get_class_details(_child_['class']).version, _child_['version'])
        self.assertEqual(n._get_class_details(_nephew_['class']).version, _nephew_['version'])


if __name__ == '__main__':
    unittest.main()
