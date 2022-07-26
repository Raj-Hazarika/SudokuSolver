# GUI.py
import pygame
from solver import solve, valid
import time

pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.solved = list(list(i) for i in self.board)
        self.solved_cubes = [[Cube(self.solved[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

    def solved_board(self):
        """
        This function solves the puzzle.
        ARGS: None
        RETURN: None
        """
        solve(self.solved)

    def update_model(self):
        """
        Updates the board.
        ARGS: None
        RETURN: None
        """
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        """
        This function inserts a number in an empty block.
        If the number is valid then the block number is changed to that else the block is set back to empty.
        ARGS: -val > number to be inserted
        RETURN: True if number is valid and inserted, False otherwise
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        """
        This function marks the given number in a block without entering it.
        The number is just added as a side-note and not checked whether it is valid or not.
        ARGS: -val > number to be inserted
        RETURN: None
        """
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        """
        This function draws the sudoku board and the each block.
        ARGS: -win > pygame windows
        RETURN: None
        """
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def view_solved(self, win):
        """
        If the space key is pressed then the solved board is displayed.
        This function is similar to draw() function but displays the solved board instead of the puzzle.
        ARGS: -win > pygame windows
        RETURN: None
        """
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.solved_cubes[i][j].set(self.solved[i][j])
                if self.board[i][j] == 0:
                    self.solved_cubes[i][j].draw_final(win, (150, 150, 150))
                else:
                    self.solved_cubes[i][j].draw_final(win, (0, 0, 0))

    def select(self, row, col):
        """
        Selects the blocks that has been pressed.
        ARGS: -row > row number of the block; -col > column number of the block
        RETURN: None
        """
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        """
        Clears the block.
        ARGS: None
        RETURN: None
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        Recognises a click on an empty block.
        ARGS: -pos > pygame mouse position tuple as x and y direction
        RETURN: Row number and column number if clicked on a valid block, None otherwise
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def is_finished(self):
        """
        Checks if the game is finished or not.
        ARGS: None
        RETURN: True if game compeleted, False otherwise
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """
        Prints the numbers of the unsolved sudoku puzzle.
        ARGS: -win > pygame window
        RETURN: None
        """
        fnt = pygame.font.SysFont('dejavuserif', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_final(self, win, color):
        """
        Draws the inserted value on the board.
        ARGS: -win > pygame window; -color > color of the font
        RETURN: None
        """
        fnt = pygame.font.SysFont('dejavuserif', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        text = fnt.render(str(self.value), 1, color)
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

    def set(self, val):
        """
        A setter function to assign a number to a block.
        ARGS: -val > number to be assigned
        RETURN: None
        """
        self.value = val

    def set_temp(self, val):
        """
        A setter function to assign the rough/side-note number to a block.
        ARGS: -val > number to be assigned
        RETURN: None
        """
        self.temp = val


def redraw_window(win, board, clock, incorrect, dims, show, pos=None):
    height, width = dims[1], dims[0]
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("arial", 40)
    text = fnt.render("Time: " + format_time(clock), 1, (0, 0, 0))
    win.blit(text, (540 - 180, 550))
    if incorrect:
        error = pygame.Rect(pos[1] * height, pos[0] * width, height, width)
        pygame.draw.rect(win, (255, 0, 0), error)
        for i in range(1000):
            pass
    # Draw grid and board
    if show:
        board.view_solved(win)
    else:
        board.draw(win)


def format_time(secs):
    """
    Responsible for the timer in the game. Converting minutes and hours.
    ARGS: -secs > number of seconds passed since the game started
    RETURN: -mat > a string formating seconds, minutes and hours
    """
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    dimension = (board.width / 9, board.height / 9)
    key = None
    run = True
    incorrect = False
    show_solution = False
    pos = (0, 0)
    start = time.time()
    board.solved_board()
    while run:
        if not show_solution:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_solution = True
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if not board.place(board.cubes[i][j].temp):
                            incorrect = True
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key!=None:
            board.sketch(key)
        redraw_window(win, board, play_time, incorrect, dimension, show_solution, board.click(pos))
        incorrect = False
        pygame.display.update()


main()
pygame.quit()
