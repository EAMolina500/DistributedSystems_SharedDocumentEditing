from operation import Operation
import document_pb2
from functools import cmp_to_key

import operation

class AuxiliarFunctions:

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

    comp_result = AuxiliarFunctions.compare(vc1, vc2)
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

  @staticmethod
  def insert_ordered_operations(operations, new_operation):
    operations.append(new_operation)
    operations.sort(key=cmp_to_key(AuxiliarFunctions.compare_operations))
    return operations

  @staticmethod
  def insert_operation(ordered_operations, new_operation):
    if ordered_operations is None:
      return [new_operation]

    ordered_operations.reverse()
    index = -1
    for curr_operation in ordered_operations:
      comp_result = AuxiliarFunctions.compare(new_operation.get_clock(), curr_operation.get_clock())
      if comp_result == 'clock1': # new_operation greater
        index = ordered_operations.index(curr_operation)
        break
      elif comp_result == 'clock2' or comp_result == 'equal':
        index = ordered_operations.index(curr_operation) + 1
      else: # there's a conflict
        if new_operation.get_replica_id() > curr_operation.get_replica_id():
          index = ordered_operations.index(curr_operation)
          break
        else:
          index = ordered_operations.index(curr_operation) + 1

    ordered_operations.insert(index, new_operation)
    ordered_operations.reverse()
    return ordered_operations

  # functions used in Server class

  @staticmethod
  def compute_new(clock, other_clock):
    return [max(a, b) for a, b in zip(clock, other_clock)]

  @staticmethod
  def increment(vector_clock, server_id):
    index = server_id - 1
    vector_clock[index] += 1
    return vector_clock

  @staticmethod
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

  @staticmethod
  def gen_replica_id(server_id, operations_number):
    replica_id = str(operations_number)
    if (server_id == 1):
      replica_id += 'A'
    elif (server_id == 2):
      replica_id += 'B'
    elif (server_id == 3):
      replica_id += 'C'

    return replica_id

  @staticmethod
  def get_initial_clock():
    return [0,0,0]