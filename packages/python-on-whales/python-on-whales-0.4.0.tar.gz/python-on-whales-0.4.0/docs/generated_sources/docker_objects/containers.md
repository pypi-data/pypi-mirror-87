# Containers

Don't use the constructor directly. Instead use 
```python
from python_on_whales import docker

my_container = docker.container.inspect("my-container-name")

# for example:
if my_container.state.running:
    my_container.kill()

```
For type hints, use this

```python
from python_on_whales import Container

def print_dodo(container: Container):
    print(container.execute(["echo", "dodo"]))
```

## Attributes

It attributes are the same that you get with the command line:
`docker container inspect ...`

An example is worth many lines of descriptions.


```
In [1]: from python_on_whales import docker

In [2]: container = docker.run("ubuntu", ["sleep", "infinity"], detach=True)

In [4]: def super_print(obj):
   ...:     print(f"type={type(obj)}, value={obj}")
   ...:

In [5]: super_print(container.id)
type=<class 'str'>, value=1fb602d9292492846a395c7d7c8400a796c6b49eecdf83ae38875feb08728071

In [6]: super_print(container.created)
type=<class 'datetime.datetime'>, value=2020-10-24 13:49:55.050922+00:00

In [7]: super_print(container.image)
type=<class 'python_on_whales.Image'>, value=sha256:9140108b62dc87d9b278bb0d4fd6a3e44c2959646eb966b86531306faa81b09b

In [8]: super_print(container.name)
type=<class 'str'>, value=charming_burnell

In [9]: super_print(container.state.status)
type=<class 'str'>, value=running

In [10]: super_print(container.state.running)
type=<class 'bool'>, value=True

In [11]: super_print(container.state.paused)
type=<class 'bool'>, value=False

In [12]: super_print(container.state.restarting)
type=<class 'bool'>, value=False

In [13]: super_print(container.state.OOM_killed)
type=<class 'bool'>, value=False

In [14]: super_print(container.state.dead)
type=<class 'bool'>, value=False

In [15]: super_print(container.state.pid)
type=<class 'int'>, value=5565

In [16]: super_print(container.state.exit_code)
type=<class 'int'>, value=0

In [17]: super_print(container.state.error)
type=<class 'str'>, value=

In [18]: super_print(container.state.started_at)
type=<class 'datetime.datetime'>, value=2020-10-24 13:49:55.325651+00:00

In [19]: super_print(container.state.finished_at)
type=<class 'datetime.datetime'>, value=0001-01-01 00:00:00+00:00

In [20]: super_print(container.host_config.auto_remove)
type=<class 'bool'>, value=False

In [21]: super_print(container.config.hostname)
type=<class 'str'>, value=1fb602d92924

In [22]: super_print(container.config.domainname)
type=<class 'str'>, value=

In [23]: super_print(container.config.attach_stdin)
type=<class 'bool'>, value=False

In [24]: super_print(container.config.attach_stdout)
type=<class 'bool'>, value=False

In [25]: super_print(container.config.attach_stderr)
type=<class 'bool'>, value=False

In [26]: super_print(container.config.tty)
type=<class 'bool'>, value=False

In [27]: super_print(container.config.open_stdin)
type=<class 'bool'>, value=False

In [28]: super_print(container.config.stdin_once)
type=<class 'bool'>, value=False

In [29]: super_print(container.config.env)
type=<class 'list'>, value=['PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin']

In [30]: super_print(container.config.cmd)
type=<class 'list'>, value=['sleep', 'infinity']

In [31]: super_print(container.config.image)
type=<class 'str'>, value=ubuntu

In [32]: super_print(container.config.labels)
type=<class 'dict'>, value={}

```

## Methods

## commit


```python
Container.commit(tag=None, author=None, message=None, pause=True)
```


Create a new image from the container's changes.

Alias: `docker.commit(...)`

See the [`docker.container.commit`](../sub-commands/container.md) command for
information about the arguments.


----

## copy_from


```python
Container.copy_from(container_path, local_path)
```


----

## copy_to


```python
Container.copy_to(local_path, container_path)
```


----

## diff


```python
Container.diff()
```


Returns the diff of this container filesystem.

See the [`docker.container.diff`](../sub-commands/container.md) command for
information about the arguments.


----

## execute


```python
Container.execute(command, detach=False)
```


Execute a command in this container

See the [`docker.container.execute`](../sub-commands/container.md#execute)
command for information about the arguments.


----

## export


```python
Container.export(output)
```


Export this container filesystem.

See the [`docker.container.export`](../sub-commands/container.md) command for
information about the arguments.


----

## kill


```python
Container.kill(signal=None)
```


Kill this container

See the [`docker.container.kill`](../sub-commands/container.md#kill) command for
information about the arguments.


----

## logs


```python
Container.logs(details=False, since=None, tail=None, timestamps=False, until=None)
```


Returns the logs of the container

See the [`docker.container.logs`](../sub-commands/container.md#logs) command for
information about the arguments.


----

## pause


```python
Container.pause()
```


Pause this container.

See the [`docker.container.pause`](../sub-commands/container.md#pause) command for
information about the arguments.


----

## reload


```python
Container.reload()
```


----

## remove


```python
Container.remove(force=False, volumes=False)
```


Remove this container.

See the [`docker.container.remove`](../sub-commands/container.md#remove) command for
information about the arguments.


----

## rename


```python
Container.rename(new_name)
```


Rename this container

See the [`docker.container.rename`](../sub-commands/container.md#rename) command for
information about the arguments.


----

## restart


```python
Container.restart(time=None)
```


Restarts this container.

See the [`docker.container.restart`](../sub-commands/container.md#restart) command for
information about the arguments.


----

## start


```python
Container.start(attach=False, stream=False)
```


Starts this container.

See the [`docker.container.start`](../sub-commands/container.md#start) command for
information about the arguments.


----

## stop


```python
Container.stop(time=None)
```


Stops this container.

See the [`docker.container.stop`](../sub-commands/container.md#stop) command for
information about the arguments.


----

## unpause


```python
Container.unpause()
```


Unpause the container

See the [`docker.container.unpause`](../sub-commands/container.md#unpause) command for
information about the arguments.


----


