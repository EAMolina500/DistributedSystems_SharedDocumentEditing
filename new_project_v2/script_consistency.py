import server
import client
import document
import time
import os
import file
import script_constants as SC

if __name__ == "__main__":
  file_1 = file.File(SC.FILE_1_NAME)
  file_2 = file.File(SC.FILE_2_NAME)
  file_3 = file.File(SC.FILE_3_NAME)

  operations = [
    (SC.SERVER_1, SC.INSERT, 0, 'x', SC.PORT_1),
    (SC.SERVER_2, SC.INSERT, 1, 'y', SC.PORT_2),
    (SC.SERVER_3, SC.INSERT, 2, 'z', SC.PORT_3),
    (SC.SERVER_1, SC.DELETE, 0, '', SC.PORT_1),
    (SC.SERVER_2, SC.INSERT, 3, 'w', SC.PORT_2),
    (SC.SERVER_3, SC.DELETE, 1, '', SC.PORT_3),
  ]

  for op in operations:
    client.run_for_test(*op)

  time.sleep(1)

  doc1 = file_1.get_content()
  doc2 = file_2.get_content()
  doc3 = file_3.get_content()

  assert repr(doc1) == repr(doc1) == repr(doc1), "Document states are inconsistent"
  print("Succesfully execution.")
  print("All servers have consistent document state.")
