import grpc
import document_pb2
import document_pb2_grpc

import rga
import document

class DocumentService(document_pb2_grpc.DocumentServiceServicer):
  def __init__(self, server_id):
    self._send_command = False
    self._server_id = server_id
    self._crdt_array = rga.RGA(server_id=server_id)
    self._document = None

  def CreateCommand(self, request, context):
    print("document service / create command")
    self._crdt_array.create(request.file_name)
    self._send_command = True
    print(f"Recibido comando de edición: {request}")
    return document_pb2.Response(message="Comando de edición recibido correctamente.")

  def InsertCommand(self, request, context):
    self._crdt_array.insert(request.position, request.character)
    self._send_command = True
    print(f"Recibido comando de edición: {request}")
    return document_pb2.Response(message="Caracter insertado correctamente.")

  def DeleteCommand(self, request, context):
    self._crdt_array.delete(request.position)
    self._send_command = True
    print(f"Recibido comando de edición: {request}")
    return document_pb2.Response(message="Caracter borrado correctamente.")

  def DisplayCommand(self, request, context):
    self._crdt_array.display()
    print(f"Recibido comando de edición: {request}")
    return document_pb2.Response(message="Comando recibido correctamente.")

  def send_command(self):
    return self._send_command

  def reset_send_command(self):
    self._send_command = False

  def set_server_id(self, server_id):
    self._server_id = server_id
    #self._crdt_array.set_server_id(self._server_id)

  def get_crdt_array(self):
    return self._crdt_array
