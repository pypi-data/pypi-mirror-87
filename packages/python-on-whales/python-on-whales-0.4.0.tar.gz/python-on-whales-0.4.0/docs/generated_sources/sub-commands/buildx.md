## bake


```python
docker.buildx.bake(
    targets=[],
    builder=None,
    files=[],
    load=False,
    cache=True,
    print=False,
    progress="auto",
    pull=False,
    push=False,
    set={},
    variables={},
)
```


Bake is similar to make, it allows you to build things declared in a file.

For example it allows you to build multiple docker image in parallel.

The CLI docs is [here](https://github.com/docker/buildx#buildx-bake-options-target)
and it contains a lot more information.

__Arguments__

- __targets__ `Union[str, List[str]]`: Targets or groups of targets to build.
- __builder__ `Optional[Union[str, python_on_whales.Builder]]`: The builder to use.
- __files__ `Union[str, pathlib.Path, List[Union[str, pathlib.Path]]]`: Build definition file(s)
- __load__ `bool`: Shorthand for `set=["*.output=type=docker"]`
- __cache__ `bool`: Whether to use the cache or not.
- __print__ `bool`: Do nothing, just returns the config.
- __progress__ `Union[str, bool]`: Set type of progress output (`"auto"`, `"plain"`, `"tty"`,
    or `False`). Use plain to keep the container output on screen
- __pull__ `bool`: Always try to pull the newer version of the image
- __push__ `bool`: Shorthand for `set=["*.output=type=registry"]`
- __set__ `Dict[str, str]`: A list of overrides in the form `"targetpattern.key=value"`.
- __variables__ `Dict[str, str]`: A dict containing the values of the variables defined in the
    hcl file. See <https://github.com/docker/buildx#hcl-variables-and-functions>

__Returns__

The configuration used for the bake (files merged + override with
the arguments used in the function). It's the loaded json you would
obtain by running `docker buildx bake --print --load my_target` if
your command was `docker buildx bake --load my_target`. Some example here.

```python
from python_on_whales import docker

# returns the config used and runs the builds
config = docker.buildx.bake(["my_target1", "my_target2"], load=True)
assert config == {
    "target": {
        "my_target1": {
            "context": "./",
            "dockerfile": "Dockerfile",
            "tags": ["pretty_image1:1.0.0"],
            "target": "out1",
            "output": ["type=docker"]
        },
        "my_target2": {
            "context": "./",
            "dockerfile": "Dockerfile",
            "tags": ["pretty_image2:1.0.0"],
            "target": "out2",
            "output": ["type=docker"]
        }
    }
}

# returns the config only, doesn't run the builds
config = docker.buildx.bake(["my_target1", "my_target2"], load=True, print=True)
```


----

## build


```python
docker.buildx.build(
    context_path,
    add_hosts={},
    allow=[],
    build_args={},
    builder=None,
    cache=True,
    cache_from=None,
    cache_to=None,
    file=None,
    labels={},
    load=False,
    network=None,
    output=None,
    platforms=None,
    progress="auto",
    pull=False,
    push=False,
    secrets=[],
    ssh=None,
    tags=[],
    target=None,
    return_image=False,
)
```


Build a Docker image with builkit as backend.

Alias: `docker.build(...)`

A `python_on_whales.Image` is returned, even when using multiple tags.
That is because it will produce a single image with multiple tags.

__Arguments__

- __context_path__ `Union[str, pathlib.Path]`: The path of the build context.
- __add_hosts__ `Dict[str, str]`: Hosts to add. `add_hosts={"my_host1": "192.168.32.35"}`
- __allow__ `List[str]`: List of extra privileges.
    Eg `allow=["network.host", "security.insecure"]`
- __build_args__ `Dict[str, str]`: The build arguments.
    ex `build_args={"PY_VERSION": "3.7.8", "UBUNTU_VERSION": "20.04"}`.
- __builder__ `Optional[Union[str, python_on_whales.Builder]]`: Specify which builder to use.
- __cache__ `bool`: Whether or not to use the cache
- __cache_from__ `Optional[str]`: Works only with the container driver. Loads the cache
    (if needed) from a registry `cache_from="user/app:cache"`  or
    a directory on the client `cache_from="type=local,src=path/to/dir"`.
- __cache_to__ `Optional[str]`: Works only with the container driver. Sends the resulting
    docker cache either to a registry `cache_to="user/app:cache"`,
    or to a local directory `cache_to="type=local,dest=path/to/dir"`.
- __file__ `Optional[Union[str, pathlib.Path]]`: The path of the Dockerfile
- __labels__ `Dict[str, str]`: Dict of labels to add to the image.
    `labels={"very-secure": "1", "needs-gpu": "0"}` for example.
- __load__ `bool`: Shortcut for `output=dict(type="docker")` If `True`,
    `docker.buildx.build` will return a `python_on_whales.Image`.
- __network__ `Optional[str]`: which network to use when building the Docker image
- __output__ `Optional[Dict[str, str]]`: Output destination
    (format: `output={"type": "local", "dest": "path"}`
    Possible output types are
    `["local", "tar", "oci", "docker", "image", "registry"]`.
    See [this link](https://github.com/docker/buildx#-o---outputpath-typetypekeyvalue)
    for more details about each exporter.
- __platforms__ `Optional[List[str]]`: List of target platforms when building the image. Ex:
    `platforms=["linux/amd64", "linux/arm64"]`
- __progress__ `Union[str, bool]`: Set type of progress output (auto, plain, tty, or False).
    Use plain to keep the container output on screen
- __pull__ `bool`: Always attempt to pull a newer version of the image
- __push__ `bool`: Shorthand for `output=dict(type="registry")`.
- __secrets__ `Union[str, List[str]]`: One or more secrets passed as string(s). For example
    `secrets="id=aws,src=/home/my_user/.aws/credentials"`
- __ssh__ `Optional[str]`: SSH agent socket or keys to expose to the build
    (format is `default|<id>[=<socket>|<key>[,<key>]]` as a string)
- __tags__ `Union[str, List[str]]`: Tag or tags to put on the resulting image.
- __target__ `Optional[str]`: Set the target build stage to build.
- __return_image__ `bool`: Return the created docker image if `True`, needs
    at least one `tags`.

__Returns__

A `python_on_whales.Image` if `return_image=True`. Otherwise, `None`.


----

## create


```python
docker.buildx.create(context_or_endpoint=None, use=False)
```


----

## disk_usage


```python
docker.buildx.disk_usage()
```


Not yet implemented


----

## inspect


```python
docker.buildx.inspect()
```


Not yet implemented


----

## list


```python
docker.buildx.list()
```


Not yet implemented


----

## prune


```python
docker.buildx.prune(all=False, filters={})
```


Remove build cache on the current builder.

__Arguments__

- __all__ `bool`: Remove all cache, not just dangling layers
- __filters__ `Dict[str, str]`: Filters to use, for example `filters=dict(until="24h")`


----

## remove


```python
docker.buildx.remove(builder)
```


Remove a builder

__Arguments__

- __builder__ `Union[python_on_whales.Builder, str]`: The builder to remove


----

## stop


```python
docker.buildx.stop()
```


Not yet implemented


----

## use


```python
docker.buildx.use(builder, default=False, global_=False)
```


----

## version


```python
docker.buildx.version()
```


Returns the docker buildx version as a string.


----

