import shelve
from config import shelve_name


def get_score_board():
    with shelve.open(shelve_name) as storage:
        leaders = set()

        for key in storage:
            leaders.add((storage[key]['score'], storage[key]['username']))

        text = 'Leader Board:\n'
        show_elements = 5
        cur = 0
        for el in sorted(leaders, reverse=True):
            if cur < show_elements:
                cur += 1
                text += f'{el[1]}: {el[0]}\n'
        return text


def get_score(chat_id):
    with shelve.open(shelve_name) as storage:
        return storage[str(chat_id)]['score']