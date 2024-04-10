from concurrent import futures

import grpc
import document_pb2
import document_pb2_grpc

import document as doc

import sys

class DocumentService(document_pb2_grpc.DocumentServiceServicer):
  def __init__(self, server_id):
    self.document = doc.Document(server_id)
    self.server_id = server_id

  # methods that listen client requests
  def InsertCommand(self, request, context):
    print('El client envio: %s' % request)

    # llega un mensaje del client al server, incremento el vector
    self.document.insert_by_index(request.index, request.char)
    self.document.apply_operations()
    self.document.display()

    self.send_to_other_servers('insert', request.index, request.char)

    return document_pb2.Response(message='The insert command sent by client was applied')

  def DeleteCommand(self, request, context):
    print('El client envio: %s' % request)

    self.document.delete_by_index(request.index)
    self.document.apply_operations()
    self.document.display()

    self.send_to_other_servers('delete', request.index, None)

    return document_pb2.Response(message='The delete command sent by client was applied')

  # methods that communicate commands to others servers
  def SendInsert(self, request, context):
    print('El server envio: %s' % request)
    self.document.insert_by_index(request.index, request.char)
    self.document.apply_operations()
    self.document.display()
    return document_pb2.Response(message='The insert command sent by server was applied')

  def SendDelete(self, request, context):
    print('El server envio: %s' % request)
    self.document.delete_by_index(request.index)
    self.document.apply_operations()
    self.document.display()
    return document_pb2.Response(message='The delete command sent by server was applied')

  def send_to_other_server(self, command, index, char, port):
    with grpc.insecure_channel('localhost:' + port) as channel:
      stub = document_pb2_grpc.DocumentServiceStub(channel)
      if (command == 'insert'):
        #falta agregar replica_id
        response = stub.SendInsert(document_pb2.InsertParams(index=int(index), char=char, server_id=self.server_id, tumbstamp=False, timestamp='', replica_id='1A'))
      elif (command == 'delete'):
        #falta agregar replica_id
        response = stub.SendDelete(document_pb2.DeleteParams(index=int(index), server_id=self.server_id, tumbstamp=True, timestamp='', replica_id='1A'))

      print("Document client received: " + response.message)

  def send_to_other_servers(self, command, index, char):
    if (self.server_id == 1):
      self.send_to_other_server(command, index, char, '50052')
      self.send_to_other_server(command, index, char, '50053')
    elif (self.server_id == 2):
      self.send_to_other_server(command, index, char, '50051')
      self.send_to_other_server(command, index, char, '50053')
    elif (self.server_id == 3):
      self.send_to_other_server(command, index, char, '50051')
      self.send_to_other_server(command, index, char, '50052')

def serve(server_id, port):
  #port = "50051"
  document = DocumentService(server_id)
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  document_pb2_grpc.add_DocumentServiceServicer_to_server(document, server)

  server.add_insecure_port("[::]:" + port)
  server.start()
  print("Server started, listening on " + port)
  server.wait_for_termination()

if __name__ == "__main__":
  server_id = sys.argv[1]
  port = ''

  if (server_id == '1'):
    port = '50051'
  elif (server_id == '2'):
    port = '50052'
  elif (server_id == '3'):
    port = '50053'

  serve(int(server_id), port)
