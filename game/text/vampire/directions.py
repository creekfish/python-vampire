from game.text.things import Direction, IndexOfThings

east, west = Direction.create_dimension(name='East', aliases=['E'], opposite_name='West', opposite_aliases=['W'])
north, south = Direction.create_dimension(name='North', aliases=['N'], opposite_name='South', opposite_aliases=['S'])
up, down = Direction.create_dimension(name='Up', aliases=['U'], opposite_name='Down', opposite_aliases=['D'])

all_directions = IndexOfThings((east, west, north, south, up, down))
