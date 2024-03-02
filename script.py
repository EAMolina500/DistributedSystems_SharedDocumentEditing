import server
import client
import document_service
import server_communication_service
import time

if __name__ == "__main__":
  client_1 = client.Client(1, '50051')
  client_2 = client.Client(2, '50052')

  client_1.send_command_with_params(command='create', file_name='document')

  time.sleep(5)

  client_1.send_command_with_params(command='insert', position=0, character='A')
  time.sleep(3)

  client_2.send_command_with_params(command='insert', position=1, character='B')
  time.sleep(3)

  client_1.send_command_with_params(command='insert', position=2, character='C')
  time.sleep(3)

  client_2.send_command_with_params(command='insert', position=3, character='D')
  time.sleep(3)

  client_1.send_command_with_params(command='insert', position=4, character='E')
  time.sleep(3)

  client_2.send_command_with_params(command='insert', position=5, character='F')
  time.sleep(3)

  """
  text = list('Finalmente!')
  index = -1
  for char in text:
  	index +=1
  	client_1.send_command_with_params(command='insert', position=index, character=char)
  """

  client_1.send_command_with_params(command='display')
  client_2.send_command_with_params(command='display')


