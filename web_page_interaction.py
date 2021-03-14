from time import sleep
from itertools import chain

from solver import solve


def get_nums_list(task_elem):
    tgs = task_elem.find_elements_by_class_name("task-group")

    nums = []

    for tg in tgs:
        tcs = tg.find_elements_by_class_name("task-cell")

        num_strings = [tc.text for tc in tcs if tc.text]
        nums.append([int(x) for x in num_strings])

    return nums





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
