""" This file contains all the custom actions that are used in the chatbot."""
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.board_functions import (
    open_board,
    open_trello,
    add_board,
    update_board_name,
)
from actions.speechtotext import recognize_speech


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
        # print(entity_value)
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
        # print(entity_value)
        add_board(boardnametoadd=entity_value)
        dispatcher.utter_message(text="Created new board, please check your browser.")

        return [SlotSet("board_name_to_create", entity_value)]


class ActionUpdateBoardName(Action):
    """This is a custom action to open a board in the browser"""

    def name(self) -> Text:
        return "action_update_board_name"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # query = tracker.get_slot("board_name")
        # entity_value = next(tracker.get_latest_entity_values("board_name"), None
        # print(entity_value)
        update_board_name(
            prev_board_name=tracker.get_slot("previous_board_name"),
            new_board_name=tracker.get_slot("new_board_name"),
        )
        dispatcher.utter_message(text="Updated board, please check your browser.")

        return [
            SlotSet("previous_board_name", tracker.get_slot("previous_board_name")),
            SlotSet("new_board_name", tracker.get_slot("new_board_name")),
        ]


class ActionTakeVoiceInput(Action):
    def name(self) -> Text:
        return "action_take_voice_input"
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(text="Please speak now...")
        recognize_speech(audio_model="C:/new_rasa_trial/whisper_models/base.en.pt")
        speech = recognize_speech.transcription = []
        print(speech)
        dispatcher.utter_message(
            text=f'You said: {tracker.get_slot("user_voice_input")}'
        )
        return [
            SlotSet("user_voice_input", tracker.get_slot("user_voice_input")),
        ]
    
# recognize_speech(audio_model="C:/new_rasa_trial/whisper_models/base.en.pt")