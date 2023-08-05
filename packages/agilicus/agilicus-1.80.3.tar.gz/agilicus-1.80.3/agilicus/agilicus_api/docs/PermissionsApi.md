# agilicus_api.PermissionsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_elevated_user_roles**](PermissionsApi.md#get_elevated_user_roles) | **GET** /v1/elevated_permissions/{user_id} | Get elevated roles for a user
[**list_elevated_user_roles**](PermissionsApi.md#list_elevated_user_roles) | **GET** /v1/elevated_permissions | List all elevated users and their roles
[**replace_elevated_user_role**](PermissionsApi.md#replace_elevated_user_role) | **PUT** /v1/elevated_permissions/{user_id} | Create or update an elevated user role


# **get_elevated_user_roles**
> UserRoles get_elevated_user_roles(user_id)

Get elevated roles for a user

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.PermissionsApi(api_client)
    user_id = '1234' # str | user_id path

    try:
        # Get elevated roles for a user
        api_response = api_instance.get_elevated_user_roles(user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PermissionsApi->get_elevated_user_roles: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 

### Return type

[**UserRoles**](UserRoles.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return elevated user roles |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_elevated_user_roles**
> ListElevatedUserRoles list_elevated_user_roles(limit=limit, user_id=user_id)

List all elevated users and their roles

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.PermissionsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)

    try:
        # List all elevated users and their roles
        api_response = api_instance.list_elevated_user_roles(limit=limit, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PermissionsApi->list_elevated_user_roles: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**ListElevatedUserRoles**](ListElevatedUserRoles.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User role updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_elevated_user_role**
> replace_elevated_user_role(user_id, replace_user_role_request=replace_user_role_request)

Create or update an elevated user role

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.PermissionsApi(api_client)
    user_id = '1234' # str | user_id path
replace_user_role_request = agilicus_api.ReplaceUserRoleRequest() # ReplaceUserRoleRequest |  (optional)

    try:
        # Create or update an elevated user role
        api_instance.replace_elevated_user_role(user_id, replace_user_role_request=replace_user_role_request)
    except ApiException as e:
        print("Exception when calling PermissionsApi->replace_elevated_user_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **replace_user_role_request** | [**ReplaceUserRoleRequest**](ReplaceUserRoleRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User role updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

