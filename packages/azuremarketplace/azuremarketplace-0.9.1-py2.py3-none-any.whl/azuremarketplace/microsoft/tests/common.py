import os

from azure.identity import ClientSecretCredential


def get_client_secret_credential():
    tenant_id = os.environ["AAD_TENANT_ID"]
    client_id = os.environ["AAD_APP_CLIENT_ID"]
    client_secret = os.environ["AAD_APP_CLIENT_SECRET"]

    cred = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    return cred
