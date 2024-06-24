from operation import Operation
from vector_clock import VectorClock
import file

class Document:
  def __init__(self, server_id):
    self._content = []
    self._operations = []
    self._server_id = server_id
    self._file_name = 'server_' + str(self._server_id) + '_file'
    self._file = file.File(self._file_name)
    self._last_clock = [0,0,0]

    if not self._file.is_empty():
      self._operations = self._file.get_content()
      self.apply_operations()

  def get_operations(self):
    return self._operations

  def set_operations(self, operations):
    # solucion temporal
    self._content = []
    self._operations = operations
    self.apply_operations()
    self.display()

  def get_last_clock(self):
    greater_clock = [0,0,0]

    for op in self._operations:
      if op.get_clock() > greater_clock:
        greater_clock = op.get_clock()

    return greater_clock

  def insert(self, index, char, vector_clock, replica_id):
    incoming_op = Operation('insert', int(index), char, vector_clock, replica_id)
    insert_operation_v2(self._operations, incoming_op)
    self._file.set_file(self._operations)

  def delete(self, index, vector_clock, replica_id):
    incoming_op = Operation('delete', int(index), None, vector_clock, replica_id)
    insert_operation_v2(self._operations, incoming_op)
    self._file.set_file(self._operations)

  def display(self):
    print('Document content:')
    print(self._operations)
    print(self._content)

  def apply_operations(self):
    for op in self._operations:
      if not op.get_applied():
        if op.get_name() == 'insert':
          self._content.insert(op.get_index(), op.get_char())
        elif op.get_name() == 'delete':
          if op.get_index() < len(self._content):
            del(self._content[op.get_index()])

      op.set_applied(True)



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

def insert_operation_v2(ordered_operations, new_operation):

  if ordered_operations is None:
    return [new_operation]

  # arriba los casos "negativos"
  ordered_operations.reverse()
  index = -1
  for curr_operation in ordered_operations:
    comp_result = compare(new_operation.get_clock(), curr_operation.get_clock())
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

def insert_operation(ordered_operations, new_operation):
  """
  if new_operation is None and ordered_operations is None:
    print("ERROR EN LA FUNCION INSERT OPERATION\n")
    return None

  if new_operation is None:
    return ordered_operations
  """

  if ordered_operations is None:
    return [new_operation]

  # arriba los casos "negativos"

  insertion_index = 0
  for existing_op in ordered_operations:
    comparison = compare(new_operation.get_clock(), existing_op.get_clock())
    if comparison == 'clock2': # new_operation smaller
      insertion_index = ordered_operations.index(existing_op)
      break
    elif comparison == 'clock1': # new_operation greater
      if (ordered_operations.index(existing_op) == len(ordered_operations)-1):
        insertion_index = len(ordered_operations)
      continue
    else:
      if new_operation.get_replica_id() <= existing_op.get_replica_id():
        # inserto antes ?
        insertion_index = ordered_operations.index(existing_op)
        break
      else:
        if (ordered_operations.index(existing_op) == len(ordered_operations)-1):
          insertion_index = len(ordered_operations)
        continue

  ordered_operations.insert(insertion_index, new_operation)

  return ordered_operations

def compare_and_order_operations(ordered_operations, new_operations):
  for operation in new_operations:
    new_ordered_operations = insert_operation(ordered_operations, operation)

  return ordered_operations

def there_is_a_conflict(ordered_operations, new_operation):
  for operation in ordered_operations:
    comparison = compare(new_operation.get_clock(), operation.get_clock())
    if (comparison == 'clock2' or comparison == 'conflict'):
      return True

  return False
