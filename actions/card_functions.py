"""
This file contains functions that will add, open, and update cards in a _list
"""
from http import client
import webbrowser

from actions.voiceassistant import speak, takecommand
from actions.client_token import CLIENT

client = CLIENT


def add_card(boardname:str, listname:str, cardname:str):
    """
    This function will add a card to a list.

    :param client: TrelloClient object
    """
    # boardname = get_input("What board do you want to add a card to?")
    print(boardname)
    boards = client.list_boards()
    matching_boards = [board for board in boards if boardname in board.name.lower()]
    if not matching_boards:
        speak(f"Could not find board with name {boardname}")
        return
    board = matching_boards[0]

    # listname = get_input("What list do you want to add a card to?")
    lists = board.list_lists()
    matching_lists = [lst for lst in lists if listname in lst.name.lower()]
    if not matching_lists:
        speak(f"Could not find list with name {listname}")
        return
    _list = matching_lists[0]

    # cardname = get_input("What do you want to name your card?")
    _list.add_card(cardname)


def get_input(prompt):
    """
    Helper function to get input from user.
    """
    speak(prompt)
    return takecommand().lower().replace(".", "")


def open_card(client):
    """
    This function will open a card in a _list

    :param client: TrelloClient object
    """
    speak("What board do you want to open a card from?")
    board_name = takecommand().lower().replace(".", "")
    boards = client.list_boards()
    for board in boards:
        if board_name in board.name.lower():
            speak("What _list do you want to open a card from?")
            list_name = takecommand().lower().replace(".", "")
            lists = board.list_lists()
            for _list in lists:
                if list_name in _list.name.lower():
                    speak("What card do you want to open?")
                    card_name = takecommand().lower().replace(".", "")
                    cards = _list.list_cards()
                    for card in cards:
                        if card_name in card.name.lower():
                            webbrowser.open(card.url)


def update_card_name(client):
    """
    This function will update a card

    :param client: TrelloClient object
    """
    speak("What board do you want to update a card from?")
    board_name = takecommand().lower().replace(".", "")
    boards = client.list_boards()
    for board in boards:
        if board_name in board.name.lower():
            speak("What _list do you want to update a card from?")
            list_name = takecommand().lower().replace(".", "")
            lists = board.list_lists()
            for _list in lists:
                if list_name in _list.name.lower():
                    speak("What card do you want to update?")
                    card_name = takecommand().lower().replace(".", "")
                    cards = _list.list_cards()
                    for card in cards:
                        if card_name in card.name.lower():
                            speak("What do you want to update the card name to?")
                            new_card_name = takecommand().lower().replace(".", "")
                            card.set_name(new_card_name)
