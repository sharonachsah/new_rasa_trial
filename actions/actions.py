""" This file contains all the custom actions that are used in the chatbot."""
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.board_functions import open_board, open_trello, add_board


class ActionHelloWorld(Action):
    """This is a custom action to say hello to the user"""

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
    """This is a custom action to open trello in the browser"""

    def name(self) -> Text:
        return "action_open_trello"

    async def run(self, dispatcher, tracker, domain):
        query = tracker.get_slot("query")
        open_trello()
        dispatcher.utter_message(text="Opened trello, please check your browser.")
        return [SlotSet("query", query)]


class ActionOpenBoard(Action):
    """This is a custom action to open a board in the browser"""

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
        print(entity_value)
        open_board(boardnametoopen=entity_value)
        dispatcher.utter_message(text="Opened board, please check your browser.")

        return [SlotSet("board_name_to_open", entity_value)]

class ActionCreateBoard(Action):
    """This is a custom action to open a board in the browser"""

    def name(self) -> Text:
        return "action_create_board"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # query = tracker.get_slot("board_name")
        # entity_value = next(tracker.get_latest_entity_values("board_name"), None)
        entity_value = tracker.get_slot("board_name_to_create")
        print(entity_value)
        add_board(boardnametoadd=entity_value)
        dispatcher.utter_message(text="Created new board, please check your browser.")

        return [SlotSet("board_name_to_create", entity_value)]