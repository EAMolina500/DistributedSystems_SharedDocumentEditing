import threading
import client
import os

def client_task(server, operation, index, char, port):
  client.run_for_test(server, operation, index, char, port)

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

  threads = []
  operations = [
    (server1, insert, 0, 'k', port1),
    (server2, insert, 1, 'l', port2),
    (server3, insert, 2, 'm', port3),
    (server1, delete, 0, '', port1),
    (server2, insert, 3, 'n', port2),
    (server3, delete, 1, '', port3),
    (server1, insert, 4, 'k', port1),
    (server2, insert, 2, 'l', port2),
    (server3, insert, 5, 'm', port3),
    (server1, delete, 3, '', port1),
    (server2, delete, 1, '', port3)
  ]

  for op in operations:
    t = threading.Thread(target=client_task, args=op)
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  client.run_for_test(server1, display, 0, '', port1)
  client.run_for_test(server2, display, 0, '', port2)
  client.run_for_test(server3, display, 0, '', port3)

  # Borrar para revisar logs en los archivos
  os.remove('server_1_file.txt')
  os.remove('server_2_file.txt')
  os.remove('server_3_file.txt')
