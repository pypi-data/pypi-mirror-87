import os
import pathlib

from azure.identity import CertificateCredential, ClientSecretCredential

from src.microsoft.marketplace.saas import SaaSAPI
from src.microsoft.marketplace.saas.models import SubscriptionStatusEnum
from src.microsoft.tests.common import get_client_secret_credential


def test_get_subscriptions():
    saas = SaaSAPI(get_client_secret_credential())
    subscription_found = False
    subscriptions = saas.fulfillment_operations.list_subscriptions()

    for sub in subscriptions:
        if sub.saas_subscription_status == SubscriptionStatusEnum.SUBSCRIBED:
            subscription_found = True

    assert subscription_found


def test_client_certificate_auth():
    current_path = pathlib.Path(__file__).parent.absolute()
    tenant_id = os.environ["AAD_TENANT_ID"]
    client_id = os.environ["AAD_APP_CLIENT_ID"]
    certificate_relative_path = pathlib.Path(os.environ["AAD_CERTIFICATE_PATH"])
    certificate_path = current_path.joinpath(certificate_relative_path)
    cert_secret = os.environ["AAD_APP_CERT_SECRET"]
    cred = CertificateCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        certificate_path=certificate_path,
        password=cert_secret
    )

    saas = SaaSAPI(cred)
    subscription_found = False
    subscriptions = saas.fulfillment_operations.list_subscriptions()

    for sub in subscriptions:
        if sub.saas_subscription_status == SubscriptionStatusEnum.SUBSCRIBED:
            subscription_found = True

    assert subscription_found


