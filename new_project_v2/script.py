from client import run_for_test
from os import remove
from script_constants import SERVER_1, SERVER_2, SERVER_3, PORT_1, PORT_2, PORT_3, \
                      INSERT, DELETE, DISPLAY, FILE_1_NAME, FILE_2_NAME, FILE_3_NAME

if __name__ == "__main__":
  run_for_test(SERVER_3, INSERT, 0, 'a', PORT_3)
  run_for_test(SERVER_2, INSERT, 1, 'b', PORT_2)
  run_for_test(SERVER_3, INSERT, 2, 'c', PORT_3)
  run_for_test(SERVER_1, DELETE, 4, '', PORT_1)
  run_for_test(SERVER_1, INSERT, 3, 'd', PORT_1)
  run_for_test(SERVER_3, INSERT, 4, 'e', PORT_3)
  run_for_test(SERVER_2, DELETE, 1, '', PORT_2)
  run_for_test(SERVER_2, INSERT, 5, 'f', PORT_2)
  run_for_test(SERVER_1, INSERT, 6, 'g', PORT_1)
  run_for_test(SERVER_3, DELETE, 2, '', PORT_3)
  run_for_test(SERVER_2, INSERT, 7, 'h', PORT_2)
  run_for_test(SERVER_1, INSERT, 8, 'i', PORT_1)
  run_for_test(SERVER_3, INSERT, 9, 'j', PORT_3)
  run_for_test(SERVER_1, DELETE, 4, '', PORT_1)
  run_for_test(SERVER_3, DELETE, 2, '', PORT_3)

  run_for_test(SERVER_1, DISPLAY, 0, '', PORT_1)
  run_for_test(SERVER_2, DISPLAY, 0, '', PORT_2)
  run_for_test(SERVER_3, DISPLAY, 0, '', PORT_3)

  # Comment lines below to review logs in text files
  remove(FILE_1_NAME + '.txt')
  remove(FILE_2_NAME + '.txt')
  remove(FILE_3_NAME + '.txt')
