import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file import File
from operation import Operation

class TestFile(unittest.TestCase):
  def setUp(self):
    self.file_name = 'test_file'
    self.file_name_with_ext = self.file_name + '.txt'

  def test(self):
    # set up
    file = File(self.file_name)
    op1 = Operation('insert', 3, 'x', [1,2,0], '1A')
    op2 = Operation('delete', 1, '', [3,2,1], '1B')
    op3 = Operation('insert', 5, 'z', [3,2,0], '2C')
    file.insert_operation(op1)
    file.insert_operation(op2)
    file.insert_operation(op3)
    content = file.get_content()
    os.remove(self.file_name_with_ext)

    # asserts
    self.assertEqual(len(content), 3)
    self.assertIsInstance(content[0], Operation)

  def test_2(self):
    # set up
    file = File(self.file_name)

    content = file.get_content()
    self.assertTrue(file.is_empty())

    os.remove(self.file_name_with_ext)
    self.assertEqual(len(content), 0)

  #def test_get_content_parses_lines(self):
    #file_obj = File(self.test_filename)
    #content = file_obj.get_content()

    #self.assertEqual(len(content), 2)  # Assert two operations parsed
    #self.assertIsInstance(content[0], Operation)  # Assert first element is Operation
    #self.assertEqual(content[0].name, "insert")  # Assert operation details

# Add similar test functions for other scenarios
if __name__ == "__main__":
  unittest.main()
