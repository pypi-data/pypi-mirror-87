# Audit

An audit record containing information about a single action performed in the system.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The id of the user performing the action | [optional] [readonly] 
**target_resource_type** | **str** | The name of the resource type which was affected by the event which generated this record. The &#x60;target_id&#x60; field will uniquely identify, if possible, the record within the resource type.  | [optional] [readonly] 
**api_name** | **str** | The name of the API which generated the event. This will typically be a single value for many different target_resource_types.  | [optional] [readonly] 
**org_id** | **str** | The organization of the user performing the action | [optional] [readonly] 
**time** | **datetime** | the time at which the log was generated | [optional] [readonly] 
**action** | **str** | The type of action performed on the target | [optional] 
**source_ip** | **str** | The IP address of the host initating the action | [optional] [readonly] 
**target_id** | **str** | The id of the resource affected by the action | [optional] [readonly] 
**token_id** | **str** | The id of the bearer token used to authenticate when performing the action | [optional] [readonly] 
**trace_id** | **str** | A correlation ID associated with requests related to this action | [optional] [readonly] 
**session** | **str** | The session associated with this action. Sessions typically span multiple tokens.  | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


