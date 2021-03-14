from copy import deepcopy
from itertools import chain


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
        pairs_to_compare = list(zip(row_groups, nums[start_pos:]))
        # print(pairs_to_compare)

        can_fit = all(
            row_g_num <= constraint_num
            for row_g_num, constraint_num in pairs_to_compare
        )
        if can_fit:
            return True
    # we haven't been able to fit it anywhere
    return False


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



def is_valid(board, top_nums, side_nums):
    rows = board
    cols = list(list(x) for x in zip(*board))
    assert len(rows) == len(top_nums) == len(side_nums) == len(cols)

    for row, nums in zip(rows, side_nums):
        if not row_is_valid(row, nums):
            # print(f"bad row! {row}")
            return False

    for col, nums in zip(cols, top_nums):
        if not row_is_valid(col, nums):
            # print(f"bad col! {col}, {nums}")
            return False

    return True





def solve(top_nums, side_nums, board_size=5):
    """Return a list of lists representing the solution to the puzzle.

    puzzles are board_size x board_size
    each board element will be either:
    - None (we don't know yet)
    - True (click it)
    - False (don't click it)
    """


    empty_board = [[None for _ in range(board_size)] for _ in range(board_size)]
    queue = [empty_board]

    while True:
        if not queue:
            raise ValueError(f"Unable to find a solution.")

        board = queue.pop(0)

        # check if we have a solution:
        if board_is_complete(board):
            return board
        new_boards = get_new_boards(board)
        new_valid_boards = [b for b in new_boards if is_valid(b, top_nums, side_nums)]
        queue.extend(new_valid_boards)
