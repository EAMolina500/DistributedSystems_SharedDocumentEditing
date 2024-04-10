from __future__ import print_function

import grpc
import document_pb2
import document_pb2_grpc

import sys


def run(server_id, server_port):
  with grpc.insecure_channel('localhost:' + server_port) as channel:
    stub = document_pb2_grpc.DocumentServiceStub(channel)
    params = get_params()
    if (params['command'] == 'insert'):
      response = stub.InsertCommand(document_pb2.Insert(index=params['index'], char=params['char']))
    elif (params['command'] == 'delete'):
      response = stub.DeleteCommand(document_pb2.Delete(index=params['index']))

    print("Document client received: " + response.message)

def get_params():
  params = {
    'command': input('Enter a command: '),
    'index': int(input('Enter an index: ')),
    'char': input('Enter a char: ')
  }

  return params

def run_for_test(server_port, command, index, char):
  with grpc.insecure_channel('localhost:' + server_port) as channel:
    stub = document_pb2_grpc.DocumentServiceStub(channel)
    #params = get_params()
    if (command == 'insert'):
      response = stub.InsertCommand(document_pb2.Operation(name=command, index=index, char=char))
    elif (command == 'delete'):
      response = stub.DeleteCommand(document_pb2.Operation(name=command, index=index))

    print("Document client received: " + response.message)

if __name__ == "__main__":
  server_id = sys.argv[1]
  port = ''

  if (server_id == '1'):
    port = '50051'
  elif (server_id == '2'):
    port = '50052'
  elif (server_id == '3'):
    port = '50053'

  run(server_id, port)
