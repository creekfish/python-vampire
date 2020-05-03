import unittest
from unittest.mock import Mock

from game.text.things import Action, Item, Player, Place


class GameTestCase(unittest.TestCase):

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            self.assertEqual(msg, str(e))
        else:
            assert False, f'No exception raised by {func}'

    def _get_player_mock(self) -> Player:
        player_mock: Player = Mock()
        player_mock.has.return_value = False
        player_mock.location = self._get_place_mock()
        return player_mock

    def _get_place_mock(self) -> Place:
        place_mock: Place = Mock()
        place_mock.name = 'Klaatu Nebula'
        place_mock.description = 'Peaceful Thermian homeworld'
        place_mock.has.return_value = True
        return place_mock

    def _get_item_mock(self) -> Item:
        item_mock: Item = Mock()
        item_mock.name = 'Widget'
        item_mock.description = 'A color out of space'
        item_mock.is_fixed = False
        item_mock.must_possess = True
        item_mock.must_be_in_location = True
        return item_mock
