from points_fl.base import Base
from points_fl.proto import federated_learning_pb2


class FederatedLearning(Base):

    def pre_create_job(self):
            return self._federated_learning_stub.PreCreateJob(federated_learning_pb2.PreCreateJobRequest(token=self._token))

    def create_job(self, description, dataset_id, epoch_count, dataset_config, model_fn, sample, target_name, organization_id, algorithm):
            return self._federated_learning_stub.CreateJob(federated_learning_pb2.CreateJobRequest(description=description, dataset_id=dataset_id, epoch_count=epoch_count, dataset_config=dataset_config, model_fn=model_fn, sample=sample, target_name=target_name, organization_id=organization_id, algorithm=algorithm, token=self._token))

    def read_job_list(self, owner_filter):
            return self._federated_learning_stub.ReadJobList(federated_learning_pb2.ReadJobListRequest(owner_filter=owner_filter, token=self._token))

    def read_job(self, id):
            return self._federated_learning_stub.ReadJob(federated_learning_pb2.ReadJobRequest(id=id, token=self._token))

    def update_job(self, action, id):
        if action == 'start':
            return self._federated_learning_stub.UpdateJob(federated_learning_pb2.UpdateJobRequest(id=id, token=self._token, start=True))
                    
        elif action == 'pause':
            return self._federated_learning_stub.UpdateJob(federated_learning_pb2.UpdateJobRequest(id=id, token=self._token, pause=True))
                        
    def delete_job(self, id):
            return self._federated_learning_stub.DeleteJob(federated_learning_pb2.DeleteJobRequest(id=id, token=self._token))

    def pre_create_vertical_job(self):
            return self._federated_learning_stub.PreCreateVerticalJob(federated_learning_pb2.PreCreateVerticalJobRequest(token=self._token))

    def create_vertical_job(self, description, epoch_count, pre_job_id, dataset_config, model_fn, target_name, target_dataset_id, is_feature_choice, organization_id, algorithm):
            return self._federated_learning_stub.CreateVerticalJob(federated_learning_pb2.CreateVerticalJobRequest(description=description, epoch_count=epoch_count, pre_job_id=pre_job_id, dataset_config=dataset_config, model_fn=model_fn, target_name=target_name, target_dataset_id=target_dataset_id, is_feature_choice=is_feature_choice, organization_id=organization_id, algorithm=algorithm, token=self._token))

    def read_vertical_job_list(self, owner_filter):
            return self._federated_learning_stub.ReadVerticalJobList(federated_learning_pb2.ReadVerticalJobListRequest(owner_filter=owner_filter, token=self._token))

    def read_vertical_job(self, id):
            return self._federated_learning_stub.ReadVerticalJob(federated_learning_pb2.ReadVerticalJobRequest(id=id, token=self._token))

    def update_vertical_job(self, action, id):
        if action == 'start':
            return self._federated_learning_stub.UpdateVerticalJob(federated_learning_pb2.UpdateVerticalJobRequest(id=id, token=self._token, start=True))
                    
        elif action == 'pause':
            return self._federated_learning_stub.UpdateVerticalJob(federated_learning_pb2.UpdateVerticalJobRequest(id=id, token=self._token, pause=True))
                        
    def delete_vertical_job(self, id):
            return self._federated_learning_stub.DeleteVerticalJob(federated_learning_pb2.DeleteVerticalJobRequest(id=id, token=self._token))

    def pre_create_align_job(self):
            return self._federated_learning_stub.PreCreateAlignJob(federated_learning_pb2.PreCreateAlignJobRequest(token=self._token))

    def create_align_job(self, description, dataset_ids, name):
            return self._federated_learning_stub.CreateAlignJob(federated_learning_pb2.CreateAlignJobRequest(description=description, dataset_ids=dataset_ids, name=name, token=self._token))

    def read_align_job_list(self):
            return self._federated_learning_stub.ReadAlignJobList(federated_learning_pb2.ReadAlignJobListRequest(token=self._token))

    def read_align_job(self, id):
            return self._federated_learning_stub.ReadAlignJob(federated_learning_pb2.ReadAlignJobRequest(id=id, token=self._token))

    def update_align_job(self, action, id):
        if action == 'start':
            return self._federated_learning_stub.UpdateAlignJob(federated_learning_pb2.UpdateAlignJobRequest(id=id, token=self._token, start=True))
                    
    def delete_align_job(self, id):
            return self._federated_learning_stub.DeleteAlignJob(federated_learning_pb2.DeleteAlignJobRequest(id=id, token=self._token))

    def pre_create_feature_engineering_job(self):
            return self._federated_learning_stub.PreCreateFeatureEngineeringJob(federated_learning_pb2.PreCreateFeatureEngineeringJobRequest(token=self._token))

    def create_feature_engineering_job(self, description, params, aligned_id, name, target_name, target_dataset_id):
            return self._federated_learning_stub.CreateFeatureEngineeringJob(federated_learning_pb2.CreateFeatureEngineeringJobRequest(description=description, params=params, aligned_id=aligned_id, name=name, target_name=target_name, target_dataset_id=target_dataset_id, token=self._token))

    def read_feature_engineering_job_list(self):
            return self._federated_learning_stub.ReadFeatureEngineeringJobList(federated_learning_pb2.ReadFeatureEngineeringJobListRequest(token=self._token))

    def read_feature_engineering_job(self, id):
            return self._federated_learning_stub.ReadFeatureEngineeringJob(federated_learning_pb2.ReadFeatureEngineeringJobRequest(id=id, token=self._token))

    def update_feature_engineering_job(self, action, id):
        if action == 'start':
            return self._federated_learning_stub.UpdateFeatureEngineeringJob(federated_learning_pb2.UpdateFeatureEngineeringJobRequest(id=id, token=self._token, start=True))
                    
    def delete_feature_engineering_job(self, id):
            return self._federated_learning_stub.DeleteFeatureEngineeringJob(federated_learning_pb2.DeleteFeatureEngineeringJobRequest(id=id, token=self._token))

    def update_feature_engineering_job_params(self, id, params):
            return self._federated_learning_stub.UpdateFeatureEngineeringJobParams(federated_learning_pb2.UpdateFeatureEngineeringJobParamsRequest(id=id, params=params, token=self._token))

    def pre_create_recommendation_job(self):
            return self._federated_learning_stub.PreCreateRecommendationJob(federated_learning_pb2.PreCreateRecommendationJobRequest(token=self._token))

    def create_recommendation_job(self, description, dataset_id, epoch_count, dataset_config, model_fn, organization_id, algorithm, item_id_name, target_name, sample):
            return self._federated_learning_stub.CreateRecommendationJob(federated_learning_pb2.CreateRecommendationJobRequest(description=description, dataset_id=dataset_id, epoch_count=epoch_count, dataset_config=dataset_config, model_fn=model_fn, organization_id=organization_id, algorithm=algorithm, item_id_name=item_id_name, target_name=target_name, sample=sample, token=self._token))

    def read_recommendation_job_list(self):
            return self._federated_learning_stub.ReadRecommendationJobList(federated_learning_pb2.ReadRecommendationJobListRequest(token=self._token))

    def read_recommendation_job(self, id):
            return self._federated_learning_stub.ReadRecommendationJob(federated_learning_pb2.ReadRecommendationJobRequest(id=id, token=self._token))

    def update_recommendation_job(self, action, id):
        if action == 'start':
            return self._federated_learning_stub.UpdateRecommendationJob(federated_learning_pb2.UpdateRecommendationJobRequest(id=id, token=self._token, start=True))
                    
        elif action == 'pause':
            return self._federated_learning_stub.UpdateRecommendationJob(federated_learning_pb2.UpdateRecommendationJobRequest(id=id, token=self._token, pause=True))
                        
    def delete_recommendation_job(self, id):
            return self._federated_learning_stub.DeleteRecommendationJob(federated_learning_pb2.DeleteRecommendationJobRequest(id=id, token=self._token))

    def approve_job(self, job_id):
            return self._federated_learning_stub.ApproveJob(federated_learning_pb2.ApproveJobRequest(job_id=job_id, token=self._token))

    def read_approval(self, job_id):
            return self._federated_learning_stub.ReadApproval(federated_learning_pb2.ReadApprovalRequest(job_id=job_id, token=self._token))

    def read_approval_list(self, order_by, job_type):
            return self._federated_learning_stub.ReadApprovalList(federated_learning_pb2.ReadApprovalListRequest(order_by=order_by, job_type=job_type, token=self._token))

    def check_job_approval(self, job_id):
            return self._federated_learning_stub.CheckJobApproval(federated_learning_pb2.CheckJobApprovalRequest(job_id=job_id, token=self._token))

    def approve_pre_job(self, id):
            return self._federated_learning_stub.ApprovePreJob(federated_learning_pb2.ApprovePreJobRequest(id=id, token=self._token))

    def read_pre_job_approval(self, id):
            return self._federated_learning_stub.ReadPreJobApproval(federated_learning_pb2.ReadPreJobApprovalRequest(id=id, token=self._token))

    def read_pre_job_approval_list(self, order_by):
            return self._federated_learning_stub.ReadPreJobApprovalList(federated_learning_pb2.ReadPreJobApprovalListRequest(order_by=order_by, token=self._token))

    def check_pre_job_approval(self, id):
            return self._federated_learning_stub.CheckPreJobApproval(federated_learning_pb2.CheckPreJobApprovalRequest(id=id, token=self._token))

    def read_schema_list(self):
            return self._federated_learning_stub.ReadSchemaList(federated_learning_pb2.ReadSchemaListRequest(token=self._token))

    def read_schema(self, id):
            return self._federated_learning_stub.ReadSchema(federated_learning_pb2.ReadSchemaRequest(id=id, token=self._token))

    def create_schema(self, name, column, uid):
            return self._federated_learning_stub.CreateSchema(federated_learning_pb2.CreateSchemaRequest(name=name, column=column, uid=uid, token=self._token))

    def delete_schema(self, id):
            return self._federated_learning_stub.DeleteSchema(federated_learning_pb2.DeleteSchemaRequest(id=id, token=self._token))

    def update_schema(self, schema):
            return self._federated_learning_stub.UpdateSchema(federated_learning_pb2.UpdateSchemaRequest(schema=schema, token=self._token))

    def create_client(self, name, address):
            return self._federated_learning_stub.CreateClient(federated_learning_pb2.CreateClientRequest(name=name, address=address, token=self._token))

    def delete_client(self, id):
            return self._federated_learning_stub.DeleteClient(federated_learning_pb2.DeleteClientRequest(id=id, token=self._token))

    def read_client_list(self):
            return self._federated_learning_stub.ReadClientList(federated_learning_pb2.ReadClientListRequest(token=self._token))

    def read_client(self, id):
            return self._federated_learning_stub.ReadClient(federated_learning_pb2.ReadClientRequest(id=id, token=self._token))

    def update_client(self, client):
            return self._federated_learning_stub.UpdateClient(federated_learning_pb2.UpdateClientRequest(client=client, token=self._token))

    def create_database_dataset(self, database_type, database_ip, database_port, database_schema, database_table, name, schema_id, client_id):
            return self._federated_learning_stub.CreateDatabaseDataset(federated_learning_pb2.CreateDatabaseDatasetRequest(database_type=database_type, database_ip=database_ip, database_port=database_port, database_schema=database_schema, database_table=database_table, name=name, schema_id=schema_id, client_id=client_id, token=self._token))

    def create_dataset(self, name, schema_id, client_id, url):
            return self._federated_learning_stub.CreateDataset(federated_learning_pb2.CreateDatasetRequest(name=name, schema_id=schema_id, client_id=client_id, url=url, token=self._token))

    def delete_dataset(self, id):
            return self._federated_learning_stub.DeleteDataset(federated_learning_pb2.DeleteDatasetRequest(id=id, token=self._token))

    def read_dataset_list(self, client_id):
            return self._federated_learning_stub.ReadDatasetList(federated_learning_pb2.ReadDatasetListRequest(client_id=client_id, token=self._token))

    def update_dataset(self, dataset):
            return self._federated_learning_stub.UpdateDataset(federated_learning_pb2.UpdateDatasetRequest(dataset=dataset, token=self._token))

    def clone_job(self, parent_id):
            return self._federated_learning_stub.CloneJob(federated_learning_pb2.CloneJobRequest(parent_id=parent_id, token=self._token))

    def clone_vertical_job(self, parent_id):
            return self._federated_learning_stub.CloneVerticalJob(federated_learning_pb2.CloneVerticalJobRequest(parent_id=parent_id, token=self._token))

    def clone_recommendation_job(self, parent_id):
            return self._federated_learning_stub.CloneRecommendationJob(federated_learning_pb2.CloneRecommendationJobRequest(parent_id=parent_id, token=self._token))

    def read_count_by_owner_sum(self):
            return self._federated_learning_stub.ReadCountByOwnerSum(federated_learning_pb2.ReadCountByOwnerSumRequest(token=self._token))

    def read_count_by_owner_source(self, source_id):
            return self._federated_learning_stub.ReadCountByOwnerSource(federated_learning_pb2.ReadCountByOwnerSourceRequest(source_id=source_id, token=self._token))

    def read_count_by_user(self):
            return self._federated_learning_stub.ReadCountByUser(federated_learning_pb2.ReadCountByUserRequest(token=self._token))
