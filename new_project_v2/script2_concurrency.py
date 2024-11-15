from os import remove
from client import run_for_test
from threading import Thread
from constants import SERVER_1, SERVER_2, SERVER_3, PORT_1, PORT_2, PORT_3, \
                      INSERT, DELETE, DISPLAY, FILE_1_NAME, FILE_2_NAME, FILE_3_NAME

def client_task(server, operation, index, char, port):
  run_for_test(server, operation, index, char, port)

if __name__ == "__main__":
  threads = []
  operations = [
    (SERVER_1, INSERT, 0, 'k', PORT_1),
    (SERVER_2, INSERT, 1, 'l', PORT_2),
    (SERVER_3, INSERT, 2, 'm', PORT_3),
    (SERVER_1, DELETE, 0, '', PORT_1),
    (SERVER_2, INSERT, 3, 'n', PORT_2),
    (SERVER_3, DELETE, 1, '', PORT_3),
    (SERVER_1, INSERT, 4, 'k', PORT_1),
    (SERVER_2, INSERT, 2, 'l', PORT_2),
    (SERVER_3, INSERT, 5, 'm', PORT_3),
    (SERVER_1, DELETE, 3, '', PORT_1),
    (SERVER_2, DELETE, 1, '', PORT_3)
  ]

  for op in operations:
    t = Thread(target=client_task, args=op)
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  run_for_test(SERVER_1, DISPLAY, 0, '', PORT_1)
  run_for_test(SERVER_2, DISPLAY, 0, '', PORT_2)
  run_for_test(SERVER_3, DISPLAY, 0, '', PORT_3)

  # Comment lines below to review logs in text files
  remove(FILE_1_NAME + '.txt')
  remove(FILE_2_NAME + '.txt')
  remove(FILE_3_NAME + '.txt')
