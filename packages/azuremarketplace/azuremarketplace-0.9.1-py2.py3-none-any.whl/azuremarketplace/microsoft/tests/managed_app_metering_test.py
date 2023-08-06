import json
import os
from datetime import datetime, timedelta
from urllib import request
from urllib.error import HTTPError

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import managedapplications
from azure.mgmt.subscription import SubscriptionClient
from msrestazure.azure_active_directory import ServicePrincipalCredentials

from src.microsoft.marketplace.meter import MeteringAPI
from src.microsoft.marketplace.meter.models import UsageEvent


def handle_usage_event_response(response, data, other):
    print(response)
    print(data)

    # data will be the usageOK event and needs to also be returned to the original caller.
    return data


def test_metering():
    tenant_id = os.environ["AAD_TENANT_ID"]
    client_id = os.environ["AAD_MGD_APP_CLIENT_ID"]
    client_secret = os.environ["AAD_MGD_APP_CLIENT_SECRET"]
    cred = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)
    subscription_client = SubscriptionClient(cred)

    subs = subscription_client.subscriptions.list()

    managed_app_credential = ClientSecretCredential(
        client_id=client_id,                                                         v
        client_secret=client_secret,
        tenant_id=tenant_id)

    billing_credential = ClientSecretCredential(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id)

    metering = MeteringAPI(billing_credential)
    access_token = cred.token['access_token']
    for sub in subs:
        managed_app_client = managedapplications.ApplicationClient(credential=managed_app_credential,
                                                                   subscription_id=sub.subscription_id)
        apps = managed_app_client.applications.list_by_subscription()

        for app in apps:
            # At this point, we need to construct a raw URL to get the billing ID if one exists
            # This could be detected by the Offer ID (app.plan.product) and Plan ID (app.plan.name)
            if app.plan.product != "scs-managed-app-saas-portal" and app.plan.name != "billing-full-control":
                continue

            timestamp = (datetime.now() - timedelta(minutes=1)).isoformat()

            usage_event = UsageEvent(
                resource_uri=app.id,
                quantity=13,
                dimension='dim1',
                effective_start_time=timestamp,
                plan_id=app.plan.name
            )

            # Make sure your cls implementation returns the second parameter so that the result also appears
            # here. Otherwise, resp will always be None.
            resp = metering.metering_operations.post_usage_event(body=usage_event, cls=handle_usage_event_response)
            if resp is None:
                continue
            print(resp.status)

