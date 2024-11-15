from concurrent import futures

import grpc
import document_pb2
import document_pb2_grpc

from document import Document
from vector_clock import VectorClock
from operation import Operation

import sys

class DocumentService(document_pb2_grpc.DocumentServiceServicer):
  def __init__(self, server_id):
    self._document = Document(server_id)
    self._server_id = int(server_id)
    self._ops_number = 0
    # esto va a funcionar siempre que el server no se caiga
    self._pending_msgs = {'50051': False, '50052': False, '50053': False}

    if self._document.get_operations():
      self._vector_clock = self._document.get_last_clock()
    else:
      self._vector_clock = VectorClock(server_id)

    if (self._server_id == 1):
      got_it = request_pending_messages(self._document, '50052')
      if not got_it:
        request_pending_messages(self._document, '50053')
    elif (self._server_id == 2):
      got_it = request_pending_messages(self._document, '50051')
      if not got_it:
        request_pending_messages(self._document, '50053')
    elif (self._server_id == 3):
      got_it = request_pending_messages(self._document, '50051')
      if not got_it:
        request_pending_messages(self._document, '50052')

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

    print('Insert command - SEND:\n')
    print('Vector before increment:\n')
    print(self._vector_clock)

    self._vector_clock.increment()
    print('Vector after increment:\n')
    print(self._vector_clock)
    replica_id = self.gen_replica_id()

    self._document.insert(request.index, request.char, self._vector_clock.get_clock(), replica_id)
    self._document.apply_operations()
    self._document.display()

    try:
      send_to_other_servers('insert', request.index, request.char, self._vector_clock.get_clock(), replica_id, self._server_id)
    except:
      self._pending_msgs[get_server_port(self._server_id)]

    return document_pb2.Response(message='The insert command sent by client was applied')

  def DeleteCommand(self, request, context):
    print('El client envio: %s' % request)

    print('Delete command - SEND:\n')
    print('Vector before increment:\n')
    print(self._vector_clock)

    self._vector_clock.increment()
    print('Vector after increment:\n')
    print(self._vector_clock)
    replica_id = self.gen_replica_id()

    self._document.delete(request.index, self._vector_clock.get_clock(), replica_id)
    self._document.apply_operations()
    self._document.display()

    try:
      send_to_other_servers('delete', request.index, None, self._vector_clock.get_clock(), replica_id, self._server_id)
    except:
      self._pending_msgs[get_server_port(self._server_id)]

    return document_pb2.Response(message='The delete command sent by client was applied')

  # methods that communicate commands to others servers
  def SendInsert(self, request, context):
    print('El server envio: %s' % request)

    print('Insert command - GET:\n')
    print('Vector before increment:\n')
    print(self._vector_clock)

    self._vector_clock.increment()

    print('Vector after increment:\n')
    print(self._vector_clock)

    sent_vector_clock = VectorClock(self._server_id, list(request.timestamp))
    self._vector_clock.compute_new(sent_vector_clock)

    print('New vector:\n')
    print(self._vector_clock)

    print('Sent vector clock:\n')
    print(sent_vector_clock)

    self._document.insert(request.index, request.char, sent_vector_clock.get_clock(), request.replica_id)
    self._document.apply_operations()
    self._document.display()
    return document_pb2.Response(message='The insert command sent by server was applied')

  def SendDelete(self, request, context):
    print('El server envio: %s' % request)

    print('Delete command - GET:\n')
    print('Vector before increment:\n')
    print(self._vector_clock)

    self._vector_clock.increment()

    print('Vector after increment:\n')
    print(self._vector_clock)

    sent_vector_clock = VectorClock(self._server_id, list(request.timestamp))
    self._vector_clock.compute_new(sent_vector_clock)

    print('New vector:\n')
    print(self._vector_clock)

    print('Sent vector clock:\n')
    print(sent_vector_clock)

    self._document.delete(request.index, sent_vector_clock.get_clock(), request.replica_id)
    self._document.apply_operations()
    self._document.display()
    return document_pb2.Response(message='The delete command sent by server was applied')

  def SendPendingMessages(self, request, context):
    params = []
    ops = self._document.get_operations()

    if len(ops) > 0:
      for op in ops:
        params.append(op_to_params(op, self._server_id))

    return document_pb2.ParamsList(params=params)

def op_to_params(op, server_id):
  return document_pb2.Params(
    operation=op.get_name(),
    index=op.get_index(),
    char=op.get_char(),
    server_id=server_id,
    tumbstamp =op.get_deleted(),
    timestamp =op.get_clock(),
    replica_id =op.get_replica_id()
  )

def get_server_port(server_id):
  if (server_id == 1):
    return 50051
  elif (server_id == 2):
    return 50052
  elif (server_id == 3):
    return 50053

def request_pending_messages(document, port):
  try:
    with grpc.insecure_channel('localhost:' + port) as channel:
      stub = document_pb2_grpc.DocumentServiceStub(channel)
      response = stub.SendPendingMessages(document_pb2.Request(message="I'm up and running", server_port=port))

      ops = []
      for params in response.params:
        op = Operation(params.operation, params.index, params.char, params.timestamp, params.replica_id)
        ops.append(op)

      print('ops:')
      print(ops)

      #ops.reverse()
      document.set_operations(ops)

      return True
  except:
    print("server doesn't response")

    return False


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
    # esto va a funcionar siempre que el server no se caiga
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

def serve(server_id, port):
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
