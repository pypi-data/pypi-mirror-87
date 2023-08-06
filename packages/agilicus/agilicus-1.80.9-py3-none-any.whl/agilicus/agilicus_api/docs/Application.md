# Application

Application's properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **datetime** | Creation time | [optional] [readonly] 
**id** | **str** | application service id | [optional] [readonly] 
**name** | **str** | application name | 
**description** | **str** | Application description text | [optional] 
**category** | **str** | application category | 
**image** | **str** | image registry path and name | [optional] 
**image_username** | **str** | registry username | [optional] 
**image_password** | **str** | registry password | [optional] 
**image_credentials_type** | **str** | type of credentials for image | [optional] 
**environments** | [**list[Environment]**](Environment.md) | List of environments | [optional] 
**org_id** | **str** | organisation id | 
**contact_email** | **str** | Administrator contact email | [optional] 
**monitoring_config** | [**ApplicationMonitoringConfig**](ApplicationMonitoringConfig.md) |  | [optional] 
**port** | **int** | The transport layer port the application listens on for requests. E.g. if the application listens for HTTP requests on the standard port, port 80, set this to 80.  | [optional] 
**healthcheck_uri** | **str** | health check URI | [optional] 
**roles** | [**RoleList**](RoleList.md) |  | [optional] 
**definitions** | [**list[Definition]**](Definition.md) | List of definitions | [optional] 
**assignments** | [**list[ApplicationAssignment]**](ApplicationAssignment.md) | Controls the Organisations which have access to Environments of this Application.  | [optional] 
**owned** | **bool** | Whether this Application is owned by the provided organisation.  | [optional] 
**maintained** | **bool** | Whether this Application has an Environment maintained by the provided organisation.  | [optional] 
**assigned** | **bool** | Whether an Environment is assigned to this Application.  | [optional] 
**published** | **str** | Whether or not this Application is published, and if so, how. An application that has been published somewhere will have high level details about it visible (through apis intended to expose published applications), such as its name and description. The enum values mean the following:  - no: This application is not published. It will only be visibile to users with       permission to access the application, or to administrators.  - public: This application is published to the public catalogue. Any user who       can request access to the organisation will see high level details about this       application.  | [optional] [default to 'no']
**default_role_id** | **str** | The id of the default role to use for this application. This role will be assigned to users granted access to this application by default, unless overridden. This value must point to a valid Role for this application. A string of length 0 will clear out the default role. | [optional] 
**default_role_name** | **str** | The name of the default role. Does not change which role is used. Provided for convenience.  | [optional] [readonly] 
**icon_url** | **str** | A url pointing to an icon representing this application.  | [optional] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**location** | **str** | Where the application runs. Applications can run within an Agilicus hosting platform, or elsewhere on the internet. The possible values have the following meanings:   - &#x60;hosted&#x60;: the application runs on the Agilicus hosting platform.   - &#x60;external&#x60;: the application runs elsewhere on the internet. External applications     will not create instances in the Agilicus hosting platform. However, they will     be able to use Agilicus for Identity and Authentication.  | [optional] 
**service_account_id** | **str** | Service account user id GUID used to deploy the application | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


