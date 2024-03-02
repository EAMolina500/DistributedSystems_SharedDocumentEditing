import grpc
import document_pb2
import document_pb2_grpc
from concurrent import futures

import sys
import rga
import client
import document_service
import server_communication_service
import vector_clock

class Server:
  def __init__(self, server_id, port):
    self._server_id = server_id
    self._port = port
    self._crdt_array = None

  def run_server(self, document_service, server_communication_service):
    #document_service.set_server_id(self._server_id)
    self.set_crdt_array(document_service.get_crdt_array())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    document_pb2_grpc.add_DocumentServiceServicer_to_server(document_service, server)
    document_pb2_grpc.add_ServerCommunicationServiceServicer_to_server(server_communication_service, server)
    server.add_insecure_port(f"[::]:{self._port}")
    server.start()
    print("Servidor gRPC iniciado en el puerto / Escuchando en el puerto " + self._port + "...")
    # Posiblemente hacer un ciclo infinito que escuche los mensajes de los clientes para actuar en consecuencia
    while True:
      self.send_message_to_servers(self._server_id, document_service, self._crdt_array.get_operations_array())
      self.merge(server_communication_service)
    server.wait_for_termination()

  def send_message_to_servers(self, server_id, document_service, operations_array):
    if document_service.send_command():
      if (server_id == 1):
        port_1 = '50052'
        port_2 = '50053'
      elif (server_id == 2):
        port_1 = '50051'
        port_2 = '50053'
      elif (server_id == 3):
        port_1 = '50051'
        port_2 = '50052'
      else:
        print('Invalid server id')

      self.send_message_to_server(port_1, operations_array)
      self.send_message_to_server(port_2, operations_array)
      document_service.reset_send_command()

  def send_message_to_server(self, port, operations_array):
    try:
      channel = grpc.insecure_channel(f'localhost:{port}')
      print('1')
      stub = document_pb2_grpc.ServerCommunicationServiceStub(channel)
      print('2')
      response = self.get_response(stub, operations_array)
      print('3')
      print(f"Respuesta del servidor: {response}")
      print('4')
    except:
      print('Servers down')

  def get_response(self, stub, operations_array):
    index = len(operations_array)-1

    print('INDEX: ' + str(index))
    op = operations_array[index]

    print('OPERACION: ' + str(op))

    response = stub.SendMessageToServers(document_pb2.Operation(
      server_id=op['server_id'],
      file_name=op['file_name'],
      command=op['command'],
      position=op['position'],
      character=op['character'],
      tumbstamp=op['tumbstamp'],
      timestamp=op['timestamp'],
      replica_id=op['replica_id']
    ))

    return response

  def merge(self, server_communication_service):
    request_1 = None
    request_2 = None

    if (self._server_id == 1):
      request_1 = server_communication_service.get_request_from_server2()
      request_2 = server_communication_service.get_request_from_server3()
    elif (self._server_id == 2):
      request_1 = server_communication_service.get_request_from_server1()
      request_2 = server_communication_service.get_request_from_server3()
    elif (self._server_id == 3):
      request_1 = server_communication_service.get_request_from_server1()
      request_2 = server_communication_service.get_request_from_server2()
    else:
      print('Invalid server id')

    reqs_number = 0

    if (request_1 and request_2):
      reqs_number = 2
    elif (request_1):
      request = request_1
      reqs_number = 1
    elif (request_2):
      request = request_2
      reqs_number = 1
    else:
      aux = True # eliminar
      #print('Request are None')

    if reqs_number > 0 and server_communication_service.apply_command():
      if request_1:
        print('request from server 1 o 2:')
        print(request_1)
      if request_2:
        print('request from server 2 o 3:')
        print(request_2)

      if reqs_number == 1:
        # Caso: llega una request
        # Actualizo vector clock local
        local_vector_clock = self._crdt_array._vector_clock
        print('local clock: ' + str(local_vector_clock.get_value()))
        local_vector_clock.increment(self._server_id)
        print('updated local clock: ' + str(local_vector_clock.get_value()))

        # Aplico operacion recibida
        self.add_operation_from_request(request)
        self._crdt_array.apply_operations()

      elif reqs_number == 2:
        vector_clock_1 = vector_clock.VectorClock(request_1.timestamp)
        vector_clock_2 = vector_clock.VectorClock(request_2.timestamp)
        result = vector_clock_1.compare(vector_clock_2)

        if self.insert_conflict(request_1, request_2):
          if (result == 1): # vector_clock_1 mas grande
            self.add_operation_from_request(request_2)
            self.add_operation_from_request(request_1)
          elif (result == -1):
            self.add_operation_from_request(request_1)
            self.add_operation_from_request(request_2)
          else:
            if (request_1.replica_id < request_2.replica_id):
              request_2.position += 1
              self.add_operation_from_request(request_1)
              self.add_operation_from_request(request_2)
            else:
              request_1.position += 1
              self.add_operation_from_request(request_2)
              self.add_operation_from_request(request_1)
        else:
          if (result == 1): # vector_clock_1 mas grande
            self.add_operation_from_request(request_2)
            self.add_operation_from_request(request_1)
          elif (result == -1):
            self.add_operation_from_request(request_1)
            self.add_operation_from_request(request_2)
          else:
            print('Vector clocks iguales o nulos')

        self._crdt_array.apply_operations()

      else:
        print('REQS_NUMBER NO ES NI 1 NI 2 / WTF ???')

      server_communication_service.reset_apply_command()

  def insert_conflict(self, request_1, request_2):
    return request_1.command == 'insert' and request_2.command == 'insert' and request_1.position == request_2.position

  def add_operation_from_request(self, request):
    self._crdt_array.add_operation(
      server_id=request.server_id,
      file_name=request.file_name,
      command=request.command,
      position=request.position,
      character=request.character,
      tumbstamp=request.tumbstamp,
      timestamp=request.timestamp,
      replica_id=request.replica_id
    )

  def set_crdt_array(self, crdt_array):
    self._crdt_array = crdt_array

    """
    comp = self._crdt_array.timestamp.compare(request.timestamp) # Esto no funciona, debo comparar relojes no arreglos
    # Tambien debo serializar el arreglo
    if comp == 1:
      ...
    elif comp == -1
      self._crdt_array.insert(request)
    elif comp == 0
      ...
    else: # comp is None
      self._crdt_array.replica_id < request.replica_id

    # Cuando llega un mensaje
    #1. Incremento en uno el reloj vectorial para el nodo corriente
    self._crdt_op.increment_vector_clock()
    #2. vc[0] = max(vc_cur[0], vc_ot[0]) // Actualizo el reloj vectorial del server corriente
    self._crdt_op._vector_clock = self.aux(self._crdt_op._vector_clock, request.timestamp) # Hacer funcion en la clase rga
    """

if __name__ == "__main__":
  server_id = int(sys.argv[1])

  if (server_id == 1):
    port = '50051'
  elif (server_id == 2):
    port = '50052'
  elif (server_id == 3):
    port = '50053'
  else:
    print('Invalid param')

  server = Server(server_id, port)
  sc_service = server_communication_service.ServerCommunicationService()
  d_service = document_service.DocumentService(server_id)
  server.run_server(d_service, sc_service)
