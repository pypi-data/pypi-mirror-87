from points_fl.base import Base
from points_fl.proto import inference_pb2


class Inference(Base):

    def create_model(self, job_id, name):
            return self._inference_stub.CreateModel(inference_pb2.CreateModelRequest(job_id=job_id, name=name, token=self._token))

    def read_model(self, id):
            return self._inference_stub.ReadModel(inference_pb2.ReadModelRequest(id=id, token=self._token))

    def read_model_list(self, type):
            return self._inference_stub.ReadModelList(inference_pb2.ReadModelListRequest(type=type, token=self._token))

    def update_model(self, model):
            return self._inference_stub.UpdateModel(inference_pb2.UpdateModelRequest(model=model, token=self._token))

    def delete_model(self, id):
            return self._inference_stub.DeleteModel(inference_pb2.DeleteModelRequest(id=id, token=self._token))

    def create_service(self, model_id, name):
            return self._inference_stub.CreateService(inference_pb2.CreateServiceRequest(model_id=model_id, name=name, token=self._token))

    def read_service(self, id):
            return self._inference_stub.ReadService(inference_pb2.ReadServiceRequest(id=id, token=self._token))

    def read_service_list(self):
            return self._inference_stub.ReadServiceList(inference_pb2.ReadServiceListRequest(token=self._token))

    def delete_service(self, id):
            return self._inference_stub.DeleteService(inference_pb2.DeleteServiceRequest(id=id, token=self._token))

    def update_service(self, service):
            return self._inference_stub.UpdateService(inference_pb2.UpdateServiceRequest(service=service, token=self._token))
