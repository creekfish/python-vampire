from game.text.things import Direction, IndexOfThings
from game.text.actions import GoAction


class VampireDirection(Direction):

    def get_action(self, name):
        if name == 'go':
            return GoAction(direction=self)
        else:
            raise KeyError()


east, west = VampireDirection.create_dimension(name='East', aliases=['E'], opposite_name='West', opposite_aliases=['W'])
north, south = VampireDirection.create_dimension(name='North', aliases=['N'], opposite_name='South', opposite_aliases=['S'])
up, down = VampireDirection.create_dimension(name='Up', aliases=['U'], opposite_name='Down', opposite_aliases=['D'])

all_directions = IndexOfThings((east, west, north, south, up, down))
