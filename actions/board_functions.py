import webbrowser
from actions.client_token import CLIENT

client = CLIENT


def open_trello():
    search_url = "https://www.trello.com"
    webbrowser.open(search_url)

def add_board(boardnametoadd: str):
    client.add_board(boardnametoadd)

def open_board(boardnametoopen: str):
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
    board_url = board.url
    webbrowser.open(board_url)


def update_board_name(previous_board_name: str, new_board_name: str):
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

    board.set_name(new_board_name)
    print(f"Board '{previous_board_name}' updated to '{new_board_name}' successfully.")

