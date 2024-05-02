from concurrent import futures

import grpc
import document_pb2
import document_pb2_grpc

from document import Document
from vector_clock import VectorClock

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
      request_pending_messages('50052')
    elif (self._server_id == 2):
      request_pending_messages('50051')
      #request_pending_messages('50053')
    elif (self._server_id == 3):
      request_pending_messages('50051')

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

    self._vector_clock.increment()
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

    self._vector_clock.increment()
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

    self._vector_clock.increment()
    sent_vector_clock = VectorClock(self._server_id, list(request.timestamp))
    # el valor computa queda guardado en el clock de self._vector_clock
    # actualizo el reloj local
    self._vector_clock.compute_new(sent_vector_clock)

    self._document.insert(request.index, request.char, sent_vector_clock.get_clock(), request.replica_id)
    self._document.apply_operations()
    self._document.display()
    return document_pb2.Response(message='The insert command sent by server was applied')

  def SendDelete(self, request, context):
    print('El server envio: %s' % request)

    self._vector_clock.increment()
    sent_vector_clock = VectorClock(list(request.timestamp))
    # el valor computa queda guardado en el clock de self._vector_clock
    # actualizo el reloj local
    self._vector_clock.compute_new(sent_vector_clock)

    self._document.delete(request.index, sent_vector_clock.get_clock(), request.replica_id)
    self._document.apply_operations()
    self._document.display()
    return document_pb2.Response(message='The delete command sent by server was applied')

  # ...
  def SendPendingMessages(self, request, context):
    """
    port = request.port
    params = document_pb2.Params(
      index=1,
      char='X',
      server_id=self._server_id,
      tumbstamp=False,
      timestamp=[0,0,0],
      replica_id='1A'
    )
    params_list = [params]
    print('PARAMS DONE!\n')

    if (self._pending_msgs[port]):
      print('ENTRE AL IF\n')
      for op in self._document.get_operations():
        params = document_pb2.Params(
          index=op.get_index(),
          char=op.get_char(),
          server_id=self._server_id,
          tumbstamp=op.get_deleted(),
          timestamp=op.get_clock(),
          replica_id=op.get_replica_id()
        )
        params_list.append(params)
    print('TERMINE EL CICLO\n')
    """
    print('Request - server post:\n')
    #print(request.server_port)
    return document_pb2.ParamsList(message="Take missing operations")

def get_server_port(server_id):
  if (server_id == 1):
    return 50051
  elif (server_id == 2):
    return 50052
  elif (server_id == 3):
    return 50053

def request_pending_messages(port):
  try:
    with grpc.insecure_channel('localhost:' + port) as channel:
      stub = document_pb2_grpc.DocumentServiceStub(channel)
      response = stub.SendPendingMessages(document_pb2.Request(message="I'm up and running"))
      print('DESPUES DE ARMAR LA RESPONSE\n')
      # paso la lista al document para que reemplace su lista desactualizada
      #self._document.set_operations(request.params)

      print("Pending params: " + response.message)
  except:
    print("server doesn't response")


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
