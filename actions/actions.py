from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.board_functions import (
    add_board,
    open_board,
    open_trello,
    update_board_name,
)
from actions.card_functions import add_card, update_card_name
from actions.list_functions import add_list, update_list_name


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello Dude!")

        return []


class ActionOpenTrello(Action):
    def name(self) -> Text:
        return "action_open_trello"

    async def run(self, dispatcher, tracker, domain):
        query = tracker.get_slot("query")
        open_trello()
        dispatcher.utter_message(text="Opened trello, please check your browser.")
        return [SlotSet("query", query)]


class ActionOpenBoard(Action):
    def name(self) -> Text:
        return "action_open_board"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        board_name = tracker.get_slot("open_board_name")
        open_board(boardnametoopen=board_name)
        dispatcher.utter_message(
            text=f"I have opened board {board_name}, please check your browser.",
        )

        return [SlotSet("open_board_name", board_name)]


class ActionCreateBoard(Action):
    def name(self) -> Text:
        return "action_create_board"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        board_name = tracker.get_slot("board_create_name")
        add_board(boardnametoadd=board_name)
        dispatcher.utter_message(
            text=f"I have created new board {board_name}, please check your browser."
        )

        return [SlotSet("board_create_name", board_name)]


class ActionUpdateBoardName(Action):
    def name(self) -> Text:
        return "action_update_board_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        previous_board_name = tracker.get_slot("old_board_name")
        new_board_name = tracker.get_slot("new_board_name")
        update_board_name(
            previous_board_name=previous_board_name,
            new_board_name=new_board_name,
        )
        dispatcher.utter_message(
            text=f"I have updated board name {previous_board_name} to {new_board_name}, please check your browser."
        )

        return [
            SlotSet("old_board_name", previous_board_name),
            SlotSet("new_board_name", new_board_name),
        ]


class ActionCreateList(Action):
    def name(self) -> Text:
        return "action_create_list"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        list_name = tracker.get_slot("list_name_create")
        board_name = tracker.get_slot("name_of_board_for_list")
        add_list(listname=list_name, boardname=board_name)
        dispatcher.utter_message(
            text=f"I have created new list named {list_name} in board {board_name}, please check your browser."
        )

        return [
            SlotSet("list_name_create", list_name),
            SlotSet("name_of_board_for_list", board_name),
        ]


class ActionUpdateListName(Action):
    def name(self) -> Text:
        return "action_update_list_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        previous_list_name = tracker.get_slot("previous_list_name")
        fresh_list_name = tracker.get_slot("fresh_list_name")
        board_name = tracker.get_slot("of_board_list_name_update")
        update_list_name(
            previous_list_name=previous_list_name,
            fresh_list_name=fresh_list_name,
            boardname=board_name,
        )
        dispatcher.utter_message(
            text=f"I have updated the list named {previous_list_name} to {fresh_list_name} in board {board_name}, please check your browser."
        )

        return [
            SlotSet("previous_list_name", previous_list_name),
            SlotSet("fresh_list_name", fresh_list_name),
            SlotSet("of_board_list_name_update", board_name),
        ]


class ActionCreateCard(Action):
    def name(self) -> Text:
        return "action_create_card"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        card_name_to_create = tracker.get_slot("card_name_to_create")
        list_name = tracker.get_slot("add_card_to_list_name")
        board_name = tracker.get_slot("to_add_card_board_name")
        add_card(cardname=card_name_to_create, listname=list_name, boardname=board_name)
        dispatcher.utter_message(
            text=f"I have created the new card named {card_name_to_create} in list {list_name} of board {board_name}, please check your browser."
        )

        return [
            SlotSet("card_name_to_create", card_name_to_create),
            SlotSet("add_card_to_list_name", list_name),
            SlotSet("to_add_card_board_name", board_name),
        ]


class ActionUpdateCardName(Action):
    def name(self) -> Text:
        return "action_update_card_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        previous_card_name = tracker.get_slot("former_card_name")
        new_card_name = tracker.get_slot("latter_card_name")
        list_name = tracker.get_slot("update_card_name_list")
        board_name = tracker.get_slot("rename_card_for_board")

        update_card_name(
            previous_card_name=previous_card_name,
            new_card_name=new_card_name,
            listname=list_name,
            boardname=board_name,
        )

        dispatcher.utter_message(
            text=f"I have updated card named {previous_card_name} to {new_card_name} in list {list_name} of board {board_name}, please check your browser."
        )

        return [
            SlotSet("former_card_name", previous_card_name),
            SlotSet("latter_card_name", new_card_name),
            SlotSet("update_card_name_list", list_name),
            SlotSet("rename_card_for_board", board_name),
        ]
