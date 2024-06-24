import server
import client
import document
import time

if __name__ == "__main__":
  server1 = '1'
  server2 = '2'
  server3 = '3'
  port1 = '50051'
  port2 = '50052'
  port3 = '50053'
  ins = 'insert'
  rem = 'delete'

  client.run_for_test(server3, ins, 0, 'a', port3)
  client.run_for_test(server2, ins, 1, 'b', port2)
  client.run_for_test(server3, ins, 2, 'c', port3)
  client.run_for_test(server1, rem, 4, '', port1)
  client.run_for_test(server1, ins, 3, 'd', port1)
  client.run_for_test(server3, ins, 4, 'e', port3)
  client.run_for_test(server2, rem, 1, '', port2)
  client.run_for_test(server2, ins, 5, 'f', port2)
  client.run_for_test(server1, ins, 6, 'g', port1)
  client.run_for_test(server3, rem, 2, '', port3)
  client.run_for_test(server2, ins, 7, 'h', port2)
  client.run_for_test(server1, ins, 8, 'i', port1)
  client.run_for_test(server3, ins, 9, 'j', port3)
  client.run_for_test(server1, rem, 4, '', port1)
  client.run_for_test(server3, rem, 2, '', port3)
