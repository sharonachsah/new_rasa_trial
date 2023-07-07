from actions.client_token import CLIENT

client = CLIENT


def add_list(listname: str, boardname: str):

    board = None
    for board in client.list_boards():
        if boardname in board.name.lower():
            break

    if not board:
        print(f"Could not find board with name {boardname}")
        return

    board.add_list(listname)

def update_list_name(previous_list_name: str, fresh_list_name: str, boardname: str):
    board = None
    for board in client.list_boards():
        if boardname in board.name.lower():
            break

    if not board:
        print(f"Could not find board with name {boardname}")
        return

    trello_list = None
    for trello_list in board.list_lists():
        if previous_list_name in trello_list.name.lower():
            break

    if not trello_list:
        print(f"Could not find list with name {previous_list_name}")
        return

    trello_list.set_name(fresh_list_name)
    print(f"List {previous_list_name} updated to {fresh_list_name} successfully")
