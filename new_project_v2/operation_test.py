import unittest
from operation import Operation

class OperationTest(unittest.TestCase):
  """Test class for the Operation class."""

  def setUp(self):
    """
    Sets up common test data before each test case.
    """
    self.name = "insert"
    self.index = 3
    self.char = "x"
    self.vector_clock = [1, 2, 0]
    self.replica_id = "replica1"
    self.operation = Operation(self.name, self.index, self.char, self.vector_clock, self.replica_id)

  def test_init_with_arguments(self):
    """
    Tests that the __init__ method initializes attributes correctly.
    """
    self.assertEqual(self.operation._name, self.name)
    self.assertEqual(self.operation._index, self.index)
    self.assertEqual(self.operation._char, self.char)
    self.assertEqual(self.operation._vector_clock, self.vector_clock)
    self.assertEqual(self.operation._replica_id, self.replica_id)
    self.assertFalse(self.operation._applied)  # Default applied state should be False

  def test_init_with_delete_name(self):
    """
    Tests that the __init__ method sets _deleted to True for 'delete' operations.
    """
    operation = Operation("delete", 5, "y", [0, 1, 3], "replica2")
    self.assertTrue(operation._deleted)

  def test_get_methods(self):
    """
    Tests that getter methods return the correct attribute values.
    """
    self.assertEqual(self.operation.get_name(), self.name)
    self.assertEqual(self.operation.get_index(), self.index)
    self.assertEqual(self.operation.get_char(), self.char)
    self.assertEqual(self.operation.get_clock(), self.vector_clock)
    self.assertEqual(self.operation.get_replica_id(), self.replica_id)
    self.assertFalse(self.operation.get_applied())

  def test_set_methods(self):
    """
    Tests that setter methods update attributes correctly.
    """
    new_name = "update"
    new_index = 10
    new_char = "z"
    new_clock = [3, 4, 5]
    new_replica_id = "replica3"
    new_applied = True

    self.operation.set_name(new_name)
    self.operation.set_index(new_index)
    self.operation.set_char(new_char)
    self.operation.set_clock(new_clock)
    self.operation.set_replica_id(new_replica_id)
    self.operation.set_applied(new_applied)

    self.assertEqual(self.operation._name, new_name)
    self.assertEqual(self.operation._index, new_index)
    self.assertEqual(self.operation._char, new_char)
    self.assertEqual(self.operation._vector_clock, new_clock)
    self.assertEqual(self.operation._replica_id, new_replica_id)
    self.assertTrue(self.operation._applied)

  def test_repr(self):
    """
    Tests that the __repr__ method returns a formatted string representation.
    """
    expected_repr = f"{self.name}/{self.index}/{self.char}/{self.vector_clock}/{self.replica_id}/{False}/{self.operation._deleted}\n"
    self.assertEqual(repr(self.operation), expected_repr)

# Run the tests
if __name__ == "__main__":
  unittest.main()
