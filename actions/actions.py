""" This file contains all the custom actions that are used in the chatbot."""
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
from actions.list_functions import add_list, update_list_name
from actions.card_functions import add_card, update_card_name


# This is a Python class that defines an action called "action_hello_world" which sends a message
# "Hello Dude!" to the user.
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


# This is a Python class that defines an action to open Trello and sends a message to the user
# confirming that Trello has been opened.
class ActionOpenTrello(Action):
    def name(self) -> Text:
        return "action_open_trello"

    async def run(self, dispatcher, tracker, domain):
        query = tracker.get_slot("query")
        open_trello()
        dispatcher.utter_message(text="Opened trello, please check your browser.")
        return [SlotSet("query", query)]


# This is a Python class that defines an action to open a board and return a message to the user.
class ActionOpenBoard(Action):
    def name(self) -> Text:
        return "action_open_board"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # query = tracker.get_slot("board_name")
        # entity_value = next(tracker.get_latest_entity_values("board_name"), None)
        entity_value = tracker.get_slot("board_name_to_open")
        # print(entity_value)
        open_board(boardnametoopen=entity_value)
        dispatcher.utter_message(text="Opened board, please check your browser.")

        return [SlotSet("board_name_to_open", entity_value)]


# This is a Python class that creates a Trello board and returns a message to the user.
class ActionCreateBoard(Action):
    def name(self) -> Text:
        return "action_create_board"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        entity_value = tracker.get_slot("board_name_to_create")
        # print(entity_value)
        add_board(boardnametoadd=entity_value)
        dispatcher.utter_message(text="Created new board, please check your browser.")

        return [SlotSet("board_name_to_create", entity_value)]


# This is a Python class that updates the name of a board and returns a message to the user.
class ActionUpdateBoardName(Action):
    def name(self) -> Text:
        return "action_update_board_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        update_board_name(
            prev_board_name=tracker.get_slot("previous_board_name"),
            new_board_name=tracker.get_slot("new_board_name"),
        )
        dispatcher.utter_message(text="Updated board, please check your browser.")

        return [
            SlotSet("previous_board_name", tracker.get_slot("previous_board_name")),
            SlotSet("new_board_name", tracker.get_slot("new_board_name")),
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
        entity_value = tracker.get_slot("list_name_to_create")
        entity_value1 = tracker.get_slot("board_name_to_create_list")
        add_list(boardname=entity_value1, listname=entity_value)
        dispatcher.utter_message(text="Created new list, please check your browser.")

        return [
            SlotSet("list_name_to_create", entity_value),
            SlotSet("board_name_to_create_list", entity_value1),
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
        entity_value = tracker.get_slot("list_name_to_update")
        entity_value1 = tracker.get_slot("board_name_to_update_list")
        entity_value2 = tracker.get_slot("new_list_name")
        update_list_name(boardname=entity_value1, listname=entity_value, newname=entity_value2)
        dispatcher.utter_message(text="Updated list, please check your browser.")

        return [
            SlotSet("list_name_to_update", entity_value),
            SlotSet("board_name_to_update_list", entity_value1),
            SlotSet("new_list_name", entity_value2),
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
        entity_value = tracker.get_slot("card_name_to_create")
        entity_value1 = tracker.get_slot("list_name_to_create_card")
        add_card(listname=entity_value1, cardname=entity_value)
        dispatcher.utter_message(text="Created new card, please check your browser.")

        return [
            SlotSet("card_name_to_create", entity_value),
            SlotSet("list_name_to_create_card", entity_value1),
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
        entity_value = tracker.get_slot("card_name_to_update")
        entity_value1 = tracker.get_slot("list_name_to_update_card")
        entity_value2 = tracker.get_slot("new_card_name")
        entity_value3 = tracker.get_slot("board_name_to_update_card")
        update_card_name(boardname=entity_value3, listname=entity_value1, cardname=entity_value, newname=entity_value2)
        dispatcher.utter_message(text="Updated card, please check your browser.")

        return [
            SlotSet("card_name_to_update", entity_value),
            SlotSet("list_name_to_update_card", entity_value1),
            SlotSet("new_card_name", entity_value2),
        ]