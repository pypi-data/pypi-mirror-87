from typing import Any

import grpc

from aipod.model import AIModelBase
from aipod.rpc import decode_data
from aipod.rpc import encode_data
from aipod.rpc.proto import ai_pb2_grpc
from aipod.rpc.proto.ai_pb2 import Input


class AIClient(AIModelBase):
    def __init__(self, address=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.address = address
        if not address:
            raise Exception("missing rpc server address")
        self.channel = grpc.insecure_channel(address)
        self.stub = ai_pb2_grpc.AIStub(self.channel)

    def initialize(self, binary_data: bytes = None, **kwargs) -> Any:
        response = self.stub.initialize(
            Input(
                kwargs_json=encode_data(kwargs),
                version=self.version,
                binary_data=binary_data,
            )
        )
        return decode_data(response.data_json)

    def train(self, binary_data: bytes = None, **kwargs) -> Any:
        response = self.stub.train(
            Input(
                kwargs_json=encode_data(kwargs),
                version=self.version,
                binary_data=binary_data,
            )
        )
        return decode_data(response.data_json)

    def predict(self, binary_data: bytes = None, **kwargs) -> Any:
        response = self.stub.predict(
            Input(
                kwargs_json=encode_data(kwargs),
                version=self.version,
                binary_data=binary_data,
            )
        )
        return decode_data(response.data_json)

    def log(self, binary_data: bytes = None, **kwargs) -> Any:
        response = self.stub.log(
            Input(
                kwargs_json=encode_data(kwargs),
                version=self.version,
                binary_data=binary_data,
            )
        )
        return decode_data(response.data_json)
