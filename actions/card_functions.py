from actions.client_token import CLIENT
from actions.voiceassistant import speak

client = CLIENT


def add_card(cardname: str, listname: str, boardname: str):
    board = None
    for board in client.list_boards():
        if boardname in board.name.lower():
            break

    if not board:
        speak(f"Could not find board with name {boardname}")
        return

    trello_list = None
    for trello_list in board.list_lists():
        if listname in trello_list.name.lower():
            break

    if not trello_list:
        speak(f"Could not find list with name {listname}")
        return

    trello_list.add_card(cardname)
    print(f"Card {cardname} added to list {listname} successfully")

def update_card_name(previous_card_name:str, new_card_name:str, listname:str, boardname:str):

    board = None
    for board in client.list_boards():
        if boardname in board.name.lower():
            break

    if not board:
        speak(f"Could not find board with name {boardname}")
        return

    trello_list = None
    for trello_list in board.list_lists():
        if listname in trello_list.name.lower():
            break

    if not trello_list:
        speak(f"Could not find list with name {listname}")
        return

    card = None
    for card in trello_list.list_cards():
        if previous_card_name in card.name.lower():
            break

    if not card:
        speak(f"Could not find card with name {previous_card_name}")
        return

    card.set_name(new_card_name)
    print(f"Card {previous_card_name} updated to {new_card_name} successfully")

