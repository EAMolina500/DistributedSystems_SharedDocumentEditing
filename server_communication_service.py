import grpc
import document_pb2
import document_pb2_grpc

class ServerCommunicationService(document_pb2_grpc.ServerCommunicationServiceServicer):
  def __init__(self):
    self._request_from_server1 = None
    self._request_from_server2 = None
    self._request_from_server3 = None
    self._apply_command = False

  def SendMessageToServers(self, request, context):
    print(f"Received message from server: {request}")

    if (request.server_id == 1):
      self.set_request_from_server1(request)
    elif (request.server_id == 2):
      self.set_request_from_server2(request)
    elif (request.server_id == 3):
      self.set_request_from_server3(request)
    else:
      print("invalid request server id")

    self._apply_command = True
    return document_pb2.Response(message="Message received")

  def apply_command(self):
    return self._apply_command

  def reset_apply_command(self):
    self._apply_command = False

  def get_request_from_server1(self):
    return self._request_from_server1

  def get_request_from_server2(self):
    return self._request_from_server2

  def get_request_from_server3(self):
    return self._request_from_server3

  def set_request_from_server1(self, request):
    self._request_from_server1 = request

  def set_request_from_server2(self, request):
    self._request_from_server2 = request

  def set_request_from_server3(self, request):
    self._request_from_server3 = request