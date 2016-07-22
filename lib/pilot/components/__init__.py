from component import Component
from interface import Interface
from importlib import import_module
from errors import ComponentManagerReservedError, ComponentManagerSetError, ComponentManagerNotAComponentError

__reserved_names__ = ['component', 'errors', 'interface']


class ComponentManager(object):
    """
    This is component manager. Through it you can simply without any pain extend your program with a variety of
    components, moreover on the go. You just need to place your component in a specified folder and load it, then it is
    available. No code changing, no registering, all is automated.

    The other feature is to change components on the go. Once you found, one of your components needs to be changed,
    just load new one and it will be replaced.

    Full documentation is located in DOCUMENTATION.md alongside this file.
    """
    component_types = None

    def __init__(self):
        self.component_types = dict()

    def find_component_type(self, name):
        if name in self.component_types:
            return self.component_types[name]

        if name in __reserved_names__:
            raise ComponentManagerReservedError('This name is reserved')

        c_type = import_module('components.' + name)

        base = {
            "stub": c_type.Stub,
            "type": c_type
        }

        if not issubclass(c_type.Stub, Component):
            raise ComponentManagerNotAComponentError("Not a component")

        base['loaded'] = base['stub']
        base['name'] = 'stub'
        base['instance'] = base['loaded'](None)
        base['interface'] = Interface(self, name)

        self.component_types[name] = base

        return self.component_types[name]

    def __load_component(self, component_type, name):
        ct = self.component_types[component_type]
        if ct['name'] != name:

            if name == 'stub':
                ct['loaded'] = ct['stub']
            else:
                ct['loaded'] = getattr(import_module(ct['type'].__name__ + '.' + name), ct['stub'].__name__)

            old = ct['instance']
            if old:
                old.__switch__()
            ct['instance'] = ct['loaded'](old)

            ct['name'] = name
        return ct

    def load_component(self, component_type, name='default'):
        ct = self.find_component_type(component_type)

        try:
            ct = self.__load_component(component_type, name)
        except ImportError:
            try:
                ct = self.__load_component(component_type, 'default')
            except ImportError:
                ct = self.__load_component(component_type, 'stub')

        return ct['interface']

    def _get_component_real(self, component_type):
        ct = self.find_component_type(component_type)
        return ct['instance']

    def get_component(self, component_type):
        ct = self.find_component_type(component_type)
        return ct['interface']

    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            if self.component_types and item in self.component_types:
                return self.get_component(item)
            raise

    def __setattr__(self, key, value):
        try:
            object.__getattribute__(self, key)
            object.__setattr__(self, key, value)
        except AttributeError:
            if self.component_types and key in self.component_types:
                raise ComponentManagerSetError("Can not set to the component.")
            object.__setattr__(self, key, value)


if __name__ == "__main__":
    raise AssertionError("It meant to run as a module, or component manager will not be able to get components")
