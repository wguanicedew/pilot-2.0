from components import ComponentManager


class Pilot(ComponentManager):
    def __init__(self):
        ComponentManager.__init__(self)

    def main(self):
        pass

if __name__ == '__main__':
    pilot = Pilot()

    T = pilot.load_component('template_component')
    t = T()

    T = pilot.load_component('template_component', 'extended')
    t = T()

    T = pilot.load_component('template_component', 'undefined')
    t = T()
