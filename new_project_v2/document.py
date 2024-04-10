class Operation:
  def __init__(self):
    self._name = ''
    self._index = -1
    self._char = ''
    self._applied = False
    self._deleted = False

  def __init__(self, name, index, char):
    self._name = name
    self._index = index
    self._char = char
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

  def get_applied(self):
    return self._applied

  def set_name(self, name):
    self._name = name

  def set_index(self, index):
    self._index = index

  def set_char(self, char):
    self._char = char

  def set_applied(self, applied):
    self._applied = applied



class Document:
  def __init__(self, server_id):
    self._content = []
    self._operations = []
    self._vector_clock = VectorClock()
    self._server_id = server_id

  def insert_by_index(self, index, char):
    self._operations.append(Operation('insert', int(index), char))

  def delete_by_index(self, index):
    self._operations.append(Operation('delete', int(index), None))

  def display(self):
    print('Document content:')
    print(self._operations)
    print(self._content)

  def increment_vector_clock(self):
    self._vector_clock.increment(self._server_id)

  def apply_operations(self):
    for op in self._operations:
      if not op.get_applied():
        if op.get_name() == 'insert':
          self._content.insert(op.get_index(), op.get_char())
        elif op.get_name() == 'delete':
          del(self._content[op.get_index()])

      op.set_applied(True)



class VectorClock:
  def __init__(self, initial_value=None):
    if initial_value is None:
      self._clock = [0,0,0]
    else:
      self._clock = initial_value

  def get_clock(self):
    return self._clock

  def set_clock(self, clock):
    self._clock = clock

  def increment(self, server_id):
    self._clock[server_id-1] += 1

  def compare(self, other_clock):
    differences = [a - b for a, b in zip(self.get_clock(), other_clock.get_clock())]

    if all(diff == 0 for diff in differences):
        return 'equal'
    elif all(diff >= 0 for diff in differences):
        return 'larger'
    elif all(diff <= 0 for diff in differences):
        return 'smaller'
    else:
        return 'conflict'

  def get_smaller(self, clock, other_clock):
    if (self.compare(clock, other_clock) == 'smaller'):
      return clock
    elif (self.compare(other_clock, clock) == 'smaller'):
      return other_clock
    else:
      return None

  def compute_new(self, other_clock):
    new_clock = VectorClock([max(a, b) for a, b in zip(self.get_clock(), other_clock.get_clock())])
    return new_clock
