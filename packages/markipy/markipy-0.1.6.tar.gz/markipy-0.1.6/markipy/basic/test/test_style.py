import unittest

from markipy.basic.style import _style_
from markipy.basic.atom import _atom_

from markipy.basic import Atom
from markipy.basic import Style

_child_ = {'class': 'Child', 'version': 2}
_nephew_ = {'class': 'Nephew', 'version': 3}


class Child(Style):
    def __init__(self):
        Style.__init__(self)
        Atom.__init__(self, _child_['class'], _child_['version'])


class Nephew(Child):
    def __init__(self):
        Child.__init__(self)
        Atom.__init__(self, _nephew_['class'], _nephew_['version'])


class TestStyle(unittest.TestCase):

    def test_style_creation(self):
        a = Style()
        self.assertEqual(a._get_class_details(_atom_['class']).version, _atom_['version'])
        self.assertEqual(a._get_class_details(_style_['class']).version, _style_['version'])
        del a

    def test_style_inheritance(self):
        c = Child()
        self.assertEqual(c._get_class_details(_atom_['class']).version, _atom_['version'])
        self.assertEqual(c._get_class_details(_style_['class']).version, _style_['version'])
        self.assertEqual(c._get_class_details(_child_['class']).version, _child_['version'])

    def test_style_multiple_inheritance(self):
        n = Nephew()
        self.assertEqual(n._get_class_details(_atom_['class']).version, _atom_['version'])
        self.assertEqual(n._get_class_details(_style_['class']).version, _style_['version'])
        self.assertEqual(n._get_class_details(_child_['class']).version, _child_['version'])
        self.assertEqual(n._get_class_details(_nephew_['class']).version, _nephew_['version'])


if __name__ == '__main__':
    unittest.main()
