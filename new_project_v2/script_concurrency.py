import threading
import client
import os
import script_constants as SC

def client_task(server, operation, index, char, port):
  client.run_for_test(server, operation, index, char, port)

if __name__ == "__main__":
  threads = []
  operations = [
    (SC.SERVER_1, SC.INSERT, 0, 'k', SC.PORT_1),
    (SC.SERVER_2, SC.INSERT, 1, 'l', SC.PORT_2),
    (SC.SERVER_3, SC.INSERT, 2, 'm', SC.PORT_3),
    (SC.SERVER_1, SC.DELETE, 0, '', SC.PORT_1),
    (SC.SERVER_2, SC.INSERT, 3, 'n', SC.PORT_2),
    (SC.SERVER_3, SC.DELETE, 1, '', SC.PORT_3),
    (SC.SERVER_1, SC.INSERT, 4, 'k', SC.PORT_1),
    (SC.SERVER_2, SC.INSERT, 2, 'l', SC.PORT_2),
    (SC.SERVER_3, SC.INSERT, 5, 'm', SC.PORT_3),
    (SC.SERVER_1, SC.DELETE, 3, '', SC.PORT_1),
    (SC.SERVER_2, SC.DELETE, 1, '', SC.PORT_3)
  ]

  for op in operations:
    t = threading.Thread(target=client_task, args=op)
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  client.run_for_test(SC.SERVER_1, SC.DISPLAY, 0, '', SC.PORT_1)
  client.run_for_test(SC.SERVER_2, SC.DISPLAY, 0, '', SC.PORT_2)
  client.run_for_test(SC.SERVER_3, SC.DISPLAY, 0, '', SC.PORT_3)

  # Comment lines below to review logs in text files
  os.remove(SC.FILE_1_NAME + '.txt')
  os.remove(SC.FILE_2_NAME + '.txt')
  os.remove(SC.FILE_3_NAME + '.txt')
