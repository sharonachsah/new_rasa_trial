from typing import Any, Text, Dict, List
import webbrowser

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions.board_functions import *

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello Dude!")

        return []

class ActionOpenTrello(Action):

    def name(self) -> Text:
        return "action_open_trello"

    def run(self, dispatcher, tracker, domain):
        query = tracker.get_slot("query")
        open_trello()
        dispatcher.utter_message(text=f"Opened trello, please check your browser.")
        return [SlotSet("query", query)]

class ActionOpenBoard(Action):

    def name(self) -> Text:
        return "action_open_board"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.get_slot("board_name")
        open_board(board_name=query)
        dispatcher.utter_message(text=f"Opened board, please check your browser.") 

        return [SlotSet("board_name", query)]