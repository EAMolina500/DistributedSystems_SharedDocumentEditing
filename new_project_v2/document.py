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
    self._server_id = server_id

  def insert_by_index(self, index, char, vector_clock, replica_id):
    self._operations.append(Operation('insert', int(index), char, vector_clock, replica_id))

  def delete_by_index(self, index, vector_clock, replica_id):
    self._operations.append(Operation('delete', int(index), None, vector_clock, replica_id))

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
