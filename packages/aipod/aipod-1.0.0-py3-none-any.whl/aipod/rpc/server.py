import os
import time

from concurrent import futures
from typing import ClassVar
from typing import Dict

import grpc

from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel

from aipod.model import AIModelBase
from aipod.pool import ModelPool
from aipod.rpc import decode_data
from aipod.rpc import encode_data
from aipod.rpc.proto import ai_pb2_grpc
from aipod.rpc.proto.ai_pb2 import Input
from aipod.rpc.proto.ai_pb2 import Output


class AIServicer(ai_pb2_grpc.AIServicer):
    def __init__(self, model_class: ClassVar[AIModelBase]) -> None:
        self.instance_pool = ModelPool(
            model_class,
            size=os.environ.get("AIPOD_MODEL_POOL_SIZE"),
            datapath=os.environ.get("AIPOD_DATA_PATH"),
        )

    def _build_input_kwargs(self, input_request: Input) -> Dict:
        kwargs = decode_data(input_request.kwargs_json)
        kwargs.update(binary_data=input_request.binary_data)
        return kwargs

    def initialize(self, request: Input, context) -> Output:
        model = self.instance_pool.get(request.version)
        model_info = decode_data(request.kwargs_json)
        model.initialize(**model_info)
        return Output(data_json=encode_data({"result": True}))

    def train(self, request: Input, context) -> Output:
        kwargs = self._build_input_kwargs(request)
        model = self.instance_pool.get(request.version)
        res = model.train(**kwargs)
        del model
        self.instance_pool.release(request.version)
        return Output(data_json=encode_data(res))

    def log(self, request: Input, context) -> Output:
        kwargs = self._build_input_kwargs(request)
        model = self.instance_pool.get(request.version)
        res = model.log(**kwargs)
        return Output(data_json=encode_data(res))

    def predict(self, request: Input, context) -> Output:
        kwargs = self._build_input_kwargs(request)
        model = self.instance_pool.get(request.version)
        res = model.predict(**kwargs)
        return Output(data_json=encode_data(res))


class Serve:
    def __init__(self, model: AIModelBase, port: int = None):
        self.model = model
        self.port = port or int(os.environ.get("AIPOD_LISTEN_PORT") or "50051")
        self.address = "[::]:{}".format(self.port)
        self.rpc_max_workers = int(os.environ.get("AIPOD_RPC_MAX_WORKERS") or "12")
        self.server = None

    def __enter__(self):
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.rpc_max_workers),
            options=[
                ("grpc.max_receive_message_length", 104857600),
                ("grpc.default_compression_algorithm", CompressionAlgorithm.gzip),
                ("grpc.grpc.default_compression_level", CompressionLevel.high),
            ],
        )
        ai_pb2_grpc.add_AIServicer_to_server(AIServicer(self.model), self.server)
        self.server.add_insecure_port(self.address)
        self.server.start()
        print(f"listening address: {self.address}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server:
            print("RPC server shutdown")
            self.server.stop(0)

    def run(self):
        with self:
            while True:
                try:
                    time.sleep(186400)
                except KeyboardInterrupt:
                    break


def serve(model: AIModelBase, port: int = 0):
    Serve(model, port).run()
