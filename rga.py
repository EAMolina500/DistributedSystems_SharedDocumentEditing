import document
import vector_clock

class RGA:
  def __init__(self, initial_value=[], server_id=0):
    self._main_array = initial_value
    self._historical_operations_array = []
    self._operations_array = []
    self._server_id = server_id
    self._document = None
    self._vector_clock = vector_clock.VectorClock()

  def create(self, name):
    self.create_file(name)
    self.add_operation(
      server_id=self._server_id,
      file_name=self._document.get_name(),
      command='create'
    )

  def insert(self, index, value):
    if self._document:
      self._vector_clock.increment(self._server_id)
      self.add_operation(
        server_id=self._server_id,
        file_name=self._document.get_name(),
        command='insert',
        position=index,
        character=value,
        timestamp=self._vector_clock.get_value(),
        replica_id=self._get_next_replica_id()
      )
      print('inserting')
      index = len(self._historical_operations_array)-1
      print(self._historical_operations_array[index])
    else:
      print('Accion insertar / Documento inexistente')

  def delete(self, index):
    if self._document:
      self._vector_clock.increment(self._server_id)
      self.add_operation(
        server_id=self._server_id,
        file_name=self._document.get_name(),
        command='delete',
        position=index,
        tumbstamp=True,
        timestamp=self._vector_clock.get_value(),
        replica_id=self._get_next_replica_id()
      )
      print('deleting')
      index = len(self._historical_operations_array)-1
      print(self._historical_operations_array[index])
    else:
      print('Accion borrar / Documento inexistente')

  def add_operation(self, server_id=0, file_name="", command="", position=-1, character="", tumbstamp=False, timestamp=[0,0,0], replica_id=""):
    params = {
      "server_id": server_id,
      "file_name": file_name,
      "command": command,
      "position": position,
      "character": character,
      "tumbstamp": tumbstamp,
      "timestamp": timestamp,
      "replica_id": replica_id
    }
    self._historical_operations_array.append(params)
    self._operations_array.append(params)

  def display(self):
    self.apply_operations()
    self._document.from_array_to_file(self._main_array)
    for op in self._historical_operations_array:
      print(op)

  def _get_next_replica_id(self):
    replica_id = str(len(self._historical_operations_array)+1)
    if (self._server_id == 1):
      replica_id += 'A'
    elif (self._server_id == 2):
      replica_id += 'B'
    elif (self._server_id == 3):
      replica_id += 'C'
    else:
      print('Invalid replica id')

    return replica_id

  def apply_operations(self):
    for operation in self._operations_array:
      if operation["command"] == "insert":
        self._main_array.insert(operation["position"], operation["character"])
      elif operation["command"] == "delete":
        del self._main_array[operation["position"]]
      elif operation["command"] == "create":
        self.create_file(operation["file_name"])

    self._operations_array = []

  def create_file(self, name):
    try:
      if self._document is None:
        self._document = document.Document(name, self._server_id)
        self._document.create()
      else:
        print('Se permite crear un unico documento y el mismo ya fue creado')
    except:
      print('Error al crear el archivo')

  def get_value(self):
    self.apply_operations()
    return self._main_array

  def increment_vector_clock(self):
    self._vector_clock.increment(self._server_id)

  def set_server_id(self, server_id):
    self._server_id = server_id

  def get_operations_array(self):
    return self._operations_array

  def set_document(self, name):
    self._document = document.Document(name, self._server_id)

  def empty_operations_array(self):
    self._operations_array = []
