
class TextGameSinglePlayer:

    def __init__(self, places, items, directions):
        super().__init__()
        self.is_started = True
        self.is_ended = False
        self.is_won = False
        self.turns = 0
        self.player = None
        self.place_by_name = IndexOfThings(places)
        self.direction_by_name = IndexOfThings(directions)
        self.item_by_name = IndexOfThings(items)
        self.grammar = SimpleGrammar()
        self.continued_action = None

    def set_default_actions(self):
        def execute_look(actor: Actor)
            self.increment_count()   # no limit on how many times this can be executed
            return ResultGeneric(success=True, self.get_player().get_location().get_inital_action('look').execute(actor).get_message())
        self.add_action(ActionInitial('look', execute_look))
        def execute_read(actor: Actor)
            return self.get_inital_action('look').execute(actor)
        self.add_action(ActionInitial('read', execute_read))
        def execute_inventory()
            self.increment_count()   # no limit on how many times this can be executed
            return ResultGeneric(success=True, self.get_player().basket_contents_look())
        self.add_action(ActionInitial('inventory', execute_inventory))

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
        if self.continued_action is not None or self.grammar.parse(text_input):
            if self.continued_action is None:
                result = self.grammar.verb.execute(self.player)
            else:
                result = self.continued_action.execute(self.player, text_input)
            if result.is_partial:
                self.continued_action = result.get_continued_action()
            if result is not None:
                return result
#TODO: raise exception here instead?
            return ResultGeneric(False, 'ERROR: Action failed to produce a result!')
        else:
            if self.grammar.object is not None:
#TODO: raise exception here instead?
                return ResultGeneric(False, "I don't know how to do that.")
            else:
#TODO: need to check against entire vocabulary! and output things as exceptions like:
#     * I don't know that word (known verb, unknown object),
#     * I don't know how to do that (unknown verb, known object)
#     * You can't do that, etc.)
                return ResultGeneric(False, "I don't know that word.")

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
