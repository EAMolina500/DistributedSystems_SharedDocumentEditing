class Document:
  def __init__(self, name="", server_id=0):
    self._name = name
    self._server_id = server_id

  def create(self):
    try:
      with open(self._name + '.txt', "x") as f:
        f.close()
    except FileNotFoundError:
      print("File not found.")
    except Exception as e:
      print(f"An error occurred: {e}")

  def from_array_to_file(self, array, name):
    with open(self._name + '.txt', 'w') as file:
      string = str(array)
      file.write(string)

  def get_name(self):
    return self._name

  def set_name(self, name):
    self._name = name

  def write_strings(self, strings):
    """Writes a list of strings to the document file."""
    try:
      with open(self._name + '.txt', 'a') as file:  # Open in append mode
        for string in strings:
          file.write(string + '\n')  # Write each string with a newline
    except Exception as e:
      print(f"An error occurred while writing to file: {e}")
