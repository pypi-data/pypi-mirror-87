# The Docker client object


## DockerClient


```python
python_on_whales.DockerClient(
    config=None,
    context=None,
    debug=None,
    host=None,
    log_level=None,
    tls=None,
    tlscacert=None,
    tlscert=None,
    tlskey=None,
    tlsverify=None,
    client_config=None,
)
```


Creates a Docker client

Note that
```python
from python_on_whales import docker
print(docker.run("hello-world"))
```
is equivalent to
```python
from python_on_whales import DockerClient
docker = DockerClient()
print(docker.run("hello-world")
```

__Arguments__

- __config__ `Optional[Union[str, pathlib.Path]]`: Location of client config files (default "~/.docker")
- __context__ `Optional[str]`: Name of the context to use to connect to the
    daemon (overrides DOCKER_HOST env var
    and default context set with "docker context use")
- __debug__ `Optional[bool]`: Enable debug mode
- __host__ `Optional[str]`: Daemon socket(s) to connect to
- __log_level__ `Optional[str]`: Set the logging level ("debug"|"info"|"warn"|"error"|"fatal")
   (default "info")
- __tls__ `Optional[bool]`:  Use TLS; implied by `tlsverify`
- __tlscacert__ `Optional[Union[str, pathlib.Path]]`: Trust certs signed only by this CA (default "~/.docker/ca.pem")


----

## login


```python
docker.login(server=None, username=None, password=None)
```


Log in to a Docker registry.

If no server is specified, the default is defined by the daemon.

__Arguments__

- __server__ `Optional[str]`: The server to log into. For example, with a self-hosted registry
    it might be something like `server="192.168.0.10:5000"`
- __username__ `Optional[str]`: The username
- __password__ `Optional[str]`: The password


----

## login_ecr


```python
docker.login_ecr(aws_access_key_id=None, aws_secret_access_key=None, region_name=None)
```


Login to the aws ECR registry. If the credentials are not provided as
arguments, they are taken from the environment variables as defined
in [the aws docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html).

Those are `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`.


----

## logout


```python
docker.logout(server=None)
```


Logout from a Docker registry

__Arguments__

- __server__ `Optional[str]`: The server to logout from. For example, with a self-hosted registry
    it might be something like `server="192.168.0.10:5000"`


----

## version


```python
docker.version()
```


Not yet implemented


----



# Sub-commands
* [`docker.app`](sub-commands/app.md)
* [`docker.buildx`](sub-commands/buildx.md)
* [`docker.compose`](sub-commands/compose.md)
* [`docker.config`](sub-commands/config.md)
* [`docker.container`](sub-commands/container.md)
* [`docker.context`](sub-commands/context.md)
* [`docker.image`](sub-commands/image.md)
* [`docker.manifest`](sub-commands/manifest.md)
* [`docker.network`](sub-commands/network.md)
* [`docker.node`](sub-commands/node.md)
* [`docker.secret`](sub-commands/secret.md)
* [`docker.service`](sub-commands/service.md)
* [`docker.stack`](sub-commands/stack.md)
* [`docker.swarm`](sub-commands/swarm.md)
* [`docker.system`](sub-commands/system.md)
* [`docker.trust`](sub-commands/trust.md)
* [`docker.volume`](sub-commands/volume.md)


# Other commands

They're actually aliases

* [`docker.build`](sub-commands/buildx.md#build)
* [`docker.commit`](sub-commands/container.md#commit)
* [`docker.copy`](sub-commands/container.md#copy)
* [`docker.create`](sub-commands/container.md#create)
* [`docker.diff`](sub-commands/container.md#diff)
* [`docker.execute`](sub-commands/container.md#execute)
* [`docker.export`](sub-commands/container.md#export)
* [`docker.images`](sub-commands/image.md#list)
* [`docker.import_`](sub-commands/image.md#import_)
* [`docker.info`](sub-commands/system.md#info)
* [`docker.kill`](sub-commands/container.md#kill)
* [`docker.load`](sub-commands/image.md#load)
* [`docker.logs`](sub-commands/container.md#logs)
* [`docker.pause`](sub-commands/container.md#pause)
* [`docker.ps`](sub-commands/container.md#list)
* [`docker.pull`](sub-commands/image.md#pull)
* [`docker.push`](sub-commands/image.md#push)
* [`docker.rename`](sub-commands/container.md#rename)
* [`docker.restart`](sub-commands/container.md#restart)
* [`docker.remove`](sub-commands/container.md#remove)
* [`docker.run`](sub-commands/container.md#run)
* [`docker.save`](sub-commands/image.md#save)
* [`docker.start`](sub-commands/container.md#start)
* [`docker.stats`](sub-commands/container.md#stats)
* [`docker.stop`](sub-commands/container.md#stop)
* [`docker.tag`](sub-commands/image.md#tag)
* [`docker.top`](sub-commands/container.md#stop)
* [`docker.unpause`](sub-commands/container.md#unpause)
* [`docker.update`](sub-commands/container.md#update)
* [`docker.wait`](sub-commands/container.md#wait)
