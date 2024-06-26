from operation import Operation
import document_pb2
from bisect import insort
from functools import cmp_to_key

import operation

# functions used in Document class

def compare(clock1, clock2):
  differences = [a - b for a, b in zip(clock1, clock2)]

  if all(diff == 0 for diff in differences):
    return 'equal'
  elif all(diff >= 0 for diff in differences):
    return 'clock1'
  elif all(diff <= 0 for diff in differences):
    return 'clock2'
  else:
    return 'conflict'

def compare_operations(op1, op2):
  vc1 = op1.get_clock()
  vc2 = op2.get_clock()

  comp_result = compare(vc1, vc2)
  if comp_result == 'clock2': # vc1 smaller
    return -1
  elif comp_result == 'clock1': # vc1 greater
    return 1

  if op1.get_replica_id() < op2.get_replica_id():
    return -1
  elif op1.get_replica_id() > op2.get_replica_id():
    return 1
  else:
    return 0

def insert_operation(operations, new_operation):
  comparable_operations = [ComparableOperation(op) for op in operations]
  new_comparable_operation = ComparableOperation(new_operation)
  insort(comparable_operations, new_comparable_operation)
  return [co.operation for co in comparable_operations]

# functions used in Server class

def compute_new(clock, other_clock):
  return [max(a, b) for a, b in zip(clock, other_clock)]

def increment(vector_clock, server_id):
  index = server_id - 1
  vector_clock[index] += 1
  return vector_clock

def operation_to_params(op, server_id):
  return document_pb2.Params(
    operation=op.get_name(),
    index=op.get_index(),
    char=op.get_char(),
    server_id=server_id,
    tumbstamp =op.get_deleted(),
    timestamp =op.get_clock(),
    replica_id =op.get_replica_id()
  )

def gen_replica_id(server_id, operations_number):
  replica_id = str(operations_number)
  if (server_id == 1):
    replica_id += 'A'
  elif (server_id == 2):
    replica_id += 'B'
  elif (server_id == 3):
    replica_id += 'C'

  return replica_id

def get_initial_clock():
  return [0,0,0]

class ComparableOperation:
  def __init__(self, operation):
    self.operation = operation

  def __lt__(self, other):
    return compare_operations(self.operation, other.operation) < 0