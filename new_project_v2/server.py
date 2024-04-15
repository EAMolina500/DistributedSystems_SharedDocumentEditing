from concurrent import futures

import grpc
import document_pb2
import document_pb2_grpc

import document as doc
import file

import sys

class DocumentService(document_pb2_grpc.DocumentServiceServicer):
  def __init__(self, server_id):
    self._document = doc.Document(server_id)
    self._server_id = int(server_id)
    self._vector_clock = [0,0,0]
    self._ops_number = 0
    self._file = file.File(self._document._file_name)

    ops = self._file.from_file_to_array()
    self._document.set_operations(ops)

  def gen_replica_id(self):
    self._ops_number += 1
    replica_id = str(self._ops_number)
    if (self._server_id == 1):
      replica_id += 'A'
    elif (self._server_id == 2):
      replica_id += 'B'
    elif (self._server_id == 3):
      replica_id += 'C'

    return replica_id

  # methods that listen client requests
  def InsertCommand(self, request, context):
    print('El client envio: %s' % request)

    self._vector_clock[self._server_id - 1] += 1
    replica_id = self.gen_replica_id()

    self._document.insert(request.index, request.char, self._vector_clock, replica_id)
    self._document.apply_operations()
    self._document.display()

    send_to_other_servers('insert', request.index, request.char, self._vector_clock, replica_id, self._server_id)

    return document_pb2.Response(message='The insert command sent by client was applied')

  def DeleteCommand(self, request, context):
    print('El client envio: %s' % request)

    self._vector_clock[self._server_id - 1] += 1
    replica_id = self.gen_replica_id()

    self._document.delete(request.index, self._vector_clock, replica_id)
    self._document.apply_operations()
    self._document.display()

    send_to_other_servers('delete', request.index, None, self._vector_clock, replica_id, self._server_id)

    return document_pb2.Response(message='The delete command sent by client was applied')

  # methods that communicate commands to others servers
  def SendInsert(self, request, context):
    print('El server envio: %s' % request)

    self._vector_clock[self._server_id - 1] += 1
    sent_vector_clock = list(request.timestamp)
    self._vector_clock = compute_new(self._vector_clock, sent_vector_clock)

    # es el sent_vector el que debo mandar ???
    self._document.insert(request.index, request.char, sent_vector_clock, request.replica_id)
    self._document.apply_operations()
    self._document.display()
    return document_pb2.Response(message='The insert command sent by server was applied')

  def SendDelete(self, request, context):
    print('El server envio: %s' % request)

    self._vector_clock[self._server_id - 1] += 1
    sent_vector_clock = list(request.timestamp)
    self._vector_clock = compute_new(self._vector_clock, sent_vector_clock)

    # es el sent_vector el que debo mandar ???
    self._document.delete(request.index, sent_vector_clock, request.replica_id)
    self._document.apply_operations()
    self._document.display()
    return document_pb2.Response(message='The delete command sent by server was applied')



def send_to_other_server(command, index, char, port, timestamp, replica_id, server_id):
  try:
    with grpc.insecure_channel('localhost:' + port) as channel:
      stub = document_pb2_grpc.DocumentServiceStub(channel)
      if (command == 'insert'):
        #falta agregar replica_id
        response = stub.SendInsert(document_pb2.InsertParams(index=int(index), char=char, server_id=server_id, tumbstamp=False, timestamp=timestamp, replica_id=replica_id))
      elif (command == 'delete'):
        #falta agregar replica_id
        response = stub.SendDelete(document_pb2.DeleteParams(index=int(index), server_id=server_id, tumbstamp=True, timestamp=timestamp, replica_id=replica_id))

      print("Document client received: " + response.message)
  except:
    print("server doesn't works")

def send_to_other_servers(command, index, char, timestamp, replica_id, server_id):
  if (server_id == 1):
    send_to_other_server(command, index, char, '50052', timestamp, replica_id, server_id)
    send_to_other_server(command, index, char, '50053', timestamp, replica_id, server_id)
  elif (server_id == 2):
    send_to_other_server(command, index, char, '50051', timestamp, replica_id, server_id)
    send_to_other_server(command, index, char, '50053', timestamp, replica_id, server_id)
  elif (server_id == 3):
    send_to_other_server(command, index, char, '50051', timestamp, replica_id, server_id)
    send_to_other_server(command, index, char, '50052', timestamp, replica_id, server_id)

def compute_new(clock1, clock2):
  return [max(a, b) for a, b in zip(clock1, clock2)]

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
