## create


```python
docker.service.create(image, command)
```


Creates a Docker swarm service.

Consider using 'docker stack deploy' instead as it's idempotent and
easier to read for complex applications.
docker stack deploy is basically docker compose for swarm clusters.

__Arguments:__

image: The image to use as the base for the service.
command: The command to execute in the container(s).


----

## inspect


```python
docker.service.inspect(x)
```


Returns one or a list of `python_on_whales.Service` object(s).


----

## list


```python
docker.service.list()
```


Returns the list of services

__Returns__

A `List[python_on_whales.Services]`


----

## logs


```python
docker.service.logs()
```


Not yet implemented


----

## ps


```python
docker.service.ps()
```


Not yet implemented


----

## remove


```python
docker.service.remove(services)
```


Removes a service

__Arguments__

- __services__ `Union[str, python_on_whales.Service, List[Union[str, python_on_whales.Service]]]`: One or a list of services to remove.


----

## rollback


```python
docker.service.rollback()
```


Not yet implemented


----

## scale


```python
docker.service.scale(new_scales, detach=False)
```


Scale one or more services.

__Arguments__

- __new_scales__ `Dict[Union[str, python_on_whales.Service], int]`: Mapping between services and the desired scales. For example
    you can provide `new_scale={"service1": 4, "service2": 8}`
- __detach__: If True, does not wait for the services to converge and return
    immediately.


----

## update


```python
docker.service.update(service, detach=False, force=False, image=None, with_registry_authentication=False)
```


Update a service


----

