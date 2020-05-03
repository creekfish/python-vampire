from game.text.things import Direction, IndexOfThings

east, west = Direction.create_dimension('East', 'West')
north, south = Direction.create_dimension('North', 'South')
up, down = Direction.create_dimension('Up', 'Down')

all_directions = IndexOfThings((east, west, north, south, up, down))
