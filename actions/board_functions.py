import re
import webbrowser
from actions.client_token import CLIENT

client = CLIENT

def open_trello():
    search_url = f"https://www.trello.com"
    webbrowser.open(search_url)
    # webbrowser.open(client.get_member("me").url)

def get_all_boards():
    boards = client.list_boards()
    for board in boards:
        print(board.id)

def add_board():
    board_name = board_name.replace(".", "")
    client.add_board(board_name)

def open_board():
    board_name = ""
    board_name = re.sub(r"[^\w\s]", "", board_name)
    board_name = board_name.strip().replace(" ", "-")
    boards = client.list_boards()
    board_names = {board.name.lower() for board in boards}
    if board_name in board_names:
        matching_board = next(
            board for board in boards if board.name.lower() == board_name
        )
        webbrowser.open(matching_board.url)
    else:
        print(f"Sorry, I couldn't find a board named {board_name}.")

# open_board()