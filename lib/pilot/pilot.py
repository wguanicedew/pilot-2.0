from components import ComponentManager
from components.interface import Interface


class Pilot(ComponentManager):
    def __init__(self):
        ComponentManager.__init__(self)

    def main(self):
        pass

if __name__ == '__main__':
    pilot = Pilot()

    pilot.load_component('example_component')
    pilot.get_component('example_component').foo()
    i = pilot.get_component('example_component')
    i.foo()

    T = pilot.load_component('example_component', 'extended')
    pilot.example_component.foo()
    i.foo()
    j = pilot.example_component
    j.foo()

    T = pilot.load_component('example_component', 'undefined')
    pilot.get_component('example_component').foo()
    i.foo()
    j.foo()

    print ''
    I = Interface(pilot, 'example_component')
    pilot.example_component.ti(1)
    I.ti(1)
    pilot.example_component.ci(1)
    I.ci(1)
    pilot.example_component.si(1)
    I.si(1)

    print '--- prop:'
    print pilot.example_component.prop
    print I.prop

    print '--- prop set'
    pilot.example_component.prop = 'setted prop'
    I.prop = 'setted prop'

    print pilot.example_component.prop

    print '--- smth'
    print pilot.example_component.smth
    print I.smth
    print '--- smth set'
    pilot.example_component.smth = 1
    I.smth = 1
