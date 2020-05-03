from game.text.things import Place


class EntranceHall(Place):

    def __init__(self, game, items=None):
        super().__init__(game, 'Entrance Hall', items=items)
        self.general_description = 'A dark and spooky entrance hall...'


class Library(Place):

    def __init__(self, game, items=None):
        super().__init__(game, 'Library', items=items)
