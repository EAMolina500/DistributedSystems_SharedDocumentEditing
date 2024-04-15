class File:
  def __init__(self, array):
    self.array = array

  def get_array(self):
    return self.array

  def set_array(self, array):
    self.array = array

  # No deberia dejar escribir en cualquier posicion
  # Debo poder escribir al lado de un caracter (al menos el espacio en blanco)
  # o al principio de una nueva linea
  def insert_operation(self, operation):
    self.array.append(operation)

  def print_array(self):
    print(self.array)

  def filter_visible_chars(self):
    return [(x) for (x, y) in self.array if y is True and x is not None]

  def filter_not_empty_items(self):
    return [x for x in self.array if x is not None]

  def from_array_to_file(self, file_name):
    with open(file_name + '.txt', 'w') as file:
      for op in self.array:
        if op:
          file.write(repr(op) + '\n')

  def parse_line(self, line):
    (key, value) = line.strip()[1:-1].split(", ")
    return (key, eval(value))

  def from_file_to_array(self, file_name):
    self.array = []
    try:
      with open(file_name + '.txt', 'r') as file:
        for line in file:
          self.array.append(self.parse_line(line))
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