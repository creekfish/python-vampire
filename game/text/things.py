import inspect
from abc import ABC, abstractmethod
from typing import Iterable, MutableMapping, TypeVar, Generic, AnyStr, Callable


class GameError(Exception):
    pass


class ThingError(GameError):
    def __init__(self, thing):
        super().__init__()
        self.thing = thing

    def __str__(self):
        return super().__str__() + f' ({self.thing})'


class ThingAlreadyInIndexError(ThingError):
    pass


class Result:
    def __init__(self, text, next_action=None):
        super().__init__()
        self.text = text
        self.next_action = next_action

    def __str__(self):
        return self.text


A = TypeVar('A')

#TODO: use Type[T] instead ala https://stackoverflow.com/questions/55819918/python-type-annotation-for-a-function-that-accepts-a-type-and-returns-a-value-of
#TODO: no, but the line below should work?
#T = TypeVar('T', 'Thing', 'Place', 'Item', 'Direction', 'Actor', 'Action')
T = TypeVar('T', bound='Thing')

#TODO: why use generics at all, can we not just say class IndexOfThings(Index[AnyStr, 'Thing']):


class Index(MutableMapping, Generic[AnyStr, A]):
    def __init__(self, *args, **kwargs):
        self._index = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._index[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._index[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self._index[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._index)

    def __len__(self):
        return len(self._index)

    def __keytransform__(self, key):
        return key


class IndexOfThings(Index[AnyStr, T]):
    def __init__(self, things: Iterable[T]=None):
        super().__init__()
        if things is not None:
            self.add_things(things)

    def __setitem__(self, index_key, thing: T):
        if index_key not in self:
            super().__setitem__(index_key, thing)
        else:
            raise ThingAlreadyInIndexError(thing=thing)

    def lookup(self, index_key: str) -> T:
        """Look up and return a thing by the given index key.
        """
        key = Thing.get_prefix(index_key.lower())
        return self[key]

    def add_thing(self, thing: T):
        """Add a thing to this index of things.
        """
        for index_key in thing.index_keys:
            self[index_key] = thing

    def add_things(self, things: Iterable[T]):
        """Add a list of things to this index of things.
        """
        for thing in things:
            self.add_thing(thing)

    def remove_thing(self, thing):
        """Remove a thing from this index of things.
        """
        for index_key in thing.index_keys:
            del self[index_key]

    def values(self):
        return list(set(super().values()))

    def keys(self):
        return list(super().keys())

    def __str__(self):
        return ','.join(str(thing) for thing in self.values())


class Thing(ABC):
    def __init__(self, game, name, aliases=None):
        super().__init__()
        self.game = game
        self.name = name
        self.aliases = aliases or []
        self.index_keys = self.generate_index_keys()

    def generate_index_keys(self):
        return {self.get_index_key(self.get_prefix(alias)) for alias in [self.name] + self.aliases}

    @staticmethod
    def get_prefix(name: str) -> str:
        """Return prefix that matches the given name or alias.
        """
        return name[0:3]

    @staticmethod
    def get_index_key(text: str) -> str:
        """Return key by which the given test string can be mached.
        """
        return text.lower()

    def __str__(self):
        cls = inspect.getmro(self.__class__)[1]
        return f'{cls.__name__}({self.name})'


class ActionableThing(Thing, ABC):
    def get_action(self, name) -> 'Action':
        return self.actions.lookup(name)

    @property
    @abstractmethod
    def _actions(self):
        return []

    @property
    def actions(self):
        return IndexOfThings(self._actions)


class DescribableThing(Thing):

    @property
    def description(self):
        return None


class ItemContainerThing(Thing, ABC):
    def __init__(self, game, name, aliases=None, items: Iterable['Item']=None):
        super().__init__(game, name, aliases=aliases)
        self.items = IndexOfThings(items or [])

    @property
    def inventory(self):
        return self.items.values()

    def add_item(self, item: 'Item'):
        self.items.add_thing(item)
        return self

    def remove_item(self, item: 'Item'):
        self.items.remove_thing(item)
        return self

    def has_item(self, item: 'Item'):
        return item in self.items.values()

    def has(self, item: 'Item'):
        return self.has_item(item)


class Direction(Thing, ABC):
    def __init__(self, name, aliases=None):
        super().__init__(game=None, name=name, aliases=aliases)
        self.opposite = None

    @classmethod
    def create_dimension(cls, name, opposite_name, aliases=None, opposite_aliases=None):
        direction = cls(name=name, aliases=aliases)
        opposite_direction = cls(name=opposite_name, aliases=opposite_aliases)
        direction.opposite = opposite_direction
        opposite_direction.opposite = direction
        return direction, opposite_direction

    def get_action(self, name):
        raise KeyError()

    def __str__(self):
        return f'{self.__class__.__name__}({self.name})'


class Item(ActionableThing, DescribableThing, ABC):
    def __init__(self, game, name, aliases=None):
        super().__init__(game=game, name=name, aliases=aliases)
        self.is_fixed = False
        self.must_possess = True
        self.must_be_in_location = True


class Place(ItemContainerThing, DescribableThing):
    def __init__(self, game, name, aliases=None, items: Iterable[Item]=None, connections: Iterable['Connection']=None):
        super().__init__(game, name, aliases=aliases)
        self.items = IndexOfThings(items or [])
        self.connections = IndexOfConnections(connections or [])
        self.general_description = None

    def connect_to(self, place: 'Place', direction: Direction, reverse_direction=True):
        self.connections.add_thing(Connection(to_place=place, direction=direction))
        if reverse_direction is True:
            reverse_direction = direction.opposite
        if reverse_direction is not None:
            place.connect_to(self, direction=reverse_direction, reverse_direction=None)

    @property
    def obvious_exits(self) -> Iterable[Direction]:
        return [connection.direction for connection in self.connections.values()]

    def get_exit_destination(self, direction):
        connection = self.connections.get_by_direction(direction)
        if connection is not None:
            return connection.to_place
        return None

    @property
    def description(self):
        description = f'{self.general_description}. You see:'
        for item in self.inventory:
            description += f'\n{item.name}'
        exits_list = ' '.join(direction.name for direction in self.obvious_exits)
        if exits_list == '':
            exits_list = 'None'
        description += '\nObvious exits are: ' + exits_list
        return description


class Connection(Thing):
    def __init__(self, to_place: Place, direction: Direction):
        super().__init__(game=to_place.game, name=to_place.name, aliases=to_place.aliases)
        self.to_place = to_place
        self.direction = direction

    def __str__(self):
        return f'{self.__class__.__name__}({self.to_place},{self.direction})'


class IndexOfConnections(IndexOfThings):

    def get_by_direction(self, direction: Direction):
        for connection in self.values():
            if connection.direction is direction:
                return connection
        return None


class Actor(ItemContainerThing):
    pass


class Player(Actor):
    def __init__(self, game, name, initial_location: Place=None):
        super().__init__(game, name)
        self.location: Place = initial_location

    def get(self, item: 'Item'):
        self.location.remove_item(item)
        return self.add_item(item)

    def drop(self, item: 'Item'):
        self.location.add_item(item)
        return self.remove_item(item)


class ActionError(GameError):
    pass


class ActionOnItemError(ActionError, ThingError):
    pass


class ActionRequiresItemPossessionError(ActionOnItemError):
    def __str__(self):
        return "You don't have it"


class ActionRequiresItemInLocationError(ActionOnItemError):
    def __str__(self):
        return f"I don't see any {self.thing.name}"


class Action(Thing):

    def __init__(self, strategy: Callable[[Player], Result], item: Item=None, aliases=None):
        name = strategy.__name__
        super().__init__(game=None, name=name, aliases=aliases)
        self.count = 0
        self.strategy = strategy
        self.item = item

    def execute(self, player: Player) -> Result:
        self.count += 1
        self.validate_player_can_execute(player)
        return self.strategy(player)

    def validate_player_can_execute(self, player: Player):
        if self.item is not None:
            if self.item.must_possess and not player.has(self.item):
                raise ActionRequiresItemPossessionError(self.item)
            if not self.item.must_possess and self.item.must_be_in_location and not player.location.has(self.item):
                raise ActionRequiresItemInLocationError(self.item)

    def next_action(self) -> 'Action':
        pass