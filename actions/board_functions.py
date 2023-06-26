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


def add_board(boardnametoadd: str):
    """
    This function adds a board to a client with a given name after removing any periods in the name.

    :param boardname: The parameter `boardname` is a string that represents the name of a board that
    needs to be added. The function removes any periods (".") from the board name and then adds the
    board using the modified name
    :type boardname: str
    """
    # boardnametoadd = re.sub(r"[^\w\s]", "", boardnametoadd)
    client.add_board(boardnametoadd)


# add_board("new board")


def open_board(boardnametoopen: str):
    """
    This function opens a Trello board in the web browser if it exists, given a board name as input.

    :param boardnametoopen: The parameter `boardnametoopen` is a string that represents the name of the
    Trello board that the user wants to open
    :type boardnametoopen: str
    """
    # board_name = re.sub(r"[^\w\s]", "", boardnametoopen)
    board_name = boardnametoopen
    # board_name = board_name.s.replace(" ", "-")
    boards = client.list_boards()
    board_names = {
        board.name.lower() for board in boards
    }  # convert board names to lowercase
    if (
        board_name.lower() in board_names
    ):  # compare lowercase board name with lowercase board names in the set
        print("board_name: ", board_name)
        matching_board = next(
            board for board in boards if board.name.lower() == board_name.lower()
        )  # compare lowercase board name with lowercase board names in the list
        print(board for board in boards if board.name == board_name)
        print("matching_board: ", matching_board)
        webbrowser.open(matching_board.url)
    else:
        print(f"Sorry, I couldn't find a board named {board_name}.")


def update_board_name(prev_board_name: str, new_board_name: str):
    """
    This function will update a board

    :param client: TrelloClient object
    """
    boards = client.list_boards()
    for board in boards:
        if prev_board_name in board.name:
            board.set_name(new_board_name)


def delete_board(board_name: str):
    """
    This function will delete a board

    :param client: TrelloClient object
    """
    boards = client.list_boards()
    for board in boards:
        if board_name in board.name:
            board.close()
