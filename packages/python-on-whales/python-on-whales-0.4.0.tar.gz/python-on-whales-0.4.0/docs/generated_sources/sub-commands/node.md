## demote


```python
docker.node.demote(x)
```


Demote one or more nodes from manager in the swarm

__Arguments__

- __x__ `Union[python_on_whales.Node, str, List[Union[python_on_whales.Node, str]]]`: One or a list of nodes.


----

## inspect


```python
docker.node.inspect(x)
```


Returns a `python_on_whales.Node` object from a string
(id or hostname of the node)

__Arguments__

- __x__ `Union[str, List[str]]`: One id or hostname or a list of ids or hostnames

__Returns__

One or a list of `python_on_whales.Node`


----

## list


```python
docker.node.list()
```


Returns the list of nodes in this swarm.

__Returns__

A `List[python_on_whales.Node]`


----

## promote


```python
docker.node.promote(x)
```


Promote one or more nodes to manager in the swarm

__Arguments__

- __x__ `Union[python_on_whales.Node, str, List[Union[python_on_whales.Node, str]]]`: One or a list of nodes.


----

## ps


```python
docker.node.ps()
```


Not yet implemented


----

## remove


```python
docker.node.remove(x, force=False)
```


Remove one or more nodes from the swarm

__Arguments__

- __x__ `Union[python_on_whales.Node, str, List[Union[python_on_whales.Node, str]]]`: One node or a list of nodes. You can use the id or the hostname of a node.
    You can also use a `python_on_whales.Node`.
- __force__ `bool`: Force remove a node from the swarm


----

## update


```python
docker.node.update(node, availability=None, labels_add={}, rm_labels=[], role=None)
```


Updates a Swarm node.

__Arguments__

- __node__ `Union[python_on_whales.Node, str]`: The node to update, you can use a string or a `python_on_whales.Node`
    object.
- __availability__ `Optional[str]`: Availability of the node ("active"|"pause"|"drain")
- __labels_add__ `Dict[str, str]`: Remove a node label if exists
- __rm_labels__ `List[str]`: Labels to remove from the node.
- __role__ `Optional[str]`: Role of the node ("worker"|"manager")


----

