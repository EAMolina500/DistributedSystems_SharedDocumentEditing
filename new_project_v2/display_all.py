from client run_for_test

if __name__ == "__main__":
  server1 = '1'
  server2 = '2'
  server3 = '3'
  port1 = '50051'
  port2 = '50052'
  port3 = '50053'
  display = 'display'

  run_for_test(server1, display, 0, '', port1)
  run_for_test(server2, display, 0, '', port2)
  run_for_test(server3, display, 0, '', port3)