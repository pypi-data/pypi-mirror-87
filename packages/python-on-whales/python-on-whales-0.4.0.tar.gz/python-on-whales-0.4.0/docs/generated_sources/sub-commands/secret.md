## create


```python
docker.secret.create(name, file, driver=None, labels={}, template_driver=None)
```


Creates a `python_on_whales.Secret`.

__Returns__

A `python_on_whales.Secret` object.


----

## inspect


```python
docker.secret.inspect(x)
```


Returns one or more `python_on_whales.Secret` based on an ID or name.

__Arguments__

- __x__ `Union[str, List[str]]`: One or more IDs/names.


----

## list


```python
docker.secret.list(filters={})
```


Returns all secrets as a `List[python_on_whales.Secret]`.


----

## remove


```python
docker.secret.remove(x)
```


Removes one or more secrets

__Arguments__

- __x__ `Union[python_on_whales.components.secret.Secret, str, List[Union[python_on_whales.components.secret.Secret, str]]]`: One or more secrets.
    Name, ids or `python_on_whales.Secret` objects are valid inputs.


----

