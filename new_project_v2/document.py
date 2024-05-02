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
      self._operations = compare_and_order_operations([], self._operations)
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

    return VectorClock(self._server_id, greater_clock)

  def insert(self, index, char, vector_clock, replica_id):
    incoming_op = Operation('insert', int(index), char, vector_clock, replica_id)
    self._operations = insert_operation(self._operations, incoming_op)
    self._file.insert_operation(incoming_op)

  def delete(self, index, vector_clock, replica_id):
    incoming_op = Operation('delete', int(index), None, vector_clock, replica_id)
    self._operations = insert_operation(self._operations, incoming_op)
    self._file.insert_operation(incoming_op)

  def display(self):
    print('Document content:')
    print(self._operations)
    print(self._content)

  def apply_operations(self):
    for op in self._operations:
      if not op.get_applied():
        if op.get_name() == 'insert':
          self._content.insert(op.get_index(), op.get_char())
          op.set_applied(True)
        elif op.get_name() == 'delete':
          del(self._content[op.get_index()])
          op.set_applied(True)

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

def insert_operation(ordered_operations, new_operation):
  """
  Inserts a new operation into an already ordered list based on vector clocks and replica IDs.

  Args:
    ordered_operations (list[Operation]): Ordered list of operations.
    new_operation (Operation): The operation to insert.

  Returns:
    list[Operation]: The updated ordered list with the new operation inserted.
  """
  if ordered_operations is None:
    # Handle the case where the initial list is empty
    return [new_operation]

  insertion_index = 0
  for existing_op in ordered_operations:
    comparison = compare(new_operation.get_clock(), existing_op.get_clock())
    if comparison == 'equal':
      # If clocks are equal, insert before the existing operation (stability)
      insertion_index = ordered_operations.index(existing_op)
      break
    elif comparison == 'clock1':  # new_operation's clock is greater
      insertion_index = ordered_operations.index(existing_op) + 1
      break
    elif comparison == 'clock2':  # existing operation's clock is greater
      continue
    else:  # Conflict: compare by replica ID
      if new_operation.get_replica_id() < existing_op.get_replica_id():
        insertion_index = ordered_operations.index(existing_op)
        break
      else:
        continue

  # Insert the new operation at the determined index
  ordered_operations.insert(insertion_index, new_operation)

  return ordered_operations

def compare_and_order_operations(document_operations, incoming_operations):
  """
  Compares and orders a list of document operations with a list of incoming operations based
  on vector clocks and replica IDs. Handles conflicts gracefully.

  Args:
      document_operations (list[Operation]): List of operations in the document.
      incoming_operations (list[Operation]): List of incoming operations to compare.

  Returns:
      list[Operation]: Ordered list of operations, combining both document and incoming
                        operations while resolving conflicts.
  """

  ordered_operations = []
  document_op_index = 0
  incoming_op_index = 0

  while document_op_index < len(document_operations) and incoming_op_index < len(incoming_operations):
    document_op = document_operations[document_op_index]
    incoming_op = incoming_operations[incoming_op_index]

    comparison = compare(document_op.get_clock(), incoming_op.get_clock())
    if comparison == 'equal':
      # If vector clocks are equal, prioritize document operations (stability)
      ordered_operations.append(document_op)
      document_op_index += 1
    elif comparison == 'clock1': #(document_op's clock is greater):
      ordered_operations.append(document_op)
      document_op_index += 1
    elif comparison == 'clock2': #(incoming_op's clock is greater):
      ordered_operations.append(incoming_op)
      incoming_op_index += 1
    else:  # Conflict: compare by replica ID
      if document_op.get_replica_id() < incoming_op.get_replica_id():
        ordered_operations.append(document_op)
        document_op_index += 1
      else:
        ordered_operations.append(incoming_op)
        incoming_op_index += 1

  # Append remaining operations after one list is exhausted
  ordered_operations.extend(document_operations[document_op_index:])
  ordered_operations.extend(incoming_operations[incoming_op_index:])

  return ordered_operations
