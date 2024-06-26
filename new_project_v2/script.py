import server
import client
import document
import time
import os
import script_constants as SC

if __name__ == "__main__":
  client.run_for_test(SC.SERVER_3, SC.INSERT, 0, 'a', SC.PORT_3)
  client.run_for_test(SC.SERVER_2, SC.INSERT, 1, 'b', SC.PORT_2)
  client.run_for_test(SC.SERVER_3, SC.INSERT, 2, 'c', SC.PORT_3)
  client.run_for_test(SC.SERVER_1, SC.DELETE, 4, '', SC.PORT_1)
  client.run_for_test(SC.SERVER_1, SC.INSERT, 3, 'd', SC.PORT_1)
  client.run_for_test(SC.SERVER_3, SC.INSERT, 4, 'e', SC.PORT_3)
  client.run_for_test(SC.SERVER_2, SC.DELETE, 1, '', SC.PORT_2)
  client.run_for_test(SC.SERVER_2, SC.INSERT, 5, 'f', SC.PORT_2)
  client.run_for_test(SC.SERVER_1, SC.INSERT, 6, 'g', SC.PORT_1)
  client.run_for_test(SC.SERVER_3, SC.DELETE, 2, '', SC.PORT_3)
  client.run_for_test(SC.SERVER_2, SC.INSERT, 7, 'h', SC.PORT_2)
  client.run_for_test(SC.SERVER_1, SC.INSERT, 8, 'i', SC.PORT_1)
  client.run_for_test(SC.SERVER_3, SC.INSERT, 9, 'j', SC.PORT_3)
  client.run_for_test(SC.SERVER_1, SC.DELETE, 4, '', SC.PORT_1)
  client.run_for_test(SC.SERVER_3, SC.DELETE, 2, '', SC.PORT_3)

  client.run_for_test(SC.SERVER_1, SC.DISPLAY, 0, '', SC.PORT_1)
  client.run_for_test(SC.SERVER_2, SC.DISPLAY, 0, '', SC.PORT_2)
  client.run_for_test(SC.SERVER_3, SC.DISPLAY, 0, '', SC.PORT_3)

  # Comment lines below to review logs in text files
  os.remove(SC.FILE_1_NAME + '.txt')
  os.remove(SC.FILE_2_NAME + '.txt')
  os.remove(SC.FILE_3_NAME + '.txt')
