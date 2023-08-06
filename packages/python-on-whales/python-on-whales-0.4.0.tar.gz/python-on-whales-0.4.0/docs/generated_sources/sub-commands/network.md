## connect


```python
docker.network.connect(network, container, alias=None, driver_options=[], ip=None, ip6=None, links=[])
```


----

## create


```python
docker.network.create(name, attachable=False, driver=None, gateway=None, subnet=None, options=[])
```


Creates a Docker network.

__Arguments__

- __name__ `str`: The name of the network

__Returns__

A `python_on_whales.Network`.


----

## disconnect


```python
docker.network.disconnect(network, container, force=False)
```


----

## inspect


```python
docker.network.inspect(x)
```


----

## list


```python
docker.network.list(filters={})
```


----

## prune


```python
docker.network.prune(filters={})
```


----

## remove


```python
docker.network.remove(networks)
```


Removes a Docker network

__Arguments__

- __networks__ `Union[python_on_whales.Network, str, List[Union[python_on_whales.Network, str]]]`: One or more networks.


----

