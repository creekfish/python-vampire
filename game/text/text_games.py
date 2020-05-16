from typing import List

from game.text.grammars import (
    GrammarUnknownActionForThingError,
    GrammarVerbIsMissingError,
    GrammarUnknownActionError,
    GrammarUnknownThingError,
)
from game.text.things import Action, Actor, Player, GameError
from game.text.actions import LookAction, InventoryAction, GoAction
from game.text.vampire.directions import all_directions


class GameNoInputError(GameError):
    def __str__(self):
        return ''


class GameUnknownObjectError(GameError):
    def __str__(self):
        return "I don't know that word."


class GameUnknownActionError(GameError):
    def __str__(self):
        return "I don't know how to do that."


class TextGameSinglePlayer:

    def __init__(self, name, grammar):
        super().__init__()
        self.name = name
        self.grammar = grammar
        self.is_started = True
        self.is_ended = False
        self.is_won = False
        self.turns = 0
        self.player = Player(game=self, name='Player 1')
        self.player.location = self.starting_location
        self.continued_action = None

    @property
    def starting_location(self):
        return None

    def set_default_actions(self):
        def execute_look(actor: Actor):
            self.increment_count()   # no limit on how many times this can be executed
#            return ResultSuccess(self.player.location.get_inital_action('look').execute(actor).get_message())
        self.add_action(Action('look', execute_look))
        def execute_read(actor: Actor):
            return self.get_inital_action('look').execute(actor)
        self.add_action(Action('read', execute_read))
        def execute_inventory():
            self.increment_count()   # no limit on how many times this can be executed
#            return ResultSuccess(self.player.basket_contents_look())
        self.add_action(Action('inventory', execute_inventory))

    def initialize(self):
        """Initialize all of the game objects and configuration.
        """
        self.is_started = True
        self.is_ended = False
        self.is_won = False
        self.turns = 0

    def start_turn(self):
        return not self.is_ended

    def take_turn(self, text_input):
        try:
            action, object = self.grammar.parse(text_input)
            result = action.execute(self.player)
        except GrammarVerbIsMissingError:
            raise GameNoInputError()
        except GrammarUnknownThingError:
            raise GameUnknownObjectError()
        except (GrammarUnknownActionError, GrammarUnknownActionForThingError):
            raise GameUnknownActionError()
        return result

        # if self.continued_action is not None or self.grammar.parse(text_input):
        #     if self.continued_action is None:
        #         result = self.grammar.verb.execute(self.player)
        #     else:
        #         result = self.continued_action.execute(self.player, text_input)
        #     if result.is_partial:
        #         self.continued_action = result.get_continued_action()
        #     if result is not None:
        #         return result
        #     # TODO: raise exception here instead?
        #     return ResultFailure('ERROR: Action failed to produce a result!')
        # else:
        #     if object is not None:
        #         # TODO: raise exception here instead?
        #         return ResultFailure("I don't know how to do that.")
        #     else:
        #         # TODO: need to check against entire vocabulary! and output things as exceptions like:
        #         #     * I don't know that word (known verb, unknown object),
        #         #     * I don't know how to do that (unknown verb, known object)
        #         #     * You can't do that, etc.)
        #         return ResultFailure("I don't know that word.")

#     def take_turn_old(self, text_input):
#         if self.continued_action is not None or self.grammar.parse(text_input):
#             if self.continued_action is None:
#                 result = self.grammar.verb.execute(self.player)
#             else:
#                 result = self.continued_action.execute(self.player, text_input)
#             if result.is_partial:
#                 self.continued_action = result.get_continued_action()
#             if result is not None:
#                 return result
# #TODO: raise exception here instead?
#             return ResultFailure('ERROR: Action failed to produce a result!')
#         else:
#             if self.grammar.object is not None:
# #TODO: raise exception here instead?
#                 return ResultFailure("I don't know how to do that.")
#             else:
# #TODO: need to check against entire vocabulary! and output things as exceptions like:
# #     * I don't know that word (known verb, unknown object),
# #     * I don't know how to do that (unknown verb, known object)
# #     * You can't do that, etc.)
#                 return ResultFailure("I don't know that word.")

    def end_turn(self):
        if self.continued_action is None:
            # completes a turn if the action is not being continued, getting more input
            self.turns += 1
        return not self.is_ended

    def end(self, is_won):
        self.is_ended = True
        self.is_won = is_won

#TODO: shouldn't this shit be in the grammar?  The game just has a list of directions... and it passes to the grammar
#TODO: or better  yet, the grammar should be constructed with all actions, directions, items, and places for a game and injected as the game grammar...!!!
    def match_direction(self, name):
        return self.direction_by_name[name]

    def match_item(self, name):
        return self.item_by_name[name]

    def match_place(self, name):
        return self.place_by_name[name]

    @property
    def game_actions(self) -> List[Action]:
        game_actions = [
            LookAction(),
            InventoryAction(),
        ]
        game_actions.extend(self.get_direction_actions())
        return game_actions

    @staticmethod
    def get_direction_actions():
        def east(player):
            return GoAction(direction=all_directions.lookup('east')).execute(player=player)

        def west(player):
            return GoAction(direction=all_directions.lookup('west')).execute(player=player)

        def north(player):
            return GoAction(direction=all_directions.lookup('north')).execute(player=player)

        def south(player):
            return GoAction(direction=all_directions.lookup('south')).execute(player=player)

        def up(player):
            return GoAction(direction=all_directions.lookup('up')).execute(player=player)

        def down(player):
            return GoAction(direction=all_directions.lookup('down')).execute(player=player)

        direction_actions = [
            Action(east, aliases=['e']),
            Action(west, aliases=['w']),
            Action(north, aliases=['n']),
            Action(south, aliases=['s']),
            Action(up, aliases=['u']),
            Action(down, aliases=['d']),
        ]
        return direction_actions
