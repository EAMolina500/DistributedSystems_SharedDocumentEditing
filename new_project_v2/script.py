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
  insert = 'insert'
  delete = 'delete'
  display = 'display'

  client.run_for_test(server3, insert, 0, 'a', port3)
  client.run_for_test(server2, insert, 1, 'b', port2)
  client.run_for_test(server3, insert, 2, 'c', port3)
  client.run_for_test(server1, delete, 4, '', port1)
  client.run_for_test(server1, insert, 3, 'd', port1)
  client.run_for_test(server3, insert, 4, 'e', port3)
  client.run_for_test(server2, delete, 1, '', port2)
  client.run_for_test(server2, insert, 5, 'f', port2)
  client.run_for_test(server1, insert, 6, 'g', port1)
  client.run_for_test(server3, delete, 2, '', port3)
  client.run_for_test(server2, insert, 7, 'h', port2)
  client.run_for_test(server1, insert, 8, 'i', port1)
  client.run_for_test(server3, insert, 9, 'j', port3)
  client.run_for_test(server1, delete, 4, '', port1)
  client.run_for_test(server3, delete, 2, '', port3)

  client.run_for_test(server1, display, 0, '', port1)
  client.run_for_test(server2, display, 0, '', port2)
  client.run_for_test(server3, display, 0, '', port3)
