"""This file contains functions that deal with lists on Trello boards."""
from actions.client_token import CLIENT

client = CLIENT


def add_list(boardname: str, listname: str):
    """
    It takes a Trello client object as an argument, asks the user for the name of a board, and then
    creates a new list on that board with a name that the user provides.

    :param client: the Trello client object
    """
    boards = client.list_boards()
    for board in boards:
        if boardname in board.name.lower():
            board.add_list(listname)


def update_list(boardname: str, listname: str, newname: str):
    """
    It takes a Trello client object as an argument, asks the user for the name of a board, and then
    updates the name of a list on that board with a name that the user provides.

    :param client: the Trello client object
    """
    boards = client.list_boards()
    for board in boards:
        if boardname in board.name.lower():
            lists = board.list_lists()
            for trello_list in lists:
                if listname in trello_list.name.lower():
                    trello_list.name = newname


def archive_list(boardname: str, listname: str):
    """
    It takes a Trello client object as an argument, asks the user for the name of a board, and then
    archives a list on that board with a name that the user provides.

    :param client: the Trello client object
    """
    boards = client.list_boards()
    for board in boards:
        if boardname in board.name.lower():
            lists = board.list_lists()
            for trello_list in lists:
                if listname in trello_list.name.lower():
                    trello_list.close()


def get_board_by_name(client, board_name):
    """
    Find a Trello board by name.

    :param client: Trello client object.
    :param board_name: Name of the board to find.
    :return: Trello board object if found, otherwise None.
    """
    return next(
        (board for board in client.list_boards() if board_name == board.name.lower()),
        None,
    )


def get_list_by_name(board, list_name):
    """
    Find a Trello list by name on a given board.

    :param board: Trello board object.
    :param list_name: Name of the list to find.
    :return: Trello list object if found, otherwise None.
    """
    return next(
        (
            trello_list
            for trello_list in board.list_lists()
            if list_name == trello_list.name.lower()
        ),
        None,
    )
