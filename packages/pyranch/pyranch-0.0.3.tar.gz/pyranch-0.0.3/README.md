# WIP

# Rancher API
Python wrapper for Rancher API

# Usage
## Connecting to Environment
```python
import pyranch
rancher = pyranch.Environment(<RANCHER_URL>, <RANCHER_ACCESS_KEY>, <RANCHER_SECRET_KEY>, project_id=<ENVIRONMENT_ID>)
```
Additional parameters:
- port - Rancher API port, default ```80```
- api_version - Rancher API version, default ```v2-beta```

## Working on Environment
* activate
* deactivate
* upgrade
* set_members **#TODO**
More information can be found [here](http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/project)

## Working on Stack
#### Stack fields

| Field | Type | Required | Can update | Default |
|---|---|---|---|---|
| binding | dict | No | **Yes** | ```{}``` |
| description |	str |No | **Yes** |	```None``` |
| dockerCompose	| str | No | No | ``` ``` |
| environment | dict | No | No | ```{}``` | 
| externalId | str | No | **Yes** | ```None``` |
| group | str | No | **Yes** | ```None``` |
| name | str | **Yes** | **Yes** |
| outputs | dict | No | **Yes** | ```{}``` |
| previousEnvironment | dict | No | **Yes** | ```{}``` |
| previousExternalId | str | No | **Yes** | ```None``` |
| rancherCompose | str | No | No | ``` ``` |
| startOnCreate | bool | No | No | ```False``` |
| **Read only values** |
| **Field** | **Type** |
| id | str |
| healthState | str |
| serviceIds | list |
| system | bool |

#### Initialize stack object
```python
cows = rancher.stack(stack_name='cows')
```
*Note: Existing stacks can be initialized using ```stack_id```*

#### Create Stack in rancher
```python
cows.description = 'Stack of cows'
cows.create()
```

#### Print Stack data
```python
cows()
```
#### Update Stack
```python
cows.name = "bulls"
cows.description = "Stack of bulls"
cows.save()
```

#### Stack actions
More actions can be found [here](http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/stack/)

## Working on Service
#### Service fields

| Field | Type | Required | Can update | Default |
|---|---|---|---|---|
| assignServiceIpAddress | bool | No | No | ```False``` |
| description |	str | No | **Yes** | ```None``` |
| externalId | str | No | No | ```None``` |
| launchConfig | dict | No | No | ```{}``` |
| lbConfig | dict | No | **Yes** | ```{}``` |
| metadata | dict | No | **Yes** | ```{}``` |
| name | str | **Yes** | **Yes** |
| retainIp | bool | No | **Yes** | ```False``` |
| scale | int | No | **Yes** | ```1``` |
| scalePolicy | dict | No | **Yes** | ```{}``` |
| secondaryLaunchConfigs | list | No | No | ```[]``` |
| selectorContainer | str | No | **Yes** | ```None``` |
| selectorLink | str | No | **Yes** | ```None``` |
| stackId | dict | No | No | ```{}``` |
| startOnCreate | bool | No | No | ```False``` |
| vip | str | No | No | ```None```|
| **Read only values** |
| **Field** | **Type** |
| id | str |
| healthState | str |
| system | bool |
| instanceIds | list |
| createIndex | int |
| currentScale | int |
| fqdn | str |
| linkedServices | dict |
| publicEndpoints | list |
| upgrade | dict |

#### Initialize Service object
```python
cow = rancher.service(stack_name='cows')
```
*Note: Existing service can be initialized using ```service_id```*

#### Create Service in rancher
```python
cow.description = 'Our Cow'
cow.create()
```

### Print service data
```python
cow()
```
#### Update service
```python
cow.name = 'bull'
cow.description = "Our bull"
cow.save()
```
#### Scale service
```python
cow.scale_out(1)
cow.scale_in(1)
```

#### Service Log
```python
cow.logs()['data']
```

#### Service actions
More actions can be found [here](http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/service/)

