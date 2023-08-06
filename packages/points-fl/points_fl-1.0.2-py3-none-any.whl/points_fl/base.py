from types import MethodType

import grpc

from points_fl.proto import federated_learning_pb2, federated_learning_pb2_grpc, permission_pb2_grpc, permission_pb2, \
    log_provider_pb2_grpc, inference_pb2_grpc


def verify_login(cls):
    orig_getattribute = cls.__getattribute__

    def new_getattribute(self, name):
        res = orig_getattribute(self, name)
        # 判断除登录外的其他函数，如果还没有登录，则跑出异常
        if name not in ['login', 'admin_login'] and isinstance(res, MethodType) \
                and orig_getattribute(self, '_connected') is False:
            raise BrokenPipeError('未登录')

        return res

    cls.__getattribute__ = new_getattribute
    return cls


@verify_login
class Base:
    """
    基类，创建连接，登录及关闭验证
    """
    def __init__(self, grpc_ip_address, flask_ip_address):
        self._channel = grpc.insecure_channel(grpc_ip_address)
        self._flask_ip_address = flask_ip_address
        self._connected = False
        self._token = ''
        self._headers = {}
        self._federated_learning_stub = federated_learning_pb2_grpc.FederatedLearningServiceStub(self._channel)
        self._permission_stub = permission_pb2_grpc.PermissionStub(self._channel)
        self._log_provider_stub = log_provider_pb2_grpc.LogProviderStub(self._channel)
        self._inference_stub = inference_pb2_grpc.InferenceStub(self._channel)

    def login(self, username, password):
        request = federated_learning_pb2.LoginRequest(username=username, password=password)
        response = self._federated_learning_stub.Login(request)
        self._token = response.token
        self._connected = True
        self._headers = {'Authorization': f'bearer {self._token}'}

    def admin_login(self, username, password):
        request = permission_pb2.BackstageLoginRequest(username=username, password=password)
        response = self._permission_stub.BackstageLogin(request)
        self._token = response.token
        self._connected = True

    def close(self):
        self._channel.close()
        self._connected = False
