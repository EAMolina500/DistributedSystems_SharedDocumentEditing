from time import sleep
from client import run_for_test
from file import File
from script_constants import SERVER_1, SERVER_2, SERVER_3, PORT_1, PORT_2, PORT_3, \
                      INSERT, DELETE, DISPLAY, FILE_1_NAME, FILE_2_NAME, FILE_3_NAME

if __name__ == "__main__":
  file_1 = File(FILE_1_NAME)
  file_2 = File(FILE_2_NAME)
  file_3 = File(FILE_3_NAME)

  operations = [
    (SERVER_1, INSERT, 0, 'x', PORT_1),
    (SERVER_2, INSERT, 1, 'y', PORT_2),
    (SERVER_3, INSERT, 2, 'z', PORT_3),
    (SERVER_1, DELETE, 0, '', PORT_1),
    (SERVER_2, INSERT, 3, 'w', PORT_2),
    (SERVER_3, DELETE, 1, '', PORT_3),
  ]

  for op in operations:
    run_for_test(*op)

  sleep(1)

  doc1 = file_1.get_content()
  doc2 = file_2.get_content()
  doc3 = file_3.get_content()

  assert repr(doc1) == repr(doc1) == repr(doc1), "Document states are inconsistent"
  print("Succesfully execution.")
  print("All servers have consistent document state.")
