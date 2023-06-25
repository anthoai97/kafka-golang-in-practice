from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GRPCMessagePackage(_message.Message):
    __slots__ = ["agent", "agent_id", "data", "resend", "timestamp"]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    RESEND_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    agent: str
    agent_id: str
    data: str
    resend: int
    timestamp: str
    def __init__(self, agent: _Optional[str] = ..., agent_id: _Optional[str] = ..., data: _Optional[str] = ..., timestamp: _Optional[str] = ..., resend: _Optional[int] = ...) -> None: ...

class ServerReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
