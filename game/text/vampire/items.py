from abc import ABC

from game.text.things import Item, Result, Action
from game.text.actions import LookAction, GetAction, DropAction


class VampireItem(Item, ABC):

    @property
    def _actions(self):
        item_actions = [
            LookAction(item=self),
            GetAction(item=self),
            DropAction(item=self),
        ]
        return super()._actions + item_actions


class Sign(VampireItem):

    def __init__(self, game):
        super().__init__(game, 'Sign')
        self.is_fixed = True
        self.must_possess = False
        self.must_be_in_location = False     #NOTE: this represents a bug in the original game!

    @property
    def description(self):
        return 'The Vampire Wakes at Midnight!'


class Timepiece(VampireItem):

    def __init__(self, game):
        super().__init__(game, 'Timepiece')

    @property
    def description(self):
        return f'The time is {self.game.time}.'


class WoodenStakes(VampireItem):

    def __init__(self, game):
        super().__init__(game, 'Wooden Stakes', ['Stakes'])

    @property
    def description(self):
#TODO: should items default to description == the name of the item...?  Is that how it is in the game?
        return f'Wooden Stakes'


class BrickFireplace(VampireItem):

    def __init__(self, game):
        super().__init__(game, 'Brick Fireplace')
        self.is_fixed = True
        self.must_possess = False

    @property
    def _actions(self):

        def hit_with(player, item):
            if player.location.has(self):
                if item.name == 'Axe' and player.has(item) and not self.game.has_item('Wooden Stakes'):
                    player.location.add_item(WoodenStakes(self.game))
                    player.location.remove_item(self)
                    return Result(player.location.do('look'))
                return Result('Nothing happened\n')
            return Result("I don't see any Fireplace")

        def hit(player):
            if player.location.has(self):
                return Result('      -- With what? ', next_action=Action(hit_with))
            else:
                return Result("I don't see any Crate")

        return super()._actions + [
            Action(hit),
        ]


class Crate(VampireItem):

    def __init__(self, game):
        super().__init__(game, 'Crate')

    @property
    def description(self):
        return f'A wooden crate.'

    @property
    def _actions(self):

        def hit_with(player, item):
            if player.location.has(self):
                if item.name == 'Axe' and player.has(item) and not self.game.has_item('Wooden Stakes'):
                    player.location.add_item(WoodenStakes(self.game))
                    player.location.remove_item(self)
                    return Result(player.location.do('look'))
                return Result('Nothing happened\n')
            return Result("I don't see any Crate")

        def hit(player):
            if player.location.has(self):
                return Result('      -- With what? ', next_action=Action(hit_with))
            else:
                return Result("I don't see any Crate")

        return super()._actions + [
            Action(hit),
        ]





