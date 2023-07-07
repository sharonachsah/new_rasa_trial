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



def add_board(boardnametoadd: str):
    client.add_board(boardnametoadd)


# add_board("new board")


def open_board(boardnametoopen: str):
    """
    This function opens a Trello board in the web browser if it exists, given a board name as input.

    :param boardnametoopen: The parameter `boardnametoopen` is a string that represents the name of the
    Trello board that the user wants to open
    :type boardnametoopen: str
    """
    board = next(
        (
            t_board
            for t_board in client.list_boards()
            if t_board.name == boardnametoopen
        ),
        None,
    )
    if not board:
        print(f"Board '{boardnametoopen}' not found.")
        return

    # Generate the board URL
    board_url = board.url

    # Open the board URL in the default web browser
    webbrowser.open(board_url)

open_board("demo")

def update_board_name(previous_board_name: str, new_board_name: str):
    """
    This function updates the name of a Trello board.

    :param previous_board_name: The parameter `previous_board_name` is a string that represents the name of the
    Trello board that the user wants to update
    :type previous_board_name: str
    :param new_board_name: The parameter `new_board_name` is a string that represents the new name of the
    Trello board that the user wants to update
    :type new_board_name: str
    """
    board = next(
        (
            t_board
            for t_board in client.list_boards()
            if t_board.name == previous_board_name
        ),
        None,
    )
    if not board:
        print(f"Board '{previous_board_name}' not found.")
        return

    # Update the board name
    board.set_name(new_board_name)
    print(f"Board '{previous_board_name}' updated to '{new_board_name}' successfully.")

update_board_name("demo", "demo1")
