"""Implemention of the Maze ADT using a 2-D array."""
from copy import deepcopy
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""

    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        path = Stack()
        curr_pos = _CellPosition(self._start_cell.row, self._start_cell.col)

        # self._mark_path(curr_pos.row, curr_pos.col)
        # path.push(curr_pos)

        while True:
            if self._valid_move(curr_pos.row - 1, curr_pos.col):
                path.push(deepcopy(curr_pos))
                self._mark_path(curr_pos.row, curr_pos.col)
                curr_pos.row, curr_pos.col = curr_pos.row - 1, curr_pos.col
                # print("up..")
            elif self._valid_move(curr_pos.row, curr_pos.col + 1):
                path.push(deepcopy(curr_pos))
                self._mark_path(curr_pos.row, curr_pos.col)
                curr_pos.row, curr_pos.col = curr_pos.row, curr_pos.col + 1
                # print("right..")
            elif self._valid_move(curr_pos.row + 1, curr_pos.col):
                path.push(deepcopy(curr_pos))
                self._mark_path(curr_pos.row, curr_pos.col)
                curr_pos.row, curr_pos.col = curr_pos.row + 1, curr_pos.col
                # print("down..")
            elif self._valid_move(curr_pos.row, curr_pos.col - 1):
                path.push(deepcopy(curr_pos))
                self._mark_path(curr_pos.row, curr_pos.col)
                curr_pos.row, curr_pos.col = curr_pos.row, curr_pos.col - 1
                # print("left..")
            else:
                # print("wrong..")
                self._mark_tried(curr_pos.row, curr_pos.col)
                old_pos = path.pop()
                curr_pos.row, curr_pos.col = old_pos.row, old_pos.col
                # print(curr_pos)

            if self._exit_found(curr_pos.row, curr_pos.col):
                self._mark_path(curr_pos.row, curr_pos.col)
                return True
            if (
                curr_pos.row == self._start_cell.row
                and curr_pos.col == self._start_cell.col
            ):
                self._mark_tried(curr_pos.row, curr_pos.col)
                return False
            # print(self, flush=True)

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if (
                    self._maze_cells[i, j] == self.TRIED_TOKEN
                    or self._maze_cells[i, j] == self.PATH_TOKEN
                ):
                    self._maze_cells[i, j] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        output = ""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if self._maze_cells[i, j] != None:
                    output += str(self._maze_cells[i, j]) + " "
                else:
                    output += "_ "
            output += "\n"
        return output[:-1]

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return (
            row >= 0
            and row < self.num_rows()
            and col >= 0
            and col < self.num_cols()
            and self._maze_cells[row, col] is None
        )

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        """
        String representation of a pos
        """
        return "(" + str(self.row) + "," + str(self.col) + ")"
