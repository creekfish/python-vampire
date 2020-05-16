from unittest.mock import Mock

from game.text.things import Item, Player
from game.text.actions import LookAction, GetAction, DropAction, InventoryAction
from tests import GameTestCase


class TestLookAtItemAction(GameTestCase):

    def setUp(self):
        super().setUp()
        self.player_mock: Player = Mock()
        self.item_mock: Item = Mock()
        self.item_mock.name = 'Cthulhu'
        self.item_mock.description = 'A color out of space'
        self.action = LookAction(item=self.item_mock)

    def test__execute__returns_description_of_player_location__when_no_item_is_specified(self):
        self.player_mock.location.description = 'A faraway place'
        self.assertEqual('A faraway place', str(LookAction(item=None).execute(player=self.player_mock)))

    def test__execute__returns_description_of_item__when_possession_not_required_and_item_in_player_location(self):
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = True
        self.assertEqual('A color out of space', str(self.action.execute(player=self.player_mock)))

    def test__execute__returns_you_see_nothing_special__when_item_description_is_none(self):
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = True
        self.item_mock.description = None
        self.assertEqual('You see nothing special', str(self.action.execute(player=self.player_mock)))

    def test__execute__raises_message_i_dont_see_any__when_possession_not_required_and_item_not_in_player_location(self):
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = False
        self.assertRaisesWithMessage("I don't see any Cthulhu", self.action.execute, player=self.player_mock)

    def test__execute__returns_description_of_item__when_possession_required_and_item_possessed_by_player(self):
        self.item_mock.must_possess = True
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = True
        self.player_mock.location.has.return_value = False
        self.assertEqual('A color out of space', str(self.action.execute(player=self.player_mock)))

    def test__execute__raises_message_you_dont_have_it__when_possession_not_required_and_item_not_possessed_by_player(self):
        self.item_mock.must_possess = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = False
        self.assertRaisesWithMessage("You don't have it", self.action.execute, player=self.player_mock)

    def test__execute__returns_description_of_item__when_location_not_required_and_item_in_player_location(self):
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = False
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = True
        self.assertEqual('A color out of space', str(self.action.execute(player=self.player_mock)))


class TestGetAction(GameTestCase):

    def setUp(self):
        super().setUp()
        self.player_mock: Player = Mock()
        self.item_mock: Item = Mock()
        self.item_mock.name = 'Widget'
        self.action = GetAction(item=self.item_mock)

    def test__execute__returns_message_got_the_item__when_item_is_in_player_location_and_movable(self):
        self.item_mock.is_fixed = False
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = True
        self.assertEqual('OK, you got the Widget', str(self.action.execute(player=self.player_mock)))

    def test__execute__returns_message_got_the_item__when_item_not_required_to_be_and_not_in_player_location(self):
        self.item_mock.is_fixed = False
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = False
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = False
        self.assertEqual('OK, you got the Widget', str(self.action.execute(player=self.player_mock)))

    def test__execute__raises_message_i_dont_see_any__when_item_is_not_in_player_location(self):
        self.item_mock.is_fixed = False
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = False
        self.assertRaisesWithMessage("I don't see any Widget", self.action.execute, player=self.player_mock)

    def test__execute__raises_message_you_cant_get_it__when_item_is_fixed_in_place(self):
        self.item_mock.is_fixed = True
        self.item_mock.must_possess = False
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = True
        self.assertRaisesWithMessage("You can't get it", self.action.execute, player=self.player_mock)

    def test__execute__raises_message_i_dont_see_any__when_item_must_be_possessed_and_player_has_it(self):
        self.item_mock.is_fixed = False
        self.item_mock.must_possess = True
        self.item_mock.must_be_in_location = True
        self.player_mock.has.return_value = True
        self.player_mock.location.has.return_value = False
        self.assertRaisesWithMessage("I don't see any Widget", self.action.execute, player=self.player_mock)

    def test__execute__gets_item_for_player(self):
        self.item_mock.is_fixed = False
        self.player_mock.has.return_value = False
        self.action.execute(player=self.player_mock)
        self.player_mock.get.assert_called_once_with(self.item_mock)


class TestDropAction(GameTestCase):

    def setUp(self):
        super().setUp()
        self.player_mock: Player = Mock()
        self.item_mock: Item = Mock()
        self.item_mock.name = 'Widget'
        self.action = DropAction(item=self.item_mock)

    def test__execute__returns_message_item_on_floor__when_item_is_in_player_possession(self):
        self.player_mock.has.return_value = True
        self.player_mock.location.has.return_value = False
        self.player_mock.location.name = 'Smoking Room'
        self.assertEqual('The Widget is on the Smoking Room floor', str(self.action.execute(player=self.player_mock)))

    def test__execute__raises_message_you_dont_have_it__when_item_is_in_player_possession(self):
        self.item_mock.must_possess = False
        self.player_mock.has.return_value = False
        self.player_mock.location.has.return_value = True
        self.assertRaisesWithMessage("You don't have it", self.action.execute, player=self.player_mock)


class TestInventoryAction(GameTestCase):

    def setUp(self):
        super().setUp()
        self.player_mock: Player = Mock()
        self.action = InventoryAction()

    def test__execute__returns_message_carrying_nothing__when_player_has_no_items(self):
        self.player_mock.inventory = []
        self.assertEqual('You are carrying: nothing', str(self.action.execute(player=self.player_mock)))

    def test__execute__message_carrying_single_item__when_player_has_single_items(self):
        mock_item1 = Mock()
        mock_item1.name = 'Whistling Birds'
        self.player_mock.inventory = [mock_item1]
        self.assertEqual('You are carrying: Whistling Birds', str(self.action.execute(player=self.player_mock)))

    def test__execute__message_carrying_list_of_items__when_player_has_multiple_items(self):
        mock_item1 = Mock()
        mock_item1.name = 'Flamethrower'
        mock_item2 = Mock()
        mock_item2.name = 'Beskar Steel'
        self.player_mock.inventory = [mock_item1, mock_item2]
        self.assertEqual('You are carrying: Flamethrower, Beskar Steel', str(self.action.execute(player=self.player_mock)))
