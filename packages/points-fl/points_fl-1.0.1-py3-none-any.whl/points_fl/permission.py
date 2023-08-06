from points_fl.base import Base
from points_fl.proto import permission_pb2


class Permission(Base):

    def create_organization(self, organization_name):
            return self._permission_stub.CreateOrganization(permission_pb2.CreateOrganizationRequest(organization_name=organization_name, token=self._token))

    def read_organization(self, organization_id):
            return self._permission_stub.ReadOrganization(permission_pb2.ReadOrganizationRequest(organization_id=organization_id, token=self._token))

    def read_organization_list(self, organization_id, organization_name):
            return self._permission_stub.ReadOrganizationList(permission_pb2.ReadOrganizationListRequest(organization_id=organization_id, organization_name=organization_name, token=self._token))

    def update_organization(self, organization_id, new_organization_name):
            return self._permission_stub.UpdateOrganization(permission_pb2.UpdateOrganizationRequest(organization_id=organization_id, new_organization_name=new_organization_name, token=self._token))

    def delete_organization(self, organization_id):
            return self._permission_stub.DeleteOrganization(permission_pb2.DeleteOrganizationRequest(organization_id=organization_id, token=self._token))

    def create_account(self, username, password, organization_id):
            return self._permission_stub.CreateAccount(permission_pb2.CreateAccountRequest(username=username, password=password, organization_id=organization_id, token=self._token))

    def create_self_account(self, username, password, role):
            return self._permission_stub.CreateSelfAccount(permission_pb2.CreateSelfAccountRequest(username=username, password=password, role=role, token=self._token))

    def read_account(self, account_id):
            return self._permission_stub.ReadAccount(permission_pb2.ReadAccountRequest(account_id=account_id, token=self._token))

    def read_account_list(self, organization_id):
            return self._permission_stub.ReadAccountList(permission_pb2.ReadAccountListRequest(organization_id=organization_id, token=self._token))

    def read_self_account(self):
            return self._permission_stub.ReadSelfAccount(permission_pb2.ReadSelfAccountRequest(token=self._token))

    def update_account(self, account_id, new_password):
            return self._permission_stub.UpdateAccount(permission_pb2.UpdateAccountRequest(account_id=account_id, new_password=new_password, token=self._token))

    def update_self_account(self, new_password):
            return self._permission_stub.UpdateSelfAccount(permission_pb2.UpdateSelfAccountRequest(new_password=new_password, token=self._token))

    def delete_account(self, account_id):
            return self._permission_stub.DeleteAccount(permission_pb2.DeleteAccountRequest(account_id=account_id, token=self._token))

    def read_self_account_list(self):
            return self._permission_stub.ReadSelfAccountList(permission_pb2.ReadSelfAccountListRequest(token=self._token))

    def create_authorized(self, organization_id, organization_name):
            return self._permission_stub.CreateAuthorized(permission_pb2.CreateAuthorizedRequest(organization_id=organization_id, organization_name=organization_name, token=self._token))

    def read_authorizing_list(self):
            return self._permission_stub.ReadAuthorizingList(permission_pb2.ReadAuthorizingListRequest(token=self._token))

    def read_authorized_list(self):
            return self._permission_stub.ReadAuthorizedList(permission_pb2.ReadAuthorizedListRequest(token=self._token))

    def delete_authorized(self, organization_id):
            return self._permission_stub.DeleteAuthorized(permission_pb2.DeleteAuthorizedRequest(organization_id=organization_id, token=self._token))
