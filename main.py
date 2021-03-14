from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from copy import deepcopy
from itertools import chain
from time import sleep


def get_nums_list(task_elem):
    tgs = task_elem.find_elements_by_class_name("task-group")

    nums = []

    for tg in tgs:
        tcs = tg.find_elements_by_class_name("task-cell")

        num_strings = [tc.text for tc in tcs if tc.text]
        nums.append([int(x) for x in num_strings])

    return nums


def get_new_boards(board):
    # return a list of boards with the next cell clicked
    new_cell_location = None
    for i, row in enumerate(board):
        if new_cell_location:
            break
        for j, cell in enumerate(row):
            if new_cell_location:
                break
            if cell is None:
                new_cell_location = (i, j)

    nc_i, nc_j = new_cell_location

    nb1 = deepcopy(board)
    nb1[nc_i][nc_j] = True

    nb2 = deepcopy(board)
    nb2[nc_i][nc_j] = False

    return [nb1, nb2]


assert get_new_boards(board=[[None, None], [None, None]]) == [[[True, None], [None, None]], [[False, None], [None, None]]]
assert get_new_boards([[True, None], [None, None]]) == [[[True, True], [None, None]], [[True, False], [None, None]]]


def get_row_groups(row):
    """
    input: [True, True, None, True, None]
    return: [2, 1]
    """
    row_groups = []

    for prev_cell, cell in zip([None] + row, row):
        if cell is not True:
            continue

        if prev_cell is True:
            # add to the last num
            row_groups[-1] += 1
        else:
            # append a new group
            row_groups.append(1)

    return row_groups

x = get_row_groups([True, True, None, True, None])
assert x == [2, 1]
assert get_row_groups([True, True, True, True, False]) == [4]


def row_groups_can_fit_in_nums(row_groups, nums):
    """
    input: [1, 1], [2, 1]
    output: True

    input: [3], [2, 1]
    output: False
    """
    if len(row_groups) > len(nums):
        return False

    # if row_groups is shorter that nums,
    # we can try "fitting it in" in multiple positions

    start_positions_to_try = range(len(nums) - len(row_groups) + 1)

    for start_pos in start_positions_to_try:
        pairs_to_compare = list(zip(row_groups, nums[start_pos :]))
        # print(pairs_to_compare)

        can_fit = all(
            row_g_num <= constraint_num
            for row_g_num, constraint_num in pairs_to_compare
        )
        if can_fit:
            return True
    # we haven't been able to fit it anywhere
    return False

assert row_groups_can_fit_in_nums([1, 1], [2, 1]) is True
assert row_groups_can_fit_in_nums([3], [2, 1]) is False
assert row_groups_can_fit_in_nums([1, 1, 1], [2, 4]) is False  # first cond.
assert row_groups_can_fit_in_nums([3, 2], [1, 2, 3, 2, 1]) is True
assert row_groups_can_fit_in_nums([], [2, 1]) is True


def row_is_complete(row):
    no_nones = all(cell is not None for cell in row)
    return no_nones


def board_is_complete(board):
    all_cells = chain(*board)
    no_nones = all(cell is not None for cell in all_cells)
    return no_nones


def row_is_valid(row, nums):
    # isn't perfect.  Errs on the side of being valid
    row_groups = get_row_groups(row)

    if row_is_complete(row):
        return row_groups == nums

    return row_groups_can_fit_in_nums(row_groups, nums)


assert row_is_valid(row=[True, None, False, True, None], nums=[2, 1]) is True
assert row_is_valid(row=[True, True, False, True, None], nums=[1, 1]) is False

assert row_is_valid([False, False, False, True, False], nums=[1, 1]) is False
assert row_is_valid([True, False, True, False, False], nums=[1, 1]) is True


def is_valid(board, top_nums, side_nums):
    rows = board
    cols = list(list(x) for x in zip(*board))
    assert len(rows) == len(top_nums) == len(side_nums) == len(cols)

    for row, nums in zip(rows, side_nums):
        if not row_is_valid(row, nums):
            #print(f"bad row! {row}")
            return False


    for col, nums in zip(cols, top_nums):
        if not row_is_valid(col, nums):
            #print(f"bad col! {col}, {nums}")
            return False

    return True


assert is_valid(board=[[True, False], [None, True]], top_nums=[[1], [1]], side_nums=[[1], [1]]) is True
assert is_valid(board=[[True, False], [None, True]], top_nums=[[1], []], side_nums=[[1], [1]]) is False

b = [
    [True, False, True, False, False],
    [False, False, True, True, True],
    [False, False, False, True, True],
    [False, False, True, True, True],
    [True, True, True, False, False],
]

assert is_valid(b, top_nums=[[1,1], [1], [2, 2], [3], [3]], side_nums=[[1,1], [3], [2], [3], [3]]) is True



def solve(top_nums, side_nums, board_size=5):

    # puzzles are board_sizexboard_size
    # each board element will be either:
    # - None (we don't know yet)
    # - True (click it)
    # - False (don't click it)

    empty_board = [[None for _ in range(board_size)] for _ in range(board_size)]
    queue = [empty_board]

    while True:
        board = queue.pop(0)

        # check if we have a solution:
        if board_is_complete(board):
            return board
        new_boards = get_new_boards(board)
        new_valid_boards = [
            b
            for b in new_boards
            if is_valid(b, top_nums, side_nums)
        ]
        queue.extend(new_valid_boards)


x = solve(top_nums=[[1], [1]], side_nums=[[1], [1]], board_size=2)
assert x == [[True, False], [True, False]]

x = solve(top_nums=[[1,1], [1], [2, 2], [3], [3]], side_nums=[[1,1], [3], [2], [3], [3]], board_size=5)
b = [
    [True, False, True, False, False],
    [False, False, True, True, True],
    [False, False, False, True, True],
    [False, False, True, True, True],
    [True, True, True, False, False],
]
assert x == b


def get_rows(board_elem):
    rows = board_elem.find_elements_by_class_name("row")

    rows_list = [
        row.find_elements_by_class_name("cell")
        for row in rows
    ]

    return rows_list


def enter_solution(board_rows, solution):
    all_board_cells = chain(*board_rows)
    all_solution_cells = chain(*solution)

    for board_cell, solution_cell in zip(all_board_cells, all_solution_cells):

        if solution_cell is True:
            sleep(0.5)
            board_cell.click()


def solve_on_screen(browser):
    tt = browser.find_element_by_id("taskTop")
    top_nums = get_nums_list(tt)
    print(f"top nums: {top_nums}")

    tl = browser.find_element_by_id("taskLeft")
    side_nums = get_nums_list(tl)
    print(f"side nums: {side_nums}")

    solution = solve(top_nums=top_nums, side_nums=side_nums)

    board_elem = browser.find_elements_by_class_name("nonograms-cell-back")[0]
    board_rows = get_rows(board_elem)

    enter_solution(board_rows, solution)

    done_button = browser.find_element_by_id("btnReady")
    done_button.click()
    sleep(1)

    new_puzzle_button = browser.find_element_by_id("btnNew")
    new_puzzle_button.click()
    sleep(2)


# TODO handle this better.  chrome driver auto installer?
cd_path = "C:/Users/BenB/Documents/BenB/chromedriver_win32/chromedriver.exe"
browser = Chrome(cd_path)
browser.get("https://www.puzzle-nonograms.com/")





while True:
    solve_on_screen(browser)
