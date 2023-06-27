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
        board_name_to_open = tracker.get_slot("board_name_to_open")
        if board_name_to_open == "":
            dispatcher.utter_message(text="Please specify a board name.")
        else:
            open_board(boardnametoopen=board_name_to_open)
            dispatcher.utter_message(text=f"I have opened board {board_name_to_open}, please check your browser.",)

        return [SlotSet("board_name_to_open", board_name_to_open)]



# This is a Python class that creates a Trello board with a specified name and returns a message
# confirming the creation of the board.
class ActionCreateBoard(Action):
    def name(self) -> Text:
        return "action_create_board"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        board_name_to_create = tracker.get_slot("board_name_to_create")
        add_board(boardnametoadd=board_name_to_create)
        dispatcher.utter_message(text=f"I have created new board {board_name_to_create}, please check your browser.")

        return [SlotSet("board_name_to_create", board_name_to_create)]


# This is a Python class that updates the name of a board and returns a message to the user.
class ActionUpdateBoardName(Action):
    def name(self) -> Text:
        return "action_update_board_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        previous_board_name=tracker.get_slot("previous_board_name")
        new_board_name=tracker.get_slot("new_board_name")
        update_board_name(
            previous_board_name=previous_board_name,
            new_board_name=new_board_name,
        )
        dispatcher.utter_message(text=f"I have updated board name {previous_board_name} to {new_board_name}, please check your browser.")

        return [
            SlotSet("previous_board_name", previous_board_name),
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
        list_name_to_create = tracker.get_slot("list_name_to_create")
        board_name_to_create_list = tracker.get_slot("board_name_to_create_list")
        add_list(boardname=board_name_to_create_list, listname=list_name_to_create)
        dispatcher.utter_message(text=f"I have created new list named {list_name_to_create} in board {board_name_to_create_list}, please check your browser.")

        return [
            SlotSet("list_name_to_create", list_name_to_create),
            SlotSet("board_name_to_create_list", board_name_to_create_list),
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
        new_list_name = tracker.get_slot("new_list_name")
        board_name_to_update_list = tracker.get_slot("board_name_to_update_list")
        update_list_name(boardname=board_name_to_update_list, listname=previous_list_name, newname=new_list_name)
        dispatcher.utter_message(text=f"I have updated the list named {previous_list_name} to {new_list_name} in board {board_name_to_update_list}, please check your browser.")

        return [
            SlotSet("previous_list_name", previous_list_name),
            SlotSet("new_list_name", new_list_name),
            SlotSet("board_name_to_update_list", board_name_to_update_list),
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
        list_name_to_create_card = tracker.get_slot("list_name_to_create_card")
        board_name_to_create_card = tracker.get_slot("board_name_to_create_card")
        add_card(listname=list_name_to_create_card, cardname=card_name_to_create, boardname=board_name_to_create_card)
        dispatcher.utter_message(text=f"I have created the new card named {card_name_to_create} in list {list_name_to_create_card} of board {board_name_to_create_card}, please check your browser.")

        return [
            SlotSet("card_name_to_create", card_name_to_create),
            SlotSet("list_name_to_create_card", list_name_to_create_card),
            SlotSet("board_name_to_create_card", board_name_to_create_card),
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
        previous_card_name = tracker.get_slot("previous_card_name")
        new_card_name = tracker.get_slot("new_card_name")
        list_name_to_update_card = tracker.get_slot("list_name_to_update_card")
        board_name_to_update_card = tracker.get_slot("board_name_to_update_card")

        update_card_name(boardname=board_name_to_update_card, listname=list_name_to_update_card, cardname=previous_card_name, newname=new_card_name)

        dispatcher.utter_message(text=f"I have updated card named {previous_card_name} to {new_card_name} in list {list_name_to_update_card} of board {board_name_to_update_card}, please check your browser.")

        return [
            SlotSet("previous_card_name", previous_card_name),
            SlotSet("new_card_name", new_card_name),
            SlotSet("list_name_to_update_card", list_name_to_update_card),
            SlotSet("board_name_to_update_card", board_name_to_update_card),
        ]