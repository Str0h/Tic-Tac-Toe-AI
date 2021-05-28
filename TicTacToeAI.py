import random


class TicTacToe:
    def __init__(self):
        self.board = ['_' for _ in range(9)]
        self.gamemodes = {'user': self.user_move, 'easy': self.easy_move,
                          'medium': self.medium_move, 'hard': self.hard_move}
        self.player1 = None
        self.player2 = None
        self.winner = None
        self.welcome()
        self.main()

    @staticmethod
    def welcome():
        print("Welcome to the TicTacToe game by Stroh!\n")
        print("To start the game, type 'start player1 player2'.\nReplace player1 and player2 with gamemodes names.")
        print("The gamemodes are 'user', 'easy', 'medium' and 'hard'.\nAny gamemodes combinations are fine.")
        print("'user' is played by you, others are played by the computer.\n")
        print("Few examples of the correct input:\n")
        print("Input command: start user user")
        print("Input command: start user hard")
        print("Input command: start easy medium\n")
        print("""The cell numbers of the board are as follows:
        -----------
        | 1  2  3 |
        | 4  5  6 |
        | 7  8  9 |
        -----------""")
        print("To exit the game type 'exit'\n")

    def check_input(self):  # checks for correct input command
        while True:
            command = input('Input command: ').split()
            if command == ['exit']:
                return False
            if len(command) == 3:
                if command[0] == 'start' and command[1] in self.gamemodes and command[2] in self.gamemodes:
                    self.player1 = command[1]
                    self.player2 = command[2]
                    self.clear_board()
                    self.print_board()
                    return True
            print('Bad parameters!')

    def print_board(self):  # displays current board state
        print(9 * '-')
        print(f"| {self.board[0]} {self.board[1]} {self.board[2]} |")
        print(f"| {self.board[3]} {self.board[4]} {self.board[5]} |")
        print(f"| {self.board[6]} {self.board[7]} {self.board[8]} |")
        print(9 * '-')

    def clear_board(self):  # clears the board to the initial state
        self.board = ['_' for _ in range(9)]

    def cell_is_empty(self, cell):  # checks if cell is empty
        if self.board[cell] == '_':
            return True
        return False

    def empty_cells(self):  # returns indices of the empty cells
        return [cell for cell in range(9) if self.cell_is_empty(cell)]

    def game_is_over(self):  # checks if game is finished, defines game's outcome
        wins = [self.board[0:3], self.board[3:6], self.board[6:], self.board[0:9:3],
                self.board[1:9:3], self.board[2:9:3], self.board[0:9:4], self.board[2:7:2]]
        if ['X', 'X', 'X'] in wins:
            self.winner = 'X wins'
            return True
        elif ['O', 'O', 'O'] in wins:
            self.winner = 'O wins'
            return True
        elif self.board.count('_') == 0:
            self.winner = 'Draw'
            return True
        else:
            return False

    def current_turn(self):  # returns the mark of whose turn it is
        if self.board.count('X') == self.board.count('O'):
            return 'X'
        return 'O'

    def make_move(self, cell):  # places an appropriate mark in the given cell
        self.board[cell] = self.current_turn()

    def user_move(self):  # places an appropriate mark according to the given coordinate
        while True:
            coord = input('Enter the cell number: ')
            if coord.isdigit():
                cell = int(coord) - 1
                if cell not in range(9):
                    print('Number should be from 1 to 9!')
                elif not self.cell_is_empty(cell):
                    print('This cell is occupied! Choose another one!')
                else:
                    self.make_move(cell)
                    self.print_board()
                    break
            else:
                print('You should enter a number from 1 to 9!')

    def random_move(self):  # places an appropriate mark into a random empty cell
        self.make_move(random.choice(self.empty_cells()))
        self.print_board()

    def easy_move(self):  # easy difficulty bot
        print('Making move level "easy"')
        self.random_move()

    def medium_move(self):  # medium difficulty bot
        print('Making move level "medium"')
        if self.board.count('X') >= 2:
            for cell in self.empty_cells():  # checks if there are two in a row of its own mark and wins
                self.make_move(cell)
                if self.game_is_over():
                    self.print_board()
                    return
                self.board[cell] = '_'
            for cell in self.empty_cells():  # checks if there are two in a row of an opponent's mark and doesn't lose
                self.make_move(cell)
                self.board[cell] = 'O' if self.board[cell] == 'X' else 'X'
                if self.game_is_over():
                    self.board[cell] = 'X' if self.board[cell] == 'O' else 'O'
                    self.print_board()
                    return
                self.board[cell] = '_'
        self.random_move()  # otherwise makes a random move

    def max(self, mark, alpha, beta):  # max algorithm of the minimax
        max_score = -2  # -1 = loss; 0 = tie; 1 = win
        max_cell = None
        if self.game_is_over():
            if self.winner == 'Draw':
                return 0, 0
            elif self.winner[0] == mark:
                return 1, 0
            else:
                return -1, 0
        for cell in self.empty_cells():
            self.make_move(cell)
            score, _ = self.min(mark, alpha, beta)
            if score > max_score:
                max_score = score
                max_cell = cell
            self.board[cell] = '_'
            if max_score >= beta:
                return max_score, max_cell
            if max_score > alpha:
                alpha = max_score
        return max_score, max_cell

    def min(self, mark, alpha, beta):  # min algorithm of the minimax
        min_score = 2  # -1 = win; 0 = tie; 1 = loss
        min_cell = None
        if self.game_is_over():
            if self.winner == 'Draw':
                return 0, 0
            elif self.winner[0] == mark:
                return 1, 0
            else:
                return -1, 0
        for cell in self.empty_cells():
            self.make_move(cell)
            score, _ = self.max(mark, alpha, beta)
            if score < min_score:
                min_score = score
                min_cell = cell
            self.board[cell] = '_'
            if min_score <= alpha:
                return min_score, min_cell
            if min_score < beta:
                beta = min_score
        return min_score, min_cell

    def hard_move(self):  # initializes minimax algorithm
        if len(self.empty_cells()) == 9:
            self.make_move(random.choice([0, 2, 6, 8]))  # goes in one the corners, so it's less boring
        else:
            mark = self.current_turn()
            _, cell = self.max(mark, -2, 2)
            self.make_move(cell)
        print('Making move level "hard"')
        self.print_board()

    def player_move(self, gamemode):  # calls [gamemode]_move function
        self.gamemodes[gamemode]()

    def main(self):  # main game loop
        while True:
            if self.check_input():
                while True:
                    self.player_move(self.player1)
                    if self.game_is_over():
                        print(self.winner)
                        break
                    self.player_move(self.player2)
                    if self.game_is_over():
                        print(self.winner)
                        break
            else:
                break


TicTacToe()
