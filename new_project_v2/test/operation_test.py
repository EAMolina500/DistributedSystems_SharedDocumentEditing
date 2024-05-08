import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from operation import Operation


class OperationTest(unittest.TestCase):
  def setUp(self):
    self.name = "insert"
    self.index = 3
    self.char = "x"
    self.vector_clock = [1, 2, 0]
    self.replica_id = "1A"
    self.operation = Operation(self.name, self.index, self.char, self.vector_clock, self.replica_id)

  def test_init_with_arguments(self):
    self.assertEqual(self.operation._name, self.name)
    self.assertEqual(self.operation._index, self.index)
    self.assertEqual(self.operation._char, self.char)
    self.assertEqual(self.operation._vector_clock, self.vector_clock)
    self.assertEqual(self.operation._replica_id, self.replica_id)
    self.assertFalse(self.operation._applied)
    self.assertFalse(self.operation._deleted)

  def test_init_with_delete_name(self):
    operation = Operation("delete", 5, "y", [0, 1, 3], "2B")
    self.assertTrue(operation._deleted)

  def test_get_methods(self):
    self.assertEqual(self.operation.get_name(), self.name)
    self.assertEqual(self.operation.get_index(), self.index)
    self.assertEqual(self.operation.get_char(), self.char)
    self.assertEqual(self.operation.get_clock(), self.vector_clock)
    self.assertEqual(self.operation.get_replica_id(), self.replica_id)
    self.assertFalse(self.operation.get_applied())
    self.assertFalse(self.operation.get_deleted())

  def test_set_methods(self):
    new_name = "update"
    new_index = 10
    new_char = "z"
    new_clock = [3, 4, 5]
    new_replica_id = "3C"
    new_applied = True
    new_deleted = True

    self.operation.set_name(new_name)
    self.operation.set_index(new_index)
    self.operation.set_char(new_char)
    self.operation.set_clock(new_clock)
    self.operation.set_replica_id(new_replica_id)
    self.operation.set_applied(new_applied)
    self.operation.set_deleted(new_deleted)

    self.assertEqual(self.operation._name, new_name)
    self.assertEqual(self.operation._index, new_index)
    self.assertEqual(self.operation._char, new_char)
    self.assertEqual(self.operation._vector_clock, new_clock)
    self.assertEqual(self.operation._replica_id, new_replica_id)
    self.assertTrue(self.operation._applied)
    self.assertTrue(self.operation._deleted)

  def test_repr(self):
    expected_repr = f"{self.name}/{self.index}/{self.char}/{self.vector_clock}/{self.replica_id}/{False}/{self.operation._deleted}\n"
    self.assertEqual(repr(self.operation), expected_repr)

if __name__ == "__main__":
  unittest.main()
