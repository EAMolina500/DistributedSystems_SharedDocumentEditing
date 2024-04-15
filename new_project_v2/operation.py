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
