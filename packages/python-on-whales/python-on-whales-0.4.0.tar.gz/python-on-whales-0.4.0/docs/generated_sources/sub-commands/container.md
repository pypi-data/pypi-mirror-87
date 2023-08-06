## attach


```python
docker.container.attach()
```


Not yet implemented


----

## commit


```python
docker.container.commit(container, tag=None, author=None, message=None, pause=True)
```


Create a new image from a container's changes

__Arguments__

- __container__ `Union[python_on_whales.Container, str]`: The container to create the image from
- __tag__ `Optional[str]`: tag to apply on the image produced
- __author__ `Optional[str]`: Author (e.g., "John Hannibal Smith <hannibal@a-team.com>")
- __message__ `Optional[str]`: Commit message
- __pause__ `bool`: Pause container during commit


----

## copy


```python
docker.container.copy(source, destination)
```


Copy files/folders between a container and the local filesystem

Alias: `docker.copy(...)`

```python
from python_on_whales import docker

docker.run("ubuntu", ["sleep", "infinity"], name="dodo", remove=True, detach=True)

docker.copy("/tmp/my_local_file.txt", ("dodo", "/path/in/container.txt"))
docker.copy(("dodo", "/path/in/container.txt"), "/tmp/my_local_file2.txt")
```

Doesn't yet support sending or receiving iterators of Python bytes.

__Arguments__

- __source__ `Union[str, pathlib.Path, Tuple[Union[python_on_whales.Container, str], Union[str, pathlib.Path]]]`: Local path or tuple. When using a tuple, the first element
    of the tuple is the container, the second element is the path in
    the container. ex: `source=("my-container", "/usr/bin/something")`.
- __destination__ `Union[str, pathlib.Path, Tuple[Union[python_on_whales.Container, str], Union[str, pathlib.Path]]]`: Local path or tuple. When using a tuple, the first element
    of the tuple is the container, the second element is the path in
    the container. ex: `source=("my-container", "/usr/bin/something")`.


----

## create


```python
docker.container.create(
    image,
    command=[],
    *,
    add_hosts=[],
    blkio_weight=None,
    blkio_weight_device=[],
    cap_add=[],
    cap_drop=[],
    cgroup_parent=None,
    cidfile=None,
    cpu_period=None,
    cpu_quota=None,
    cpu_rt_period=None,
    cpu_rt_runtime=None,
    cpu_shares=None,
    cpus=None,
    cpuset_cpus=None,
    cpuset_mems=None,
    detach=False,
    devices=[],
    device_cgroup_rules=[],
    device_read_bps=[],
    device_read_iops=[],
    device_write_bps=[],
    device_write_iops=[],
    content_trust=False,
    dns=[],
    dns_options=[],
    dns_search=[],
    domainname=None,
    entrypoint=None,
    envs={},
    env_files=[],
    expose=[],
    gpus=None,
    groups_add=[],
    healthcheck=True,
    health_cmd=None,
    health_interval=None,
    health_retries=None,
    health_start_period=None,
    health_timeout=None,
    hostname=None,
    init=False,
    ip=None,
    ip6=None,
    ipc=None,
    isolation=None,
    kernel_memory=None,
    labels={},
    label_files=[],
    link=[],
    link_local_ip=[],
    log_driver=None,
    log_options=[],
    mac_address=None,
    memory=None,
    memory_reservation=None,
    memory_swap=None,
    memory_swappiness=None,
    mounts=[],
    name=None,
    networks=[],
    network_aliases=[],
    oom_kill=True,
    oom_score_adj=None,
    pid=None,
    pids_limit=None,
    platform=None,
    privileged=False,
    publish=[],
    publish_all=False,
    read_only=False,
    restart=None,
    remove=False,
    runtime=None,
    security_options=[],
    shm_size=None,
    sig_proxy=True,
    stop_signal=None,
    stop_timeout=None,
    storage_options=[],
    sysctl={},
    tmpfs=[],
    ulimit=[],
    user=None,
    userns=None,
    uts=None,
    volumes=[],
    volume_driver=None,
    volumes_from=[],
    workdir=None
)
```


Creates a container, but does not start it.

Alias: `docker.create(...)`

Start it then with the `.start()` method.

It might be useful if you want to delay the start of a container,
to do some preparations beforehand. For example, it's common to do this
workflow: `docker create` -> `docker cp` -> `docker start` to put files
in the container before starting.

There is no `detach` argument since it's a runtime option.

The arguments are the same as [`docker.run`](#run).


----

## diff


```python
docker.container.diff(container)
```


List all the files modified, added or deleted since the container started.

Alias: `docker.diff(...)`

__Arguments__

- __container__ `Union[python_on_whales.Container, str]`: The container to inspect

__Returns__

`Dict[str, str]` Something like
`{"/some_path": "A", "/some_file": "M", "/tmp": "D"}` for example.


----

## execute


```python
docker.container.execute(container, command, detach=False)
```


Execute a command inside a container

Alias: `docker.execute(...)`

__Arguments__

- __container__ `Union[python_on_whales.Container, str]`: The container to execute the command in.
- __command__ `Union[str, List[str]]`: The command to execute.
- __detach__ `bool`: if `True`, returns immediately with `None`. If `False`,
    returns the command stdout as string.

__Returns:__

Optional[str]


----

## export


```python
docker.container.export(container, output)
```


Export a container's filesystem as a tar archive

Alias: `docker.export(...)`

__Arguments__

- __container__ `Union[python_on_whales.Container, str]`: The container to export.
- __output__ `Union[str, pathlib.Path]`: The path of the output tar archive.


----

## inspect


```python
docker.container.inspect(x)
```


Returns a container object from a name or ID.

__Arguments__

- __reference__: A container name or ID, or a list of container names
    and/or IDs

__Returns:__

A [`python_on_whales.Container`](/docker_objects/containers/) object or a list of those
if a list of IDs was passed as input.


----

## kill


```python
docker.container.kill(containers, signal=None)
```


Kill a container.

Alias: `docker.kill(...)`

__Arguments__

- __containers__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or more containers to kill
- __signal__ `Optional[str]`: The signal to send the container


----

## list


```python
docker.container.list(all=False, filters={})
```


List the containers on the host.

Alias: `docker.ps(...)`

__Arguments__

- __all__ `bool`: If `True`, also returns containers that are not running.

__Returns__

A `List[python_on_whales.Container]`


----

## logs


```python
docker.container.logs(container, details=False, since=None, tail=None, timestamps=False, until=None)
```


Returns the logs of a container as a string.

Alias: `docker.logs(...)`

The follow option is not yet implemented.

__Arguments__

- __container__ `Union[python_on_whales.Container, str]`: The container to get the logs of
- __details__ `bool`: Show extra details provided to logs
- __since__ `Union[None, datetime.datetime, datetime.timedelta]`: Use a datetime or timedelta to specify the lower
    date limit for the logs.
- __tail__ `Optional[int]`: Number of lines to show from the end of the logs (default all)
- __timestamps__ `bool`: Put timestamps next to lines.
- __until__ `Union[None, datetime.datetime, datetime.timedelta]`: Use a datetime or a timedelta to specify the upper date
    limit for the logs.

__Returns__

`str`


----

## pause


```python
docker.container.pause(containers)
```


Pauses one or more containers

Alias: `docker.pause(...)`

__Arguments__

- __containers__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or more containers to pause


----

## prune


```python
docker.container.prune(filters=[])
```


Remove containers that are not running.

__Arguments__

- __filters__ `Union[str, List[str]]`: Filters as strings or list of strings


----

## remove


```python
docker.container.remove(containers, force=False, volumes=False)
```


Removes a container

Alias: `docker.remove(...)`

__Arguments__

- __containers__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or more containers.
- __force__ `bool`: Force the removal of a running container (uses SIGKILL)
- __volumes__ `bool`: Remove anonymous volumes associated with the container


----

## rename


```python
docker.container.rename(container, new_name)
```


Changes the name of a container.

Alias: `docker.rename(...)`

__Arguments__

- __container__ `Union[python_on_whales.Container, str]`: The container to rename
- __new_name__ `str`: The new name of the container.


----

## restart


```python
docker.container.restart(containers, time=None)
```


Restarts one or more container.

Alias: `docker.restart(...)`

__Arguments__

- __containers__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or more containers to restart
- __time__ `Union[None, int, datetime.timedelta]`: Amount of to wait for stop before killing the container (default 10s).
    If `int`, the unit is seconds.


----

## run


```python
docker.container.run(
    image,
    command=[],
    *,
    add_hosts=[],
    blkio_weight=None,
    blkio_weight_device=[],
    cap_add=[],
    cap_drop=[],
    cgroup_parent=None,
    cidfile=None,
    cpu_period=None,
    cpu_quota=None,
    cpu_rt_period=None,
    cpu_rt_runtime=None,
    cpu_shares=None,
    cpus=None,
    cpuset_cpus=None,
    cpuset_mems=None,
    detach=False,
    devices=[],
    device_cgroup_rules=[],
    device_read_bps=[],
    device_read_iops=[],
    device_write_bps=[],
    device_write_iops=[],
    content_trust=False,
    dns=[],
    dns_options=[],
    dns_search=[],
    domainname=None,
    entrypoint=None,
    envs={},
    env_files=[],
    expose=[],
    gpus=None,
    groups_add=[],
    healthcheck=True,
    health_cmd=None,
    health_interval=None,
    health_retries=None,
    health_start_period=None,
    health_timeout=None,
    hostname=None,
    init=False,
    ip=None,
    ip6=None,
    ipc=None,
    isolation=None,
    kernel_memory=None,
    labels={},
    label_files=[],
    link=[],
    link_local_ip=[],
    log_driver=None,
    log_options=[],
    mac_address=None,
    memory=None,
    memory_reservation=None,
    memory_swap=None,
    memory_swappiness=None,
    mounts=[],
    name=None,
    networks=[],
    network_aliases=[],
    oom_kill=True,
    oom_score_adj=None,
    pid=None,
    pids_limit=None,
    platform=None,
    privileged=False,
    publish=[],
    publish_all=False,
    read_only=False,
    restart=None,
    remove=False,
    runtime=None,
    security_options=[],
    shm_size=None,
    sig_proxy=True,
    stop_signal=None,
    stop_timeout=None,
    storage_options=[],
    stream=False,
    sysctl={},
    tmpfs=[],
    ulimit=[],
    user=None,
    userns=None,
    uts=None,
    volumes=[],
    volume_driver=None,
    volumes_from=[],
    workdir=None
)
```


Runs a container

You can use `docker.run` or `docker.container.run` to call this function.

For a deeper dive into the arguments and what they do, visit
<https://docs.docker.com/engine/reference/run/>

If you want to know exactly how to call `docker.run()` depending on your
use case (detach, stream...), take a look at
the [`docker.run()` guide](../user_guide/docker_run.md).

```python
>>> from python_on_whales import docker
>>> returned_string = docker.run("hello-world")
>>> print(returned_string)

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

```python
>>> from python_on_whales import docker
>>> result_string = docker.run("ubuntu", ["ls", "/host"], volumes=[("/", "/host", "ro")])
>>> print(result_string)
bin
boot
dev
etc
home
init
lib
lib64
lost+found
media
mnt
opt
proc
projects
root
run
sbin
snap
srv
sys
tmp
usr
var
```

__Arguments__

- __image__ `Union[str, python_on_whales.Image]`: The docker image to use for the container
- __command__ `List[str]`: List of arguments to provide to the container.
- __add_hosts__ `List[Tuple[str, str]]`: hosts to add in the format of a tuple. For example,
    `add_hosts=[("my_host_1", "192.168.30.31"), ("host2", "192.168.80.81")]`
- __blkio_weight__ `Optional[int]`: Block IO (relative weight), between 10 and 1000,
    or 0 to disable (default 0)
- __cpu_period__ `Optional[int]`: Limit CPU CFS (Completely Fair Scheduler) period
- __cpu_quota__ `Optional[int]`: Limit CPU CFS (Completely Fair Scheduler) quota
- __cpu_rt_period__ `Optional[int]`: Limit CPU real-time period in microseconds
- __cpu_rt_runtime__ `Optional[int]`: Limit CPU real-time runtime in microseconds
- __cpu_shares__ `Optional[int]`: CPU shares (relative weight)
- __cpus__ `Optional[float]`: The maximal amount of cpu the container can use.
    `1` means one cpu core.
- __cpuset_cpus__ `Optional[List[int]]`: CPUs in which to allow execution. Must be given as a list.
- __cpuset_mems__ `Optional[List[int]]`: MEMs in which to allow execution. Must be given as a list.
- __detach__ `bool`: If `False`, returns the ouput of the container as a string.
    If `True`, returns a [`python_on_whales.Container`](/docker_objects/containers/) object.
- __dns_search__ `List[str]`: Set custom DNS search domains
- __domainname__ `Optional[str]`: Container NIS domain name
- __entrypoint__ `Optional[str]`: Overwrite the default ENTRYPOINT of the image
- __envs__ `Dict[str, str]`: Environment variables as a `dict`.
    For example: `{"OMP_NUM_THREADS": 3}`
- __env_files__ `Union[str, pathlib.Path, List[Union[str, pathlib.Path]]]`: One or a list of env files.
- __gpus__ `Optional[Union[int, str]]`: For this to work, you need the
    [Nvidia container runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#install-guide)
    The value needed is a `str` or `int`. Some examples of valid argument
    are `"all"` or `"device=GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a"` or
    `"device=0,2"`. If you want 3 gpus, just write `gpus=3`.
- __hostname__ `Optional[str]`: Container host name
- __ip__ `Optional[str]`: IPv4 address (e.g., 172.30.100.104)
- __ip6__ `Optional[str]`: IPv6 address (e.g., 2001:db8::33)
- __ipc__ `Optional[str]`: IPC mode to use
- __isolation__ `Optional[str]`: Container isolation technology
- __kernel_memory__ `Optional[Union[int, str]]`: Kernel memory limit. `int` represents the number of bytes,
    but you can use `"4k"` or `2g` for example.
- __log_driver__ `Optional[str]`: Logging driver for the container
- __mac_adress__: Container MAC address (e.g., `"92:d0:c6:0a:29:33"`)
- __memory__ `Optional[Union[int, str]]`:  Memory limit, valid values are `1024` (ints are bytes) or
    `"43m"` or `"6g"`.
- __memory_reservation__ `Optional[Union[int, str]]`: Memory soft limit
- __memory_swap__ `Optional[Union[int, str]]`: Swap limit equal to memory plus swap: '-1'
    to enable unlimited swap.
- __memory_swappiness__ `Optional[int]`: Tune container memory swappiness (0 to 100) (default -1)
- __name__ `Optional[str]`: The container name. If not provided, one is automatically genrated for
    you.
- __healthcheck__ `bool`: Set to `False` to disable container periodic healthcheck.
- __oom_kill__ `bool`: Set to `False` to disable the OOM killer for this container.
- __pid__ `Optional[str]`: PID namespace to use
- __pids_limit__ `Optional[int]`: Tune container pids limit (set `-1` for unlimited)
- __platform__ `Optional[str]`: Set platform if server is multi-platform capable.
- __privileged__ `bool`: Give extended privileges to this container.
- __publish__ `List[Union[Tuple[Union[str, int], Union[str, int]], Tuple[Union[str, int], Union[str, int], str]]]`: Ports to publish, same as the `-p` argument in the Docker CLI.
    example are `[(8000, 7000) , ("127.0.0.1:3000", 2000)]` or
    `[("127.0.0.1:3000", 2000, "udp")]`.
- __publish_all__ `bool`: Publish all exposed ports to random ports.
- __read_only__ `bool`: Mount the container's root filesystem as read only.
- __restart__ `Optional[str]`: Restart policy to apply when a container exits (default "no")
- __remove__ `bool`: Automatically remove the container when it exits.
- __runtime__ `Optional[str]`: Runtime to use for this container.
- __security_options__ `List[str]`: Security options
- __shm_size__ `Optional[Union[int, str]]`: Size of /dev/shm. `int` is for bytes. But you can use `"512m"` or
    `"4g"` for example.
- __stop_timeout__ `Optional[int]`: Signal to stop a container (default "SIGTERM")
- __storage_options__ `List[str]`: Storage driver options for the container
- __user__ `Optional[str]`: Username or UID (format: `<name|uid>[:<group|gid>]`)
- __userns__ `Optional[str]`:  User namespace to use
- __uts__ `Optional[str]`:  UTS namespace to use
- __volumes__ `Optional[List[Union[Tuple[Union[python_on_whales.Volume, str, pathlib.Path], Union[str, pathlib.Path]], Tuple[Union[python_on_whales.Volume, str, pathlib.Path], Union[str, pathlib.Path], str]]]]`:  Bind mount a volume. Some examples:
    `[("/", "/host"), ("/etc/hosts", "/etc/hosts", "rw")]`.
- __volume_driver__ `Optional[str]`: Optional volume driver for the container
- __workdir__ `Optional[Union[str, pathlib.Path]]`: The directory in the container where the process will be executed.

__Returns__

The container output as a string if detach is `False` (the default),
and a [`python_on_whales.Container`](/docker_objects/containers/) if detach is `True`.


----

## start


```python
docker.container.start(containers, attach=False, stream=False)
```


Starts one or more stopped containers.

Aliases: `docker.start`, `docker.container.start`,
`python_on_whales.Container.start`.

__Arguments__

- __containers__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or a list of containers.


----

## stats


```python
docker.container.stats()
```


Get containers resource usage statistics

Alias: `docker.stats(...)`

Not yet implemented


----

## stop


```python
docker.container.stop(containers, time=None)
```


Stops one or more running containers

Alias: `docker.stop(...)`

Aliases: `docker.stop`, `docker.container.stop`,
`python_on_whales.Container.stop`.

__Arguments__

- __containers__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or a list of containers.
- __time__ `Optional[Union[int, datetime.timedelta]]`: Seconds to wait for stop before killing a container (default 10)


----

## top


```python
docker.container.top()
```


Get the running processes of a container

Alias: `docker.top(...)`

Not yet implemented


----

## unpause


```python
docker.container.unpause(x)
```


Unpause all processes within one or more containers

Alias: `docker.unpause(...)`

__Arguments__

- __x__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or more containers (name, id or [`python_on_whales.Container`](/docker_objects/containers/) object).


----

## update


```python
docker.container.update(
    x,
    blkio_weight=None,
    cpu_period=None,
    cpu_quota=None,
    cpu_rt_period=None,
    cpu_rt_runtime=None,
    cpu_shares=None,
    cpus=None,
    cpuset_cpus=None,
    cpuset_mems=None,
    kernel_memory=None,
    memory=None,
    memory_reservation=None,
    memory_swap=None,
    pids_limit=None,
    restart=None,
)
```


Update configuration of one or more containers

Alias: `docker.update(...)`

__Arguments__

- __x__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or a list of containers to update.
- __blkio_weight__ `Optional[int]`: Block IO (relative weight), between 10 and 1000,
    or 0 to disable (default 0)
- __cpu_period__ `Optional[int]`: Limit CPU CFS (Completely Fair Scheduler) period
- __cpu_quota__ `Optional[int]`: Limit CPU CFS (Completely Fair Scheduler) quota
- __cpu_rt_period__ `Optional[int]`: Limit CPU real-time period in microseconds
- __cpu_rt_runtime__ `Optional[int]`: Limit CPU real-time runtime in microseconds
- __cpu_shares__ `Optional[int]`: CPU shares (relative weight)
- __cpus__ `Optional[float]`: The maximal amount of cpu the container can use.
    `1` means one cpu core.
- __cpuset_cpus__ `Optional[List[int]]`: CPUs in which to allow execution. Must be given as a list.
- __cpuset_mems__ `Optional[List[int]]`: MEMs in which to allow execution. Must be given as a list.
- __memory__ `Optional[Union[int, str]]`:  Memory limit, valid values are `1024` (ints are bytes) or
    `"43m"` or `"6g"`.
- __memory_reservation__ `Optional[Union[int, str]]`: Memory soft limit
- __memory_swap__ `Optional[Union[int, str]]`: Swap limit equal to memory plus swap: '-1'
    to enable unlimited swap.
- __pids_limit__ `Optional[int]`: Tune container pids limit (set `-1` for unlimited)
- __restart__ `Optional[str]`: Restart policy to apply when a container exits (default "no")


----

## wait


```python
docker.container.wait(x)
```


Block until one or more containers stop, then returns their exit codes

Alias: `docker.wait(...)`


__Arguments__

- __x__ `Union[python_on_whales.Container, str, List[Union[python_on_whales.Container, str]]]`: One or a list of containers to wait for.

__Returns__

An `int` if a single container was passed as argument or a list of ints
if multiple containers were passed as arguments.

Some Examples:

```python
cont = docker.run("ubuntu", ["bash", "-c", "sleep 2 && exit 8"], detach=True)

exit_code = docker.wait(cont)

print(exit_code)
# 8
docker.container.remove(cont)
```

```python
cont_1 = docker.run("ubuntu", ["bash", "-c", "sleep 4 && exit 8"], detach=True)
cont_2 = docker.run("ubuntu", ["bash", "-c", "sleep 2 && exit 10"], detach=True)

exit_codes = docker.wait([cont_1, cont_2])

print(exit_codes)
# [8, 10]
docker.container.remove([cont_1, cont_2])
```


----

