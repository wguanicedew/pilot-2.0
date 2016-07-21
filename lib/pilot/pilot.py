from components import ComponentManager


class Pilot(ComponentManager):
    def __init__(self):
        ComponentManager.__init__(self)

    def main(self):
        pass

if __name__ == '__main__':
    pilot = Pilot()

    pilot.load_component('example_component')
    pilot.get_component('example_component').foo()

    T = pilot.load_component('example_component', 'extended')
    pilot.example_component.foo()

    T = pilot.load_component('example_component', 'undefined')
    pilot.get_component('example_component').foo()
