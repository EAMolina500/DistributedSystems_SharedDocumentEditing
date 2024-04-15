class Operation:
  def __init__(self):
    self._name = ''
    self._index = -1
    self._char = ''
    self._vector_clock = [0,0,0]
    self._replica_id = ''
    self._applied = False
    self._deleted = False

  def __init__(self, name, index, char, vector_clock, replica_id):
    self._name = name
    self._index = index
    self._char = char
    self._vector_clock = vector_clock
    self._replica_id = replica_id
    self._applied = False
    self._deleted = name == 'delete'

  def __repr__(self):
    return f"Commando: {self._name}, Indice: {self._index}, Char: {self._char}, Borrado: {self._deleted}\n"

  def get_name(self):
    return self._name

  def get_index(self):
    return self._index

  def get_char(self):
    return self._char

  def get_clock(self):
    return self._vector_clock

  def get_replica_id(self):
    return self._replica_id

  def get_applied(self):
    return self._applied

  def set_name(self, name):
    self._name = name

  def set_index(self, index):
    self._index = index

  def set_char(self, char):
    self._char = char

  def set_clock(self, vector_clock):
    self._vector_clock = vector_clock

  def set_replica_id(self, replica_id):
    self._replica_id = replica_id

  def set_applied(self, applied):
    self._applied = applied



class Document:
  def __init__(self, server_id):
    self._content = []
    self._operations = []
    self._server_id = server_id
    self._file = File([])

  def get_operations(self):
    return self._operations

  def set_operations(self, operations):
    self._operations = operations

  def insert(self, index, char, vector_clock, replica_id):
    incoming_op = Operation('insert', int(index), char, vector_clock, replica_id)
    self._operations = compare_and_order_operations(self._operations, [incoming_op])

    #for op in self._operations:
    if not incoming_op.get_applied():
      self._file.insert_char(incoming_op.get_char(), incoming_op.get_index())
      incoming_op.set_applied(True)

    self._file.from_array_to_file('server_' + str(self._server_id) + '_file')

    #self._operations.append(Operation('insert', int(index), char, vector_clock, replica_id))

  def delete(self, index, vector_clock, replica_id):
    incoming_op = Operation('delete', int(index), None, vector_clock, replica_id)
    self._operations = compare_and_order_operations(self._operations, [incoming_op])

    #for op in self._operations:
    if not incoming_op.get_applied():
      self._file.delete_char(incoming_op.get_index())
      incoming_op.set_applied(True)

    self._file.from_array_to_file('server_' + str(self._server_id) + '_file')

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

class File:
  def __init__(self, array):
    self.array = array

  def get_array(self):
    return self.array

  def set_array(self, array):
    self.array = array

  # No deberia dejar escribir en cualquier posicion
  # Debo poder escribir al lado de un caracter (al menos el espacio en blanco)
  # o al principio de una nueva linea
  def insert_char(self, char, pos):
    new_item = (char, True)

    self.array.insert(pos, new_item)
    """
    if pos >= len(self.array):
      self.array.append(new_item)
    else:
      if not self.array[pos]:
        self.array[pos] = new_item
      elif self.array[pos] != new_item:
        self.array = self.array[:pos] + [new_item] + self.array[pos:]
    """

  def delete_char(self, pos):
    if self.array[pos]:
      aux_array = list(self.array[pos])
      if aux_array[1]:
        aux_array[1] = False
      self.array[pos] = tuple(aux_array)

  def print_array(self):
    print(self.array)

  def filter_visible_chars(self):
    return [(x) for (x, y) in self.array if y is True and x is not None]

  def filter_not_empty_items(self):
    return [x for x in self.array if x is not None]

  def from_array_to_file(self, file_name):
    with open(file_name + '.txt', 'w') as file:
      for tup in self.array:
        if tup:
          file.write(f"({tup[0]}, {tup[1]})\n")

  def parse_line(self, line):
    (key, value) = line.strip()[1:-1].split(", ")
    return (key, eval(value))

  def from_file_to_array(self, file_name):
    self.array = []
    with open(file_name + '.txt', 'r') as file:
      for line in file:
        self.array.append(self.parse_line(line))

  def create(self, name):
    try:
      with open(name + '.txt', "x") as f:
        f.close()
    except FileNotFoundError:
      print("File not found.")
    except Exception as e:
      print(f"An error occurred: {e}")

  def file_filter(self, tuples_file, file_to_display):
    with open(tuples_file, 'r') as tf:
        lines = tf.readlines()

    filtered_chars = []
    for line in lines:
      if 'True' in line:
        char = line.split(',')[0].strip('(')
        filtered_chars.append(char)

    filtered_text = ''.join(filtered_chars)

    with open(file_to_display, 'w') as ftd:
      ftd.write(filtered_text)

  def first_free_pos(self):
    i = 0
    while self.array[i]:
      i += 1
    return i

