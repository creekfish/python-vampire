import re
from typing import Tuple

from game.text.things import Thing, Action, IndexOfThings, ThingError


class SimplePhrase:

    def __init__(self, text_input):
        super().__init__()
        self.terms = re.split('\s+', text_input)

    @property
    def verb(self):
        try:
            return self.terms[0]
        except IndexError:
            return None

    @property
    def object(self):
        try:
            if len(self.terms) > 1:
                return self.terms[-1]
            return None
        except IndexError:
            return None

    def __str__(self):
        return f'{self.__class__}: {self.verb}, {self.object}'


class GrammarError(Exception):
    pass


class GrammarVerbIsMissingError(GrammarError):
    pass


class GrammarUnknownActionError(GrammarError):
    pass


class GrammarUnknownThingError(GrammarError):
    pass


class GrammarUnknownActionForThingError(GrammarError, ThingError):
    pass


class SimpleGrammar:


#TODO: things must include all places, items, directions - all things that have associated actions

#TODO: raw_actions includes all actions the game has without objects... plus all direction shortcuts!

    def __init__(self, things: [Thing], raw_actions: [Action]):
        super().__init__()
        self.things_by_name = IndexOfThings(things)
#TODO: need to account for aliases of things and index by those too...
        self.raw_actions_by_verb = IndexOfThings(raw_actions)

    @property
    def is_parsed(self):
        return self.verb is not None

    def parse(self, text_input: str) -> Tuple[Action, Thing or None]:
        """ Parse the given text input and return a tuple of action and thing.
        """
        text_input = text_input.lower().strip()
        phrase = SimplePhrase(text_input)
        if phrase.verb is None:
            raise GrammarVerbIsMissingError()
        if phrase.object is None:
            try:
                action = self.raw_actions_by_verb.lookup(phrase.verb)
            except KeyError:
                raise GrammarUnknownActionError()
            return action, None
        else:
            try:
                thing = self.things_by_name.lookup(phrase.object)
            except KeyError:
                raise GrammarUnknownThingError()
            try:
                action = thing.get_action(phrase.verb)
            except KeyError:
                raise GrammarUnknownActionForThingError(thing)
            return action, thing
