
class Interface(object):
    __manager__ = None
    __component__ = None

    def __init__(self, manager, component):
        object.__setattr__(self, "__manager__", manager)
        object.__setattr__(self, "__component__", component)

    def __getattr__(self, name):
        man = object.__getattribute__(self, "__manager__")
        comp = object.__getattribute__(self, "__component__")
        return getattr(man._get_component_real(comp), name)

    def __setattr__(self, name, arg):
        man = object.__getattribute__(self, "__manager__")
        comp = object.__getattribute__(self, "__component__")
        return setattr(man._get_component_real(comp), name, arg)
