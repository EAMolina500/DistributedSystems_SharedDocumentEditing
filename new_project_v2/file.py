class File:
  def __init__(self, file_name):
    self._name = file_name + '.txt'
    self._file = None
    try:
      self._file = open(self._name, "x")
      self._file.close()
    except:
      print('File already exists')

  # No deberia dejar escribir en cualquier posicion
  # Debo poder escribir al lado de un caracter (al menos el espacio en blanco)
  # o al principio de una nueva linea
  def insert_operation(self, operation):
    with open(self._name, 'w') as file:
      if operation:
        file.write(f"{repr(operation)}\n")
        file.close()

  def print_array(self):
    print(self.array)

  def filter_visible_chars(self):
    return [(x) for (x, y) in self.array if y is True and x is not None]

  def filter_not_empty_items(self):
    return [x for x in self.array if x is not None]

  def from_array_to_file(self, array):
    with open(self._name, 'w') as file:
      for op in array:
        if op:
          file.write(f"{repr(op)}\n")
      file.close()

  def parse_line(self, line):
    """Parses a line of text representing an operation into its corresponding object.

    Args:
        line (str): The line of text to parse.

    Returns:
        Operation: The parsed operation object.

    Raises:
        ValueError: If the line cannot be parsed into a valid operation.
    """

    # Assuming your operations are represented as strings with a specific format:
    # "OperationName index character {vector_clock_elements separated by commas} replica_id"
    line_parts = line.strip().split(' ')  # Split the line based on spaces

    if len(line_parts) < 6:
      raise ValueError(f"Invalid operation line: {line}")  # Check for minimum parts

    operation_name = line_parts[0]  # Extract operation name
    index = int(line_parts[1])  # Extract and convert index to integer
    char = line_parts[2]  # Extract character
    vector_clock = [int(val) for val in line_parts[3].strip('[]').split(',')]  # Extract and convert vector clock elements to integers
    replica_id = line_parts[4]  # Extract replica ID
    applied = False  # Assuming applied is initially False

    # Create an Operation object and set its attributes
    operation_obj = Operation(operation_name, index, char, vector_clock, replica_id)

    return operation_obj


  def from_file_to_array(self):
    array = []
    try:
      with open(self._name, 'r') as file:
        for line in file:
          array.append(self.parse_line(line))
        file.close()
      return array
    except:
      print("File doesn't exist")

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