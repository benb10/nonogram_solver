from solver import get_new_boards, get_row_groups, row_groups_can_fit_in_nums, row_is_valid, is_valid, solve



def test_get_new_boards():
    assert get_new_boards(board=[[None, None], [None, None]]) == [
        [[True, None], [None, None]],
        [[False, None], [None, None]],
    ]
    assert get_new_boards([[True, None], [None, None]]) == [
        [[True, True], [None, None]],
        [[True, False], [None, None]],
    ]


def test_get_row_groups():
    assert get_row_groups([True, True, None, True, None]) == [2, 1]
    assert get_row_groups([True, True, True, True, False]) == [4]


def test_row_groups_can_fit_in_nums():
    assert row_groups_can_fit_in_nums([1, 1], [2, 1]) is True
    assert row_groups_can_fit_in_nums([3], [2, 1]) is False
    assert row_groups_can_fit_in_nums([1, 1, 1], [2, 4]) is False
    assert row_groups_can_fit_in_nums([3, 2], [1, 2, 3, 2, 1]) is True
    assert row_groups_can_fit_in_nums([], [2, 1]) is True


def test_row_is_valid():
    assert row_is_valid(row=[True, None, False, True, None], nums=[2, 1]) is True
    assert row_is_valid(row=[True, True, False, True, None], nums=[1, 1]) is False
    assert row_is_valid([False, False, False, True, False], nums=[1, 1]) is False
    assert row_is_valid([True, False, True, False, False], nums=[1, 1]) is True


def test_is_valid():
    assert (
        is_valid(
            board=[[True, False], [None, True]], top_nums=[[1], [1]], side_nums=[[1], [1]]
        )
        is True
    )
    assert (
        is_valid(
            board=[[True, False], [None, True]], top_nums=[[1], []], side_nums=[[1], [1]]
        )
        is False
    )

    b = [
        [True, False, True, False, False],
        [False, False, True, True, True],
        [False, False, False, True, True],
        [False, False, True, True, True],
        [True, True, True, False, False],
    ]

    assert (
        is_valid(
            b,
            top_nums=[[1, 1], [1], [2, 2], [3], [3]],
            side_nums=[[1, 1], [3], [2], [3], [3]],
        )
        is True
    )


def test_solve_simple():
    solution = solve(top_nums=[[1], [1]], side_nums=[[1], [1]], board_size=2)
    assert solution == [[True, False], [False, True]]


def test_solve_5_by_5():
    solution = solve(
        top_nums=[[1, 1], [1], [2, 2], [3], [3]],
        side_nums=[[1, 1], [3], [2], [3], [3]],
        board_size=5,
    )
    expected_solution = [
        [True, False, True, False, False],
        [False, False, True, True, True],
        [False, False, False, True, True],
        [False, False, True, True, True],
        [True, True, True, False, False],
    ]
    assert solution == expected_solution
