from operation import Operation

class File:
  def __init__(self, file_name):
    self._name = file_name + '.txt'
    self._file = None
    self._content = []
    try:
      self._file = open(self._name, 'x')
      self._file.close()
    except FileExistsError:
      print('Constructor exception')
      self.get_content_from_file()

  def get_content_from_file(self):
    try:
      with open(self._name, 'r') as file:
        for line in file:
          parsed_line = self.parse_line(line)
          if parsed_line:
            self._content.append(parsed_line)
        file.close()
    except FileExistsError:
      print("File doesn't exist")

  def get_content(self):
    self.get_content_from_file()
    return self._content

  def is_empty(self):
    return self._content == []

  def set_file(self, operations):
    with open(self._name, 'w') as file:
      for operation in operations:
        if operation:
          file.write(f"{repr(operation)}\n")
      file.close()

  def insert_operation(self, operation):
    with open(self._name, 'a') as file:
      if operation:
        file.write(f"{repr(operation)}\n")
        file.close()

  def parse_line(self, line):
    line_parts = line.strip().split('/')
    operation_obj = None

    if len(line_parts) >= 6:
      name = line_parts[0]
      index = int(line_parts[1])
      char = line_parts[2]
      vector_clock = [int(val) for val in line_parts[3].strip('[]').split(',')]
      replica_id = line_parts[4]
      applied = line_parts[5]
      deleted = line_parts[6]

      operation_obj = Operation(name, index, char, vector_clock, replica_id)

    return operation_obj
