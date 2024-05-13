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

  def test_insert_operation_after(self):
    op1 = Operation('insert', 1, 'a', [0, 1, 1], '1A')
    op2 = Operation('insert', 2, 'b', [1, 1, 1], '1B')
    op3 = Operation('insert', 3, 'c', [1, 1, 2], '1C')
    op4 = Operation('delete', 2, '', [1, 2, 3], '1B')
    op5 = Operation('insert', 4, 'd', [2, 2, 3], '1A')
    op6 = Operation('insert', 5, 'e', [3, 2, 2], '1C')
    op7 = Operation('delete', 3, '', [4, 3, 4], '1A')
    op8 = Operation('insert', 6, 'f', [5, 4, 4], '1C')
    op9 = Operation('insert', 7, 'g', [6, 4, 5], '1B')

    ops = []
    ops = insert_operation(ops, op1)
    ops = insert_operation(ops, op3)
    ops = insert_operation(ops, op5)
    ops = insert_operation(ops, op7)
    ops = insert_operation(ops, op9)
    ops = insert_operation(ops, op2)
    ops = insert_operation(ops, op4)
    ops = insert_operation(ops, op6)
    ops = insert_operation(ops, op8)

    expected = [op1, op2, op3, op4, op5, op6, op7, op8, op9]

    print(ops)
    print(ops)

    self.assertEqual(ops, expected)

  """
  def test_insert_operation_conflict_replica_id_1(self):
    operations = [Operation('insert', 0, 'd', [3, 1, 0], '1A')]
    new_operation = Operation('insert', 0, 'e', [2, 1, 0], '2B')
    expected = [operations[0], new_operation]
    self.assertEqual(insert_operation(operations, new_operation), expected)
  """
  # Puedes agregar más tests para la función compare_and_order_operations si lo deseas

if __name__ == "__main__":
  unittest.main()