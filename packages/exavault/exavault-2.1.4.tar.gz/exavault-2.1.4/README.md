# ExaVault Python API Library - v2 API

Welcome to ExaVault's Python code library for our v2 API. Use our API to interact with all aspects of the service the same way our web portal would. The library is generated from our API's [public swagger YAML file](https://www.exavault.com/api/docs/evapi_2.0_public.yaml).

## Requirements 

The SDK supports the following versions of Python:

-  Python 2 versions 2.7.9 and later
-  Python 3 versions 3.4 and later

You will also need an ExaVault account, as well as an API key and access token.

## Installing the Code Library

### Option 1 - Using PIP
You can use pip to add this library to your project by running this command in your project folder:

```bash
% pip install exavault
```

### Option 2 - Manual Installation
Alternatively, you can:

1. Clone the repo `git clone https://github.com/ExaVault/evapi-python.git evapi-python` or manually download the library.
2. Run setup script `python setup.py install` Depending on your python setup, you may need to run the script as root; e.g. `sudo python setup.py install`

## Sample Code

For a gentle introduction to using Python code with ExaVault's API, check out [our code samples](https://github.com/ExaVault/evapi-python-samples). Follow the instructions in that repository's README to run the sample scripts, which will demonstrate how to use several of the APIs to interact with your ExaVault account.

## Writing Your Own Code

When you're ready to write your own code using this library, you'll need to:

1. Install our code library in your project, either with `pip install exavault` or by downloading this repository and importing the package directly
1. Provide your API key and access token with every function method on the Api classes
1. Whenever you instantiate an Api object (ResourcesApi, UsersApi, etc.), override the configuration to point the code at the correct API URL:
```python
from exavault import AccountApi
ACCOUNT_URL = "https://YOUR_ACCOUNT_NAME_HERE.exavault.com/api/v2/";
account_api = AccountApi()
account_api.api_client.configuration.host = ACCOUNT_URL
```
```python
from exavault import ResourcesApi
ACCOUNT_URL = "https://YOUR_ACCOUNT_NAME_HERE.exavault.com/api/v2/";
resources_api = ResourcesApi()
resources_api.api_client.configuration.host = ACCOUNT_URL
```
```python
from exavault import NotificationsApi
ACCOUNT_URL = "https://YOUR_ACCOUNT_NAME_HERE.exavault.com/api/v2/";
notifications_api = NotificationsApi()
notifications_api.api_client.configuration.host = ACCOUNT_URL
```

If you'd like to see this done in sample code, please take a look at [our code samples](https://github.com/ExaVault/evapi-python-samples).

## Author

support@exavault.com
