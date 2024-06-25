from concurrent import futures

import grpc
import document_pb2
import document_pb2_grpc

from document import Document
from operation import Operation
from copy import copy
from auxiliar_functions import AuxiliarFunctions as AUX

from threading import Thread, Lock

import sys

class DocumentService(document_pb2_grpc.DocumentServiceServicer):
  def __init__(self, server_id):
    self._document = Document(server_id)
    self._server_id = int(server_id)
    self._operations_number = 0
    self._operation_lock = Lock()

    if self._document.get_operations():
      self._vector_clock = self._document.get_last_clock()
    else:
      self._vector_clock = AUX.get_initial_clock()

    handle_pending_messages(self._server_id, self._document)

  def gen_replica_id(self):
    self._operations_number += 1
    return AUX.gen_replica_id(self._server_id, self._operations_number)

  # Methods that listen client requests

  def InsertCommand(self, request, context):
    with self._operation_lock:
      print('El client envio: %s\n' % request)

      self._vector_clock = AUX.increment(self._vector_clock, self._server_id)
      vector_clock_copy = copy(self._vector_clock)
      replica_id = self.gen_replica_id()

      self._document.insert(request.index, request.char, vector_clock_copy, replica_id)
      self._document.display()

      try:
        send_to_other_servers('insert', request.index, request.char, vector_clock_copy, replica_id, self._server_id)
      except Exception as e:
        print(f'Unexpected exception occurred while sending message to another server: {e}')

    return document_pb2.Response(message='The insert command sent by client was applied')

  def DeleteCommand(self, request, context):
    with self._operation_lock:
      print('El client envio: %s\n' % request)

      self._vector_clock = AUX.increment(self._vector_clock, self._server_id)
      vector_clock_copy = copy(self._vector_clock)
      replica_id = self.gen_replica_id()

      self._document.delete(request.index, vector_clock_copy, replica_id)
      self._document.display()

      try:
        send_to_other_servers('delete', request.index, None, vector_clock_copy, replica_id, self._server_id)
      except Exception as e:
        print(f'Unexpected exception occurred while sending message to another server: {e}')

    return document_pb2.Response(message='The delete command sent by client was applied')

  def DisplayCommand(self, request, context):
    with self._operation_lock:
      print('El client envio: %s\n' % request)

      self._document.apply_operations()
      self._document.display()

    return document_pb2.Response(message='The display command sent by client was applied')

  # Methods that communicate commands to others servers

  def SendInsert(self, request, context):
    print('El server envio: %s' % request)

    self._vector_clock = AUX.increment(self._vector_clock, self._server_id)
    sent_vector_clock = list(request.timestamp)
    self._vector_clock = AUX.compute_new(self._vector_clock, sent_vector_clock)

    self._document.insert(request.index, request.char, sent_vector_clock, request.replica_id)
    self._document.display()
    return document_pb2.Response(message='The insert command sent by server was applied')

  def SendDelete(self, request, context):
    print('El server envio: %s' % request)

    self._vector_clock = AUX.increment(self._vector_clock, self._server_id)
    sent_vector_clock = list(request.timestamp)
    self._vector_clock = AUX.compute_new(self._vector_clock, sent_vector_clock)

    self._document.delete(request.index, sent_vector_clock, request.replica_id)
    self._document.display()
    return document_pb2.Response(message='The delete command sent by server was applied')

  def SendPendingMessages(self, request, context):
    params = []
    operations = self._document.get_operations()

    if len(operations) > 0:
      for op in operations:
        params.append(AUX.operation_to_params(op, self._server_id))

    return document_pb2.ParamsList(params=params)

# Auxiliar functions to communication between servers

def handle_pending_messages(server_id, document):
  if server_id == 1:
    request_pending_messages_from(document, '50052', '50053')
  elif server_id == 2:
    request_pending_messages_from(document, '50051', '50053')
  elif server_id == 3:
    request_pending_messages_from(document, '50051', '50052')

def request_pending_messages_from(document, port1, port2):
  if not request_pending_messages(document, port1):
    if not request_pending_messages(document, port2):
      print("Warning: Document may not be fully updated due to communication issues with other servers.")


def request_pending_messages(document, port):
  try:
    with grpc.insecure_channel('localhost:' + port) as channel:
      stub = document_pb2_grpc.DocumentServiceStub(channel)
      response = stub.SendPendingMessages(document_pb2.Request(message="I'm up and running", server_port=port))

      ops = []
      for params in response.params:
        op = Operation(params.operation, params.index, params.char if params.char != '' else None, params.timestamp, params.replica_id)
        ops.append(op)

      document.set_operations(ops)
      return True

  except Exception:
    print("Error: Failed to communicate with server or server is not responding.")
    return False


def send_to_other_server(command, index, char, port, timestamp, replica_id, server_id):
  try:
    with grpc.insecure_channel('localhost:' + port) as channel:
      stub = document_pb2_grpc.DocumentServiceStub(channel)
      if (command == 'insert'):
        response = stub.SendInsert(document_pb2.InsertParams(index=int(index), char=char, server_id=server_id, tumbstamp=False, timestamp=timestamp, replica_id=replica_id))
      elif (command == 'delete'):
        response = stub.SendDelete(document_pb2.DeleteParams(index=int(index), server_id=server_id, tumbstamp=True, timestamp=timestamp, replica_id=replica_id))

  except Exception:
    print("Error: Failed to communicate with server or server is not responding.")

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

# Main code

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

  serve(server_id, port)
