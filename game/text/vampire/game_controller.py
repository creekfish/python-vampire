from typing import List

import game.text.vampire.directions as directions
from game.text.grammars import SimpleGrammar
from game.text.text_games import TextGameSinglePlayer
from game.text.things import Thing, Action, Direction, Player, IndexOfThings
from game.text.results import ResultSuccess
from game.text.vampire import items, places


class Vampire(TextGameSinglePlayer):

    def __init__(self):
        self.time = 8 * 60   # game time in minutes
        self._places = None
        self._all_things = None

        self.connect_places()

        grammar = SimpleGrammar(things=self.all_things, raw_actions=self.game_actions)
        super().__init__('Vampire', grammar)
        self.dump_places()

    @property
    def starting_location(self):
        return self.places.lookup('Entrance Hall')

    def connect_places(self):
        self.places.lookup('Entrance Hall').connect_to(self.places.lookup('Library'), direction=directions.east)

    def welcome(self):
        return "Welcome to the VAMPIRE'S CASTLE Adventure\n\nDo you need the instructions? "




    @property
    def places(self) -> IndexOfThings:
#TODO: instead of list here, import all places from the module?
        if self._places is None:
            list_of_places = [
                places.EntranceHall(
                    self,
                    items=[items.Sign(self), items.Timepiece(self)],
                ),
                places.Library(
                    self,
                    items=[items.Crate(self), items.BrickFireplace(self)]
                ),
            ]
            self._places = IndexOfThings(list_of_places)
        return self._places

    @property
    def all_things(self) -> List[Thing]:
        if self._all_things is None:
            self._all_things = [place for place in self.places.values()]
            for place in self.places.values():
                self._all_things.extend(item for item in place.items.values())
            self._all_things.extend(direction for direction in self.directions.values())
        return self._all_things

    @property
    def directions(self) -> List[Direction]:
        return directions.all_directions

    def dump_places(self):
        for place in self.places.values():
            print(f'{place}')
            for connection in place.connections.values():
                print(f'    {connection}')
            for item in place.items.values():
                print(f'    {item}')