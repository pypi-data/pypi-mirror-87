## ca


```python
docker.swarm.ca()
```


Not yet implemented


----

## init


```python
docker.swarm.init(
    advertise_address=None,
    autolock=False,
    availability="active",
    data_path_address=None,
    data_path_port=None,
    listen_address=None,
)
```


Initialize a Swarm.

If you need the token to join the new swarm from another node,
use the [`docker.swarm.join_token`](#join_token) function.

A example of how to initialize the whole swarm without leaving the manager
if the manager has ssh access to the workers:
```python
from python_on_whales import docker, DockerClient

worker_docker = DockerClient(host="ssh://worker_linux_user@worker_hostname")
# Here the docker variable is connected to the local daemon
# worker_docker is a connected to the Docker daemon of the
# worker through ssh, useful to control it without login to the machine
# manually.
docker.swarm.init()
my_token = docker.swarm.join_token("worker")  # you can set manager too
worker_docker.swarm.join("manager_hostname:2377", token=my_token)
```

__Arguments__

- __advertise_address__ `Optional[str]`: Advertised address (format: `<ip|interface>[:port]`)
- __autolock__ `bool`: Enable manager autolocking (requiring an unlock key to start a
    stopped manager)
- __availability__ `str`: Availability of the node ("active"|"pause"|"drain")
- __data_path_address__ `Optional[str]`: Address or interface to use for data path
    traffic (format is `<ip|interface>`)


----

## join


```python
docker.swarm.join(
    manager_address,
    advertise_address=None,
    availability="active",
    data_path_address=None,
    listen_address=None,
    token=None,
)
```


Joins a swarm

__Arguments__

- __manager_address__ `str`: The address of the swarm manager in the format `"{ip}:{port}"`
- __advertise_address__ `Optional[str]`: Advertised address (format: <ip|interface>[:port])
- __availability__ `str`: Availability of the node
    (`"active"`|`"pause"`|`"drain"`)
- __data_path_address__ `Optional[str]`: Address or interface to use for data
    path traffic (format: <ip|interface>)
- __listen-address__: Listen address (format: <ip|interface>[:port])
    (default 0.0.0.0:2377)
- __token__ `Optional[str]`: Token for entry into the swarm, will determine if
    the node enters the swarm as a manager or a worker.


----

## join_token


```python
docker.swarm.join_token(node_type, rotate=False)
```


Obtains a token to join the swarm

This token can then be used
with `docker.swarm.join("manager:2377", token=my_token)`.

__Arguments__

- __node_type__ `str`: `"manager"` or `"worker"`
- __rotate__ `bool`: Rotate join token


----

## leave


```python
docker.swarm.leave(force=False)
```


Leave the swarm

__Arguments__

- __force__ `bool`: Force this node to leave the swarm, ignoring warnings


----

## unlock


```python
docker.swarm.unlock()
```


Not yet implemented


----

## unlock_key


```python
docker.swarm.unlock_key()
```


Not yet implemented


----

## update


```python
docker.swarm.update()
```


Not yet implemented


----

