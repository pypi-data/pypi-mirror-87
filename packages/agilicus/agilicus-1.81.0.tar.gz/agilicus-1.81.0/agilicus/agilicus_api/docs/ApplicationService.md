# ApplicationService

Application service's properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **datetime** | Creation time | [optional] [readonly] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**name** | **str** | The name of the service. Services will be selected and assigned using this. This value must be unique within an organisation.  | 
**org_id** | **str** | The organisation which owns this service. | 
**hostname** | **str** | The hostname of the service. Your applications will refer to this service using its hostname.  | 
**ipv4_addresses** | **list[str]** | The IPv4 addresses of &#x60;hostname&#x60; within the data center. | [optional] 
**name_resolution** | **str** | How to resolve the hostname of the service. If static, then ipv4_address will be used. Otherwise, if dns the Organisation&#39;s dns services will be queried.  | [optional] [default to 'static']
**port** | **int** | The transport-layer port on which to access the service. exclusiveMinimum: 0 exclusiveMaximum: 65536  | 
**protocol** | **str** | The transport-layer protocol over which to communicate with the service.  | [optional] [default to 'tcp']
**assignments** | [**list[ApplicationServiceAssignment]**](ApplicationServiceAssignment.md) | The Application Environments which have access to this ApplicationService. Manipulate this list to add or remove access to the ApplicationService.  | [optional] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**service_type** | **str** | The type of application service. This refers to how the application connects to the service | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


