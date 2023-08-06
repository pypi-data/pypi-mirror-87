import hvac
from nameko.extensions import DependencyProvider


class VaultProvider(DependencyProvider):
    def __init__(self, mount_point=None):
        self.mount_point = mount_point

    def setup(self):
        url = self.container.config.get("VAULT_URL", "")
        self.client = hvac.Client(url=url)
        if self.client.is_authenticated() is False:
            self.client.token = self.container.config.get("VAULT_TOKEN", "")

    def get_connection(self):
        return self.client

    def get_dependency(self, worker_ctx):
        return self

    def get_kv_secret(self, path, mount_point=None):
        mount_point = mount_point if mount_point else self.mount_point
        secret = self.client.secrets.kv.read_secret_version(
            mount_point=mount_point, path=path
        )

        return secret["data"]

    def get_kv_secrets_list(self, path, mount_point=None):
        mount_point = mount_point if mount_point else self.mount_point
        secret = self.client.secrets.kv.list_secrets(
            path=path, mount_point=mount_point
        )
        path = path if path.endswith("/") else path + "/"

        return [path + key for key in secret["data"]["keys"]]

    def create_or_update_kv_secret(self, path, secret, mount_point=None):
        mount_point = mount_point if mount_point else self.mount_point

        response = self.client.secrets.kv.v2.create_or_update_secret(
            mount_point=mount_point,
            path=path,
            secret=secret,
        )
        return response

    def patch_kv_secret(self, path, secret, mount_point=None):
        mount_point = mount_point if mount_point else self.mount_point

        response = self.client.secrets.kv.v2.patch(
            mount_point=mount_point,
            path=path,
            secret=secret,
        )
        return response

    def delete_metadata_and_all_versions_kv_secret(
        self, path, mount_point=None
    ):
        mount_point = mount_point if mount_point else self.mount_point

        response = self.client.secrets.kv.v2.delete_metadata_and_all_versions(
            mount_point=mount_point,
            path=path,
        )
        return response.status_code
