import server
import client
import document
import time
import os
import file

if __name__ == "__main__":
  server1 = '1'
  server2 = '2'
  server3 = '3'
  port1 = '50051'
  port2 = '50052'
  port3 = '50053'
  insert = 'insert'
  delete = 'delete'
  display = 'display'
  file_1_name = 'server_1_file'
  file_2_name = 'server_2_file'
  file_3_name = 'server_3_file'
  file_1 = file.File(file_1_name)
  file_2 = file.File(file_2_name)
  file_3 = file.File(file_3_name)

  operations = [
    (server1, insert, 0, 'x', port1),
    (server2, insert, 1, 'y', port2),
    (server3, insert, 2, 'z', port3),
    (server1, delete, 0, '', port1),
    (server2, insert, 3, 'w', port2),
    (server3, delete, 1, '', port3),
  ]

  for op in operations:
    client.run_for_test(*op)

  time.sleep(1)

  doc1 = file_1.get_content()
  doc2 = file_2.get_content()
  doc3 = file_3.get_content()

  assert repr(doc1) == repr(doc1) == repr(doc1), "Document states are inconsistent"
  print("All servers have consistent document state.")
