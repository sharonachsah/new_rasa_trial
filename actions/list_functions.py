"""This file contains functions that deal with lists on Trello boards."""
from actions.client_token import CLIENT

client = CLIENT


def add_list(listname: str, boardname: str):
    boards = [board for board in client.list_boards() if boardname in board.name.lower()]
    for board in boards:
        board.add_list(listname)

def update_list_name(previous_list_name: str, new_list_name: str, boardname: str):
    boards = [board for board in client.list_boards() if boardname in board.name.lower()]
    lists = [trello_list for board in boards for trello_list in board.list_lists() if previous_list_name in trello_list.name.lower()]
    for trello_list in lists:
        trello_list.name = new_list_name


