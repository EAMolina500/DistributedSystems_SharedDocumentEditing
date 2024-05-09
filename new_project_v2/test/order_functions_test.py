import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from operation import Operation
from document import compare
from document import insert_operation
from document import compare_and_order_operations
from vector_clock import VectorClock

class FunctionTest(unittest.TestCase):
  # compare function test
  def test_compare_equal(self):
    clock1 = [1, 2, 3]
    clock2 = [1, 2, 3]
    self.assertEqual(compare(clock1, clock2), 'equal')

  def test_compare_clock1(self):
    clock1 = [1, 2, 3]
    clock2 = [1, 1, 3]
    self.assertEqual(compare(clock1, clock2), 'clock1')

  def test_compare_clock2(self):
    clock1 = [1, 1, 3]
    clock2 = [1, 2, 3]
    self.assertEqual(compare(clock1, clock2), 'clock2')

  def test_compare_conflict(self):
    clock1 = [1, 0, 3]
    clock2 = [0, 2, 3]
    self.assertEqual(compare(clock1, clock2), 'conflict')

  # insert_operation function test

  def test_insert_operation_empty(self):
    new_operation = Operation('insert', 0, 'c', [1, 0, 0], '1A')
    self.assertEqual(insert_operation(None, new_operation), [new_operation])

  def test_insert_before_by_clock(self):
    operations = [Operation('insert', 0, 'a', [2, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'b', [1, 0, 0], '1B')
    expected = [new_operation, operations[0]]
    self.assertEqual(insert_operation(operations, new_operation), expected)

  def test_insert_before_by_replica_id(self):
    operations = [Operation('insert', 0, 'a', [2, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'b', [1, 0, 1], '1B')
    expected = [new_operation, operations[0]]
    self.assertEqual(insert_operation(operations, new_operation), expected)
  """
  def test_insert_operation_after(self):
    operations = [Operation('insert', 0, 'c', [1, 0, 0], '1B')]
    new_operation = Operation('insert', 2, 'c', [1, 0, 0], '3C')
    expected = [operations[0], new_operation]
    self.assertEqual(insert_operation(operations, new_operation), expected)

  def test_insert_operation_conflict_replica_id_1(self):
    operations = [Operation('insert', 0, 'd', [3, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'e', [2, 1, 0], '2B')
    expected = [operations[0], new_operation]
    self.assertEqual(insert_operation(operations, new_operation), expected)
  """
  # Puedes agregar más tests para la función compare_and_order_operations si lo deseas

if __name__ == "__main__":
  unittest.main()