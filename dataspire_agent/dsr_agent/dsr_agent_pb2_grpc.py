# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import dsr_agent_pb2 as dsr__agent__pb2


class DsrAgentStub(object):
    """The service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMessage = channel.unary_unary(
                '/dsr_agent.DsrAgent/SendMessage',
                request_serializer=dsr__agent__pb2.GRPCMessagePackage.SerializeToString,
                response_deserializer=dsr__agent__pb2.ServerReply.FromString,
                )


class DsrAgentServicer(object):
    """The service definition.
    """

    def SendMessage(self, request, context):
        """Sends a message
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DsrAgentServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=dsr__agent__pb2.GRPCMessagePackage.FromString,
                    response_serializer=dsr__agent__pb2.ServerReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dsr_agent.DsrAgent', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DsrAgent(object):
    """The service definition.
    """

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dsr_agent.DsrAgent/SendMessage',
            dsr__agent__pb2.GRPCMessagePackage.SerializeToString,
            dsr__agent__pb2.ServerReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
