## copy_from


```python
docker.image.copy_from(image, path_in_image, destination)
```


----

## copy_to


```python
docker.image.copy_to(base_image, local_path, path_in_image, new_tag=None)
```


----

## history


```python
docker.image.history()
```


Not yet implemented


----

## import_


```python
docker.image.import_(source, tag=None, changes=[], message=None, platform=None)
```


Import the contents from a tarball to create a filesystem image

Alias: `docker.import_(...)`

__Arguments__

- __changes__ `List[str]`: Apply Dockerfile instruction to the created image
- __message__ `Optional[str]`: Set commit message for imported image
- __platform__ `Optional[str]`: Set platform if server is multi-platform capable


----

## inspect


```python
docker.image.inspect(x)
```


Creates a `python_on_whales.Image` object.


----

## list


```python
docker.image.list()
```


Returns the list of Docker images present on the machine.

Alias: `docker.images()`

Note that each image may have multiple tags.

__Returns__

A `List[python_on_whales.Image]` object.


----

## load


```python
docker.image.load(input, quiet=False)
```


Loads one or multiple Docker image(s) from a tar or an iterator of `bytes`.

Alias: `docker.load(...)`

__Arguments__

- __input__ `Union[str, pathlib.Path, bytes, Iterator[bytes]]`: Path or input stream to load the images from.
- __quiet__ `bool`: If you don't want to display the progress bars.

__Returns__

`None` when using bytes as input. A `List[str]` (list of tags)
 when a path is provided.


----

## prune


```python
docker.image.prune(all=False, filter={})
```


Remove unused images

__Arguments__

- __all__ `bool`: Remove all unused images, not just dangling ones
- __filter__ `Dict[str, str]`: Provide filter values (e.g. `{"until": "<timestamp>"}`)


----

## pull


```python
docker.image.pull(image_name, quiet=False)
```


Pull a docker image

Alias: `docker.pull(...)`

__Arguments__

- __image_name__ `str`: The image name
- __quiet__ `bool`: If you don't want to see the progress bars.

__Returns:__

The Docker image loaded (`python_on_whales.Image` object).


----

## push


```python
docker.image.push(tag_or_repo, quiet=False)
```


Push a tag or a repository to a registry

Alias: `docker.push(...)`

__Arguments__

- __tag_or_repo__ `str`: Tag or repo to push
- __quiet__ `bool`: If you don't want to see the progress bars.


----

## remove


```python
docker.image.remove(x, force=False, prune=True)
```


Remove one or more docker images.

__Arguments__

- __x__ `Union[str, python_on_whales.Image, List[Union[str, python_on_whales.Image]]]`: Single image or list of Docker images to remove. You can use tags or
    `python_on_whales.Image` objects.
- __force__ `bool`: Force removal of the image
- __prune__ `bool`: Delete untagged parents


----

## save


```python
docker.image.save(images, output=None)
```


Save one or more images to a tar archive. Returns a stream if output is `None`

Alias: `docker.save(...)`

__Arguments__

- __images__ `Union[str, python_on_whales.Image, List[Union[str, python_on_whales.Image]]]`: Single docker image or list of docker images to save
- __output__ `Optional[Union[str, pathlib.Path]]`: Path of the tar archive to produce. If `output` is None, a generator
    of bytes is produced. It can be used to stream those bytes elsewhere,
    to another Docker daemon for example.

__Returns__

`Optional[Iterator[bytes]]`. If output is a path, nothing is returned.

An example of transfer of an image from a local Docker daemon to a remote Docker
daemon. We assume that the remote machine has an ssh access:

```python
from python_on_whales import DockerClient

local_docker = DockerClient()
remote_docker = DockerClient(host="ssh://my_user@186.167.32.84")

image_name = "busybox:1"
local_docker.pull(image_name)
bytes_iterator = local_docker.image.save(image_name)

remote_docker.image.load(bytes_iterator)
```

Of course the best solution is to use a registry to transfer image but
it's a cool example nonetheless.


----

## tag


```python
docker.image.tag(source_image, new_tag)
```


Adds a tag to a Docker image.

Alias: `docker.tag(...)`

__Arguments__

- __source_image__ `Union[python_on_whales.Image, str]`: The Docker image to tag. You can use a tag to reference it.
- __new_tag__ `str`: The tag to add to the Docker image.


----

