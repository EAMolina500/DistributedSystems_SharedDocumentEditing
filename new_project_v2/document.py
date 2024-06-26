from file import File
from operation import Operation
from auxiliar_functions import get_initial_clock, insert_operation

class Document:
  def __init__(self, server_id):
    self._content = []
    self._operations = []
    self._server_id = server_id
    self._file_name = 'server_' + str(self._server_id) + '_file'
    self._file = File(self._file_name)

    if not self._file.is_empty():
      self._operations = self._file.get_content()
      self.apply_operations()

  def get_operations(self):
    return self._operations

  def set_operations(self, operations):
    self._content = []
    self._operations = operations
    self.apply_operations()
    self.display()

  def get_last_clock(self):
    greater_clock = get_initial_clock()

    for op in self._operations:
      if op.get_clock() > greater_clock:
        greater_clock = op.get_clock()

    return greater_clock

  def insert(self, index, char, vector_clock, replica_id):
    incoming_op = Operation('insert', int(index), char, vector_clock, replica_id)
    self._operations = insert_operation(self._operations, incoming_op)
    self._file.set_file(self._operations)

  def delete(self, index, vector_clock, replica_id):
    incoming_op = Operation('delete', int(index), None, vector_clock, replica_id)
    self._operations = insert_operation(self._operations, incoming_op)
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
