class Document:
  def __init__(self, name="", server_id=0):
    self._name = name
    self._server_id = server_id

  def create(self):
    try:
      #with open(self._name + '.txt', "x") as f:
      with open(self.format_name() + '.txt', "x") as f:
        f.close()
    except FileNotFoundError:
      print("File not found.")
    except Exception as e:
      print(f"An error occurred: {e}")

  def from_array_to_file(self, array):
    with open(self.format_name() + '.txt', 'w') as file:
      string = str(array)
      file.write(string)

  def get_name(self):
    return self._name

  def set_name(self, name):
    self._name = name

  def format_name(self):
    return 'server_' + str(self._server_id) + '_' + self._name
