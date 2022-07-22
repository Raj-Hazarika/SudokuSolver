def solve(bo):
    """
    This function is responsible to solve a given block in the grid.
    This is done by entering all the numbers from 1 to 9 and finding a valid entry.
    If the entry is illegal then the block is made empty and the previous block value is changed and so on.
    ARGS: -bo > block object
    RETURN: True if solved, False otherwise
    """
    find = find_empty(bo)  # Calling the find_empty() function to check wheher the given block is empty or not.
    if not find:
        return True  # exiting the function if the block is not empty.
    else:
        row, col = find  # if block is empty then assigning its row and column to identify its location.

    for i in range(1, 10):  # checks for every number from 1 to 9 for a valid entry
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    """
    This function is resonsible to check whether a number is valid or not. 
    This is done by checking along the row, along the column and in 3x3 grids.
    ARGS: -bo > block object; -num > number to be inserted; -pos > row and column index of the block
    RETURN: True if the number is valid, False otherwise
    """
    # check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    """
    This function is responsible for printing the board.
    ARGS: -bo > block object
    RETURN: None
    """
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("_ _ _ _ _ _ _ _ _ _ _ ")
        for j in range(len(bo)):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(bo[i][j], end=" ")
        print()


def find_empty(bo):
    """
    This function checks whether the given block is empty or not. 
    If the given block is empty then it returns the location of the block.
    ARGS: -bo > block object
    RETURN: row and column index if block is empty, None otherwise
    """
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, col

    return None
