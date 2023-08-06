## clone


```python
docker.volume.clone(source, new_volume_name=None, driver=None, labels={}, options={})
```


Clone a volume.

__Arguments__

- __source__ `Union[python_on_whales.Volume, str]`: The volume to clone
- __new_volume_name__ `Optional[str]`: The new volume name. If not given, a random name is chosen.
- __driver__ `Optional[str]`: Specify volume driver name (default "local")
- __labels__ `Dict[str, str]`: Set metadata for a volume
- __options__ `Dict[str, str]`: Set driver specific options

__Returns__

A `python_on_whales.Volume`, the new volume.


----

## copy


```python
docker.volume.copy(source, destination)
```


Copy files/folders between a volume and the local filesystem.

__Arguments__

- __source__ `Union[str, pathlib.Path, Tuple[Union[python_on_whales.Volume, str], Union[str, pathlib.Path]]]`: If `source` is a directory/file inside a Docker volume,
    a tuple `(my_volume, path_in_volume)` must be provided. The volume
    can be a `python_on_whales.Volume` or a volume name as `str`. The path
    can be a `pathlib.Path` or a `str`. If `source` is  a local directory,
    a `pathlib.Path` or `str` should be provided. End the source path with
    `/.` if you want to copy the directory content in another directory.
- __destination__ `Union[str, pathlib.Path, Tuple[Union[python_on_whales.Volume, str], Union[str, pathlib.Path]]]`: Same as `source`.


----

## create


```python
docker.volume.create(volume_name=None, driver=None, labels={}, options={})
```


Creates a volume

__Arguments__

- __volume_name__ `Optional[str]`: The volume name, if not provided, a long random
    string will be used instead.
- __driver__ `Optional[str]`: Specify volume driver name (default "local")
- __labels__ `Dict[str, str]`: Set metadata for a volume
- __options__ `Dict[str, str]`: Set driver specific options


----

## inspect


```python
docker.volume.inspect(x)
```


----

## list


```python
docker.volume.list(filters={})
```


List volumes

__Arguments__

- __filters__ `Dict[str, Union[str, int]]`: See the [Docker documentation page about filtering
    ](https://docs.docker.com/engine/reference/commandline/volume_ls/#filtering).
    An example `filters=dict(dangling=1, driver="local")`.

__Returns__

`List[python_on_whales.Volume]`


----

## prune


```python
docker.volume.prune(filters={})
```


Remove volumes

__Arguments__

- __filters__ `Dict[str, Union[str, int]]`: See the [Docker documentation page about filtering
    ](https://docs.docker.com/engine/reference/commandline/volume_ls/#filtering).
    An example `filters=dict(dangling=1, driver="local")`.


----

## remove


```python
docker.volume.remove(x)
```


Removes one or more volumes

__Arguments__

- __x__ `Union[python_on_whales.Volume, str, List[Union[python_on_whales.Volume, str]]]`: A volume or a list of volumes.


----

