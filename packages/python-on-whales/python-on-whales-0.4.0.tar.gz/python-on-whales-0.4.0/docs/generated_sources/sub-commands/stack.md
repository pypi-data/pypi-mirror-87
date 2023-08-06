## deploy


```python
docker.stack.deploy(
    name,
    compose_files=[],
    orchestrator=None,
    prune=False,
    resolve_image="always",
    with_registry_auth=False,
    env_files=[],
    variables={},
)
```


Deploys a stack.

__Arguments__

- __name__ `str`: The name of the stack to deploy. Mandatory.
- __compose_files__ `Union[str, pathlib.Path, List[Union[str, pathlib.Path]]]`: One or more docker-compose files. If there are more than
one, they will be fused together.
- __orchestrator__ `Optional[str]`: The orchestrator to use, `"swarm" or "kubernetes" or "all".
- __prune__ `bool`: Prune services that are no longer referenced
- __resolve_image__ `str`: Query the registry to resolve image digest
    and supported platforms `"always"|"changed"|"never"` (default `"always"`).
    Note that if the registry cannot be queried when using `"always"`, it's
    going to try to use images present locally on the nodes.
- __with_registry_auth__ `bool`: Send registry authentication details to Swarm agents.
    Required if you need to run `docker login` to pull the docker images
    in your stack.
- __env_files__ `List[Union[str, pathlib.Path]]`: Similar to `.env` files in docker-compose. Loads `variables` from
    `.env` files. If both `env_files` and `variables` are used, `variables`
    have priority. This behavior is similar to the one you would experience with
    compose.
- __variables__ `Dict[str, str]`: A dict dictating by what to replace the variables declared in
    the docker-compose files. In the docker CLI, you would use
    environment variables for this.

__Returns__

A `python_on_whales.Stack` object.


----

## list


```python
docker.stack.list()
```


Returns a list of `python_on_whales.Stack`

__Returns__

A `List[python_on_whales.Stack]`.


----

## ps


```python
docker.stack.ps()
```


Not yet implemented


----

## remove


```python
docker.stack.remove(x)
```


Removes one or more stacks.

__Arguments__

- __x__ `Union[str, python_on_whales.Stack, List[Union[str, python_on_whales.Stack]]]`: One or more stacks


----

## services


```python
docker.stack.services(stack)
```


List the services present in the stack.

__Arguments__

- __stack__ `Union[str, python_on_whales.Stack]`: A docker stack or the name of a stack.

__Returns__

A `List[python_on_whales.Stack]`


----

