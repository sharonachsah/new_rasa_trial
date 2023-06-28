"""
This file contains functions that will add, open, and update cards in a _list
"""
from http import client
import webbrowser

from actions.voiceassistant import speak, takecommand
from actions.client_token import CLIENT

client = CLIENT


def add_card(cardname: str, listname: str, boardname: str):
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
    print(lists)
    matching_lists = [lst for lst in lists if listname in lst.name.lower()]
    print(matching_lists)
    if not matching_lists:
        speak(f"Could not find list with name {listname}")
        return
    _list = matching_lists[0]
    print(_list)

    # cardname = get_input("What do you want to name your card?")
    _list.add_card(cardname)

def update_card_name(previous_card_name:str, new_card_name:str, listname:str, boardname:str):
    speak("What board do you want to update a card from?")
    boardname = boardname.lower().replace(".", "")
    boards = [board for board in client.list_boards() if boardname in board.name.lower()]

    listname = listname.lower().replace(".", "")

    found_list = None
    for board in boards:
        lists = [trello_list for trello_list in board.list_lists() if listname in trello_list.name.lower()]
        if lists:
            found_list = lists[0]
            break

    if not found_list:
        # Handle case when no matching list is found
        print("No matching list found with name: ", listname)

    previous_card_name = previous_card_name.lower().replace(".", "")

    cards = [card for card in found_list.list_cards() if previous_card_name in card.name.lower()]

    if not cards:
        # Handle case when no matching card is found
        print("No matching card found with name: ", previous_card_name)

    new_card_name = new_card_name.lower().replace(".", "")

    cards[0].set_name(new_card_name)
    print(f"Card name updated from {previous_card_name} to {new_card_name} successfully")

