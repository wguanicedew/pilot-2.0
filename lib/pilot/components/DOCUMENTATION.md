Introduction
============

`components` is a library providing component-based interface to your project.
The main class of it is `ComponentManager`, which does all the work.

As a restriction of Python importing system, all the components *must* be placed in the folder of the library.
However, they can themselves be folders or single files, but for sake of loading, it is better to make them foldered.


Component manager
=================

Component manager is presented as an extendable class, `ComponentManager`. Through it you can simply without
any pain extend your program with a variety of components, moreover on the go. You just need to place your component in
a specified folder and load it, then it is available. No code changing, no registering, all is automated.

The other feature is to change components on the go. Once you found, one of your components needs to be changed,
just load new one and it will be replaced.


Loading components
==================

To load a component, simply call `load_component` from your component manager instance. Then it will be present as
an attribute of the component manager.

Example:
```python
from components import ComponentManager

comp_man = ComponentManager()

my_comp = comp_man.load_component('example_component')
my_comp.foo()  # the 'default' component is used
...
```

There are three ways to access components:
```python
my_comp = comp_man.load_component('example_component', 'some_type')
my_comp = comp_man.get_component('example_component')  # previously loaded one
my_comp = comp_man.example_component  # previously loaded one
```

By default the 'default' version of component is loaded, if present. To load a specific version, add the second argument:
```python
...
comp_man.load_component('example_component', 'extended')
my_comp.foo()  # the 'extended' component is used
...
```

Along with 'default' component, one can introduce an abstract component, which will be preloaded on component search.
It will be used as a class reference and a stub component where no default component is present.

To switch the component anywhere in your code, just call `load_component` with the new type and the component will be
switched:
```python
...
my_comp.foo()  # previously loaded component is used

comp_man.load_component('example_component', 'new')
my_comp.foo()  # the 'new' component is now used
...
```

**NOTE!** Though referencing components themselves is transparent,
referencing object-properties of components might be tricky:
```python
...
comp_man.load_component('example_component', 'some')
my_comp = comp_man.example_component
my_prop = my_comp.some_object
my_prop is my_comp.some_object  # True

comp_man.load_component('example_component', 'new')
my_comp  # is now 'new'
my_prop  # is an object from 'example_component.some'
my_prop is my_comp.some_object  # False
...
comp_man.load_component('example_component', 'some')
my_prop  # is from old instance of 'example_component.some'
my_prop is my_comp.some_object  # still False
```


Creating components
===================

The simple
----------
To create a basic component, just add into components folder any component, that can be imported as a part of it and has
`Stub` attribute inside, that inherits from `components.component.Component`. This will be the simplest option.

The extenable
-------------
To make your component extendable, make it as follows:

1. Create a folder, named accordingly
2. Place `__init__.py` inside it, which will present a component interface class as `Stub`
3. Add files and folders into this which are named as types of your module and each of which holds the same class name
   in their basic namespace and inherit from `Stub`.

`Stub` is a reference class for the interface. It's name will be searched later in the implemented types.
**NOTE!** Your interface classes must be named in each component type exactly as the interface class. It may be the
class alias, but this must be preserved.

The example
-----------
Folder structure
```text
components
/...
|- example_component    # name of our component
|  /- __init__.py       # it's initializer
|  |- abstract.py       # types
|  |- default.py
|  \- some_other.py
\...
```
`__init__.py` contents:
```python
from abstract import ExampleComponent as Stub
```
`abstract.py` contents:
```python
from ..component import Component as Base

class ExampleComponent(Base):
    pass
```
Other classes contents:
```python
from .abstract import ExampleComponent as Base

class ExampleComponent(Base):
    pass
```
Other classes contents (alias example):
```python
from .abstract import ExampleComponent as Base

class ExampleComponentExtended(Base):
    pass

ExampleComponent = ExampleComponentExtended
```

The API
-------
As you've implemented as many as two different types, you may wonder, how do they swap. For this case, we presented a
very simple callback API to make the things easier.

### Referencing a previous instance
The `__init__` of each interface is to accept one parameter (except `self`), the previous instance. If it is not None,
then we can get all the features from it into our new instance.

### Preparing the instance to be changed
The other API option is to prepare all necessary things to be moved into the new instance. When the instance is about to
be switched, a method `__switch__` is called, no parameters required (except `self`). Thus it may prepare all the data
to be moved to the new instance and close all of the opened resources.

**NOTE!** `__switch__` is called first, then the new instance is created. So, if there was any locked resource, it may
be unlocked to lock it into the new one. Or it may appear, that during that time it was locked by another process, keep
it in mind.

The API interface is located in `components.component.Component` class. See the source.

### Example:
```python
from .abstract import ExampleComponent as Base

class ExampleComponent(Base):
    def __init__(self, previous):
        if previous:
            self.get_all_the_stuff_from(previous)
        else:
            self.make_new_stuff()
    
    def __switch__(self):
        self.prepare_stuff()
        self.cleanup()
```
