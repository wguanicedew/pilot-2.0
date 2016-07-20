from component import Component
from importlib import import_module


class ComponentManager(object):

    def __init__(self):
        self.component_types = dict()

    def find_component_type(self, name):
        if name in self.component_types:
            return self.component_types[name]

        c_type = import_module('components.' + name)

        base = {
            "stub": c_type.Stub,
            "type": c_type
        }

        if not issubclass(c_type.Stub, Component):
            raise ImportError("Not a component")

        base['loaded'] = base['stub']
        base['name'] = 'stub'

        self.component_types[name] = base

        return self.component_types[name]

    def __load_component(self, component_type, name):
        ct = self.component_types[component_type]
        if ct['name'] == name:
            return ct['loaded']

        if name == 'stub':
            ct['loaded'] = ct['stub']
        else:
            ct['loaded'] = getattr(import_module(ct['type'].__name__ + '.' + name), ct['stub'].__name__)

        ct['name'] = name
        return ct['loaded']

    def load_component(self, component_type, name='default'):
        self.find_component_type(component_type)

        try:
            return self.__load_component(component_type, name)
        except ImportError:
            try:
                return self.__load_component(component_type, 'default')
            except ImportError:
                return self.__load_component(component_type, 'stub')


if __name__ == "__main__":
    raise AssertionError("It meant to run as a module, or component manager will not be able to get components")
