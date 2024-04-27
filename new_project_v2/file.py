import operation as op

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
          print('line')
          print(line)
          parsed_line = self.parse_line(line)
          if parsed_line:
            self._content.append(parsed_line)
        file.close()
        print('get content from file')
        print(self._content)
    except FileExistsError:
      print(self._name)
      print("File doesn't exist")

  def get_content(self):
    return self._content

  def is_empty(self):
    return self._content == []

  def insert_operation(self, operation):
    with open(self._name, 'a') as file:
      if operation:
        file.write(f"{repr(operation)}\n")
        file.close()
  """
  def from_array_to_file(self, array):
    with open(self._name, 'w') as file:
      for op in array:
        if op:
          file.write(f"{repr(op)}\n")
      file.close()
  """

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
    line_parts = line.strip().split('/')  # Split the line based on spaces

    print('line parts')
    print(line_parts)
    operation_obj = None

    if len(line_parts) >= 6:
      #raise ValueError(f"Invalid operation line: {line}")  # Check for minimum parts
      operation_name = line_parts[0]  # Extract operation name
      index = int(line_parts[1])  # Extract and convert index to integer
      char = line_parts[2]  # Extract character
      vector_clock = [int(val) for val in line_parts[3].strip('[]').split(',')]  # Extract and convert vector clock elements to integers
      replica_id = line_parts[4]  # Extract replica ID
      applied = False  # Assuming applied is initially False

      # Create an Operation object and set its attributes
      operation_obj = op.Operation(operation_name, index, char, vector_clock, replica_id)

    return operation_obj
