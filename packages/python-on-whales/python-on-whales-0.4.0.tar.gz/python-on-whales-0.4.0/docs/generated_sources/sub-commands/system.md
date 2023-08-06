## disk_free


```python
docker.system.disk_free()
```


Give information about the disk usage of the Docker daemon.

Returns a `python_on_whales.DiskFreeResult` object.

```python
from python_on_whales import docker
disk_free_result = docker.system.disk_free()
print(disk_free_result.images.active)  #int
print(disk_free_result.containers.reclaimable)  # int, number of bytes
print(disk_free_result.volumes.reclaimable_percent)  # float
print(disk_free_result.build_cache.total_count)  # int
print(disk_free_result.build_cache.size)  # int, number of bytes
...
```
Note that the number are not 100% accurate because the docker CLI
doesn't provide the exact numbers.

Maybe in a future implementation, we can provide exact numbers.

Verbose mode is not yet implemented.


----

## events


```python
docker.system.events()
```


Not yet implemented


----

## info


```python
docker.system.info()
```


Not yet implemented


----

## prune


```python
docker.system.prune(all=False, volumes=False)
```


Remove unused docker data

__Arguments__

- __all__ `bool`: Remove all unused images not just dangling ones
- __volumes__ `bool`: Prune volumes


----

