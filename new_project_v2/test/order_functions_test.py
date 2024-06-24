import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from operation import Operation
from auxiliar_functions import AuxiliarFunctions as AUX

class FunctionTest(unittest.TestCase):

  # compare function tests

  def test_compare_equal(self):
    clock1 = [1, 2, 3]
    clock2 = [1, 2, 3]
    self.assertEqual(AUX.compare(clock1, clock2), 'equal')

  def test_compare_clock1(self):
    clock1 = [1, 2, 3]
    clock2 = [1, 1, 3]
    self.assertEqual(AUX.compare(clock1, clock2), 'clock1')

  def test_compare_clock2(self):
    clock1 = [1, 1, 3]
    clock2 = [1, 2, 3]
    self.assertEqual(AUX.compare(clock1, clock2), 'clock2')

  def test_compare_conflict(self):
    clock1 = [1, 0, 3]
    clock2 = [0, 2, 3]
    self.assertEqual(AUX.compare(clock1, clock2), 'conflict')

  # insert_operation function tests

  def test_insert_operation_empty(self):
    new_operation = Operation('insert', 0, 'c', [1, 0, 0], '1A')
    self.assertEqual(AUX.insert_operation(None, new_operation), [new_operation])

  def test_insert_before_by_clock(self):
    operations = [Operation('insert', 0, 'a', [2, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'b', [1, 0, 0], '1B')
    expected = [new_operation, operations[0]]
    self.assertEqual(AUX.insert_operation(operations, new_operation), expected)

  def test_insert_before_by_replica_id(self):
    operations = [Operation('insert', 0, 'a', [2, 1, 0], '1C')]
    new_operation = Operation('insert', 0, 'b', [1, 0, 1], '1B')
    expected = [new_operation, operations[0]]
    self.assertEqual(AUX.insert_operation(operations, new_operation), expected)

  def test_insert_after_by_clock(self):
    operations = [Operation('insert', 0, 'a', [2, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'b', [3, 1, 0], '1B')
    expected = [operations[0], new_operation]
    self.assertEqual(AUX.insert_operation(operations, new_operation), expected)

  def test_insert_after_by_replica_id(self):
    operations = [Operation('insert', 0, 'a', [2, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'b', [1, 0, 1], '1B')
    expected = [operations[0], new_operation]
    self.assertEqual(AUX.insert_operation(operations, new_operation), expected)

  def test_insert_in_middle_by_clock(self):
    operations = [
      Operation('insert', 0, 'a', [2, 1, 0], '1A'),
      Operation('insert', 0, 'c', [3, 1, 0], '1C')
    ]
    new_operation = Operation('insert', 0, 'b', [2, 0, 0], '1B')
    expected = [
      operations[0],
      new_operation,
      operations[1]
    ]
    self.assertEqual(AUX.insert_operation(operations, new_operation), expected)

  def test_insert_in_middle_by_replica_id(self):
    operations = [
      Operation('insert', 0, 'a', [2, 1, 0], '1A'),
      Operation('insert', 0, 'c', [2, 0, 1], '1C')
    ]
    new_operation = Operation('insert', 0, 'b', [2, 0, 0], '1B')
    expected = [
      operations[0],
      new_operation,
      operations[1]
    ]
    self.assertEqual(AUX.insert_operation(operations, new_operation), expected)

if __name__ == "__main__":
  unittest.main()