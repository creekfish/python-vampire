from typing import Callable

from game.text.things import (
    Thing,
    Item,
    Player,
    Result,
    ThingError,
)


class ActionError(ThingError):
    pass


class ActionRequiresItemPossessionError(ActionError):
    def __str__(self):
        return "You don't have it"


class ActionRequiresItemInLocationError(ActionError):
    def __str__(self):
        return f"I don't see any {self.thing.name}"


class GetActionItemIsFixedInPlace(ActionError):
    def __str__(self):
        return "You can't get it"


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
            if type(self) is not GetAction and self.item.must_possess and not player.has(self.item):
                raise ActionRequiresItemPossessionError(self.item)
            if not self.item.must_possess and self.item.must_be_in_location and not player.location.has(self.item):
                raise ActionRequiresItemInLocationError(self.item)

    def next_action(self) -> 'Action':
        pass


class LookAction(Action):

    def __init__(self, item: Item):
        def look(player: Player) -> Result:
            return Result(item.description)
        super().__init__(strategy=look, item=item, aliases=['read'])


class GetAction(Action):

    def __init__(self, item: Item):
        def get(player: Player) -> Result:
            player.location.remove_item(item)
            player.get(item)
            return Result(f'OK, you got the {item.name}')
        super().__init__(strategy=get, item=item)

    def validate_player_can_execute(self, player: Player):
        if player.has(self.item):
            raise ActionRequiresItemInLocationError(self.item)
        super().validate_player_can_execute(player)
        if self.item.is_fixed:
            raise GetActionItemIsFixedInPlace(self.item)
