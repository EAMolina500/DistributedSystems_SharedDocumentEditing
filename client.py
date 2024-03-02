import grpc
import document_pb2
import document_pb2_grpc

import sys

class Client:
  def __init__(self, client_id, server_port):
    self._client_id = client_id
    self._server_port = server_port

  def send_command(self):
    channel = grpc.insecure_channel("localhost:" + self._server_port)
    stub = document_pb2_grpc.DocumentServiceStub(channel)
    params = self.get_params()
    response = self.get_response(params, stub)
    print("Respuesta del servidor:", response.message)

  def get_params(self):
    print('Puede escribir los comandos:')
    print('1. create')
    print('2. insert')
    print('3. delete')
    print('4. display')
    command = input('Enter an action: ')
    if (command == 'create'):
      file_name = input('Enter a file name: ')
      params = {
        'command': command,
        'file_name': file_name
      }
    elif (command == 'insert'):
      position = int(input('Enter a position: '))
      character = input('Enter a character: ')
      params = {
        'command': command,
        'position': position,
        'character': character
      }
    elif (command == 'delete'):
      position = int(input('Enter a position: '))
      params = {
        'command': command,
        'position': position
      }
    elif (command == 'display'):
      params = {
        'command': command
      }

    return params

  def get_response(self, params, stub):
    if (params['command'] == 'create'):
      response = stub.CreateCommand(document_pb2.Create(file_name=params['file_name']))
    elif (params['command'] == 'insert'):
      response = stub.InsertCommand(document_pb2.Insert(position=params['position'], character=params['character']))
    elif (params['command'] == 'delete'):
      response = stub.DeleteCommand(document_pb2.Delete(position=params['position']))
    elif (params['command'] == 'display'):
      response = stub.DisplayCommand(document_pb2.Display()) # Revisar

    return response

if __name__ == "__main__":
  client_id = int(sys.argv[1])

  if (client_id == 1):
    port = '50051'
  elif (client_id == 2):
    port = '50052'
  elif (client_id == 3):
    port = '50053'
  else:
    print('Invalid param')

  client = Client(client_id, port)
  client.send_command()
