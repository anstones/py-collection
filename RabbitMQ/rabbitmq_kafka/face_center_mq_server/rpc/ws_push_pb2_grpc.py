# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import rpc.ws_push_pb2 as ws__push__pb2


class WsPushHandlerStub(object):
  """The WsPushHandler service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.PushToWsClient = channel.unary_unary(
        '/ws_push.WsPushHandler/PushToWsClient',
        request_serializer=ws__push__pb2.WsPushRequest.SerializeToString,
        response_deserializer=ws__push__pb2.WsPushReply.FromString,
        )


class WsPushHandlerServicer(object):
  """The WsPushHandler service definition.
  """

  def PushToWsClient(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WsPushHandlerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'PushToWsClient': grpc.unary_unary_rpc_method_handler(
          servicer.PushToWsClient,
          request_deserializer=ws__push__pb2.WsPushRequest.FromString,
          response_serializer=ws__push__pb2.WsPushReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ws_push.WsPushHandler', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
