import server
import client
import document
import time

if __name__ == "__main__":
  port1 = '50051'
  port2 = '50052'
  port3 = '50053'
  ins = 'insert'
  rem = 'delete'

  client.run_for_test(port1, ins, 0, 'a')
  client.run_for_test(port1, ins, 1, 'b')

  client.run_for_test(port2, ins, 2, 'c')
  client.run_for_test(port2, ins, 3, 'd')

  client.run_for_test(port3, ins, 4, 'e')
  client.run_for_test(port3, ins, 5, 'f')

  client.run_for_test(port1, ins, 1, 'g')
  client.run_for_test(port2, ins, 3, 'h')

  client.run_for_test(port3, ins, 5, 'i')
  client.run_for_test(port2, ins, 4, 'j')

  client.run_for_test(port3, ins, 2, 'k')
  client.run_for_test(port1, ins, 0, 'l')

  client.run_for_test(port1, rem, 0, '')
  client.run_for_test(port2, rem, 3, '')

  client.run_for_test(port3, rem, 5, '')
  client.run_for_test(port2, rem, 1, '')

  # borrados

  #client.run_for_test(port1, rem, 0, '')
  #client.run_for_test(port1, rem, 0, '')
  #client.run_for_test(port1, rem, 0, '')

