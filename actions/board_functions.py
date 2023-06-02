""" This file contains functions that are used to interact with Trello boards."""
import re
import webbrowser
from actions.client_token import CLIENT

client = CLIENT


def open_trello():
    """
    This function opens the Trello website using the webbrowser module in Python.
    """
    search_url = "https://www.trello.com"
    webbrowser.open(search_url)
    # webbrowser.open(client.get_member("me").url)


def get_all_boards():
    """
    This function retrieves and prints the IDs of all boards using the Trello API client.
    """
    boards = client.list_boards()
    for board in boards:
        print(board.id)


def add_board(boardname: str):
    """
    This function adds a board to a client with a given name after removing any periods in the name.

    :param boardname: The parameter `boardname` is a string that represents the name of a board that
    needs to be added. The function removes any periods (".") from the board name and then adds the
    board using the modified name
    :type boardname: str
    """
    # boardname = boardname.replace(".", "")
    client.add_board(boardname)


# add_board("new board")


def open_board(boardname: str):
    """
    This function opens a Trello board in the web browser if it exists, otherwise it prints an error
    message.

    :param boardname: a string representing the name of a Trello board to be opened
    :type boardname: str
    """
    board_name = re.sub(r"[^\w\s]", "", boardname)
    # board_name = board_name.strip().replace(" ", "-")
    boards = client.list_boards()
    print(boards)
    board_names = {board.name for board in boards}
    if board_name in board_names:
        print("board_name: ", board_name)
        matching_board = next(board for board in boards if board.name == board_name)
        print(board for board in boards if board.name == board_name)
        print("matching_board: ", matching_board)
        webbrowser.open(matching_board.url)
    else:
        print(f"Sorry, I couldn't find a board named {board_name}.")


# open_board("speech recognition")


def update_board_name(board_name: str, new_board_name: str):
    """
    This function will update a board

    :param client: TrelloClient object
    """
    boards = client.list_boards()
    for board in boards:
        if board_name in board.name.lower():
            board.set_name(new_board_name)


update_board_name("speech recognition", "voice recognition")


def delete_board(board_name: str):
    """
    This function will delete a board

    :param client: TrelloClient object
    """
    boards = client.list_boards()
    for board in boards:
        if board_name in board.name.lower():
            board.close()
