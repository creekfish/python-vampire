from game.text.things import (
    Action,
    ActionError,
    ActionOnItemError,
    ActionRequiresItemInLocationError,
    ActionRequiresItemPossessionError,
    Direction,
    Item,
    Player,
    Result,
)


class GetActionItemIsFixedInPlace(ActionOnItemError):
    def __str__(self):
        return "You can't get it"


class GoActionItemNoConnectionToDestination(ActionError):
    def __str__(self):
        return "You can't go there"


class LookAction(Action):

    def __init__(self, item: Item=None):
        def look(player: Player) -> Result:
            if item is None:
                description = player.location.description
            else:
                description = item.description
            return Result(description)
        super().__init__(strategy=look, item=item, aliases=['read'])


class GetAction(Action):

    def __init__(self, item: Item):
        def get(player: Player) -> Result:
            player.get(item)
            return Result(f'OK, you got the {item.name}')
        super().__init__(strategy=get, item=item)

    def validate_player_can_execute(self, player: Player):
        if player.has(self.item):
            raise ActionRequiresItemInLocationError(self.item)
        try:
            super().validate_player_can_execute(player)
        except ActionRequiresItemPossessionError:
            pass
        if self.item.is_fixed:
            raise GetActionItemIsFixedInPlace(self.item)


class DropAction(Action):

    def __init__(self, item: Item):
        def drop(player: Player) -> Result:
            player.drop(item)
            return Result(f'The {item.name} is on the {player.location.name} floor')
        super().__init__(strategy=drop, item=item)

    def validate_player_can_execute(self, player: Player):
        if not player.has(self.item):
            raise ActionRequiresItemPossessionError(self.item)
        super().validate_player_can_execute(player)


class InventoryAction(Action):

    def __init__(self):
        def inventory(player: Player) -> Result:
            inventory_list = ', '.join(item.name for item in player.inventory)
            if inventory_list == '':
                inventory_list = 'nothing'
            return Result(f'You are carrying: {inventory_list}')
        super().__init__(strategy=inventory, item=None)


class GoAction(Action):

    def __init__(self, direction: Direction):
        def go(player: Player) -> Result:
            destination = player.location.get_exit_destination(direction)
            if destination is not None:
                player.location = player.location.get_exit_destination(direction)
#TODO: next action is Look... or just hardcode that here?
                return LookAction().execute(player=player)
            else:
                raise GoActionItemNoConnectionToDestination()
        super().__init__(strategy=go, item=None)
