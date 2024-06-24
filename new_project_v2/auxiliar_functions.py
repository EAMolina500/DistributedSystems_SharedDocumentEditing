from operation import Operation
import document_pb2

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
      elif comp_result == 'clock2':
        index = ordered_operations.index(curr_operation) + 1
        break
      elif comp_result == 'equal':
        # system exception
        print('EXCEPTION !!!')
      else: # there's a conflict
        if new_operation.get_replica_id() > curr_operation.get_replica_id():
          index = ordered_operations.index(curr_operation)
          break
        else:
          index = ordered_operations.index(curr_operation) + 1
          break

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
