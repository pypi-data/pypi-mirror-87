import os
import sys
import logging
from functools import wraps

from fincura import Configuration
from fincura.api_client import ApiClient
from fincura.model.api_key import ApiKey
from fincura.apis import  (
    ApiKeyApi,
    BorrowersApi,
    CustomAttributesApi,
    DataViewsApi,
    EmbeddedWorkflowsApi,
    FilesApi,
    LoansApi,
    PortfoliosApi,
    RequirementsApi,
    TenantSettingsApi,
    WebhooksApi,
)
from fincura import (
	Configuration,
    ApiKeyApi,
    BorrowersApi,
    CustomAttributesApi,
    DataViewsApi,
    EmbeddedWorkflowsApi,
    FilesApi,
    LoansApi,
    PortfoliosApi,
    RequirementsApi,
    TenantSettingsApi,
    WebhooksApi,
)
from fincura.rest import ApiException

TENANT_ID =  os.environ.get('FINCURA_TENANT_ID')
REFRESH_TOKEN = str(os.environ['FINCURA_API_REFRESH_TOKEN'])

FINCURA_ENV = os.environ['FINCURA_ENV']

if FINCURA_ENV == 'local':
	host = "https://api-local.fincura.com:8000"
elif FINCURA_ENV == 'production':
	host = "https://api.fincura.com"
else:
	host = "https://api-%s.fincura.com" % FINCURA_ENV

# Configure API key authorization: ApiKeyAuth
configuration = Configuration(host=host)
configuration.verify_ssl = FINCURA_ENV != 'local' # for debug only
configuration.client_side_validation = False
configuration.api_key['API_Key'] = None
configuration.api_key_prefix['API_Key'] = 'Bearer'

# create an instance of the API class
api_key_api = ApiKeyApi(ApiClient(configuration))
borrowers_api = BorrowersApi(ApiClient(configuration))
custom_attributes_api = CustomAttributesApi(ApiClient(configuration))
data_views_api = DataViewsApi(ApiClient(configuration))
embedded_workflows_api = EmbeddedWorkflowsApi(ApiClient(configuration))
files_api = FilesApi(ApiClient(configuration))
loans_api = LoansApi(ApiClient(configuration))
portfolios_api = PortfoliosApi(ApiClient(configuration))
requirements_api = RequirementsApi(ApiClient(configuration))
tenant_settings_api = TenantSettingsApi(ApiClient(configuration))
webhooks_api = WebhooksApi(ApiClient(configuration))

APIS = [
    "api_key_api",
    "borrowers_api",
    "custom_attributes_api",
    "data_views_api",
    "embedded_workflows_api",
    "files_api",
    "loans_api",
    "portfolios_api",
    "requirements_api",
    "tenant_settings_api",
    "webhooks_api",
]

class Clients(object):
    pass

clients = Clients()

for api_name in APIS:
    client_name = f"{api_name.rpartition('_api')[0]}_client"
    setattr(clients, client_name, locals()[api_name])


def ensure_api_access(function):
	@wraps(function)
	def wrap(request, *args, **kwargs):
		# TODO - check current access, dont refresh if still valid
	    refresh_access_token()
	    return function(request, *args, **kwargs)
	return wrap

def refresh_access_token():
	refresh_response = clients.api_key_client.refresh_api_key(
		api_key=ApiKey(refresh_token=REFRESH_TOKEN, tenant_id=TENANT_ID)
	)
	configuration.access_token = refresh_response.access_token