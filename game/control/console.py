import sys

from game.text.results import ResultSuccess
from game.text.text_games import GameError
from game.text.vampire.game_controller import Vampire


class Console:
    def __init__(self, game):
        self.text_game = game

    def start(self):
        self.restart()
        is_running = True
        while is_running:
            self.event_loop()
            self.output('\n\nWould you like to try again? ')
            choice = self.input(first_letter=True)
            if choice == 'y':
                self.restart()
            elif choice == 'r':
                game.reset_ended()
            else:
                is_running = False

    def restart(self):
        self.text_game.initialize()
        self.output(self.text_game.welcome())
        choice = self.input(first_letter=True)
        if choice == 'y':
            self.output(self.text_game.instructions())
        self.output('\n\n' + str(self.text_game.take_turn('look')))

    def end(self):
        self.text_game.end(False)
        self.output('\nGame suddenly ended by mysterious external forces. Goodbye.')

    def event_loop(self):
        while not self.text_game.is_ended:
            self.output('\n\nWhat do you want to do? ')
            text = self.input()
            if self.controller_action(text):
                self.text_game.start_turn()
                try:
                    result = self.text_game.take_turn(text)
                    self.output('\n' + str(result))
                except GameError as thing_error:
                    self.output('\n' + str(thing_error))

    def controller_action(self, text: str):
        if text.startswith('quit'):
            self.output('\nAre you sure you want to quit and exit the game (y or n)? ')
            choice = self.input(first_letter=True)
            if choice == 'y':
                self.end()
                return False
            else:
                self.output("\nOK, let's keep exploring!\n")
        return True

    def output(self, message):
        print(message, end='')

    def input(self, first_letter=False):
        text = str(input()).lower()
        if text != '' and first_letter:
            text = text[0]
        return text


if __name__ == "__main__":

    args = sys.argv
    game = None

    if len(args) < 0:
        print('Usage: python -m game.control.console name_of_game')
        sys.exit(1)
    if 'vampire' in args[0]:
        game = Vampire()
    else:
        print(f'Unknown game {args[0]}. Valid games are: vampire')
        sys.exit(1)

    controller = Console(game=game)
    controller.start()
    sys.exit(0)
