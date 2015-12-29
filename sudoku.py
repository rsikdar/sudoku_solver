from tkinter import *
import copy
class Sudoku_box:
    def __init__(self):
        self.val = 0
        self.possible_val = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def remove_possible(self, val):
        if val in self.possible_val:
            self.possible_val.remove(val)

    def set_val(self, val):
        if val in self.possible_val:
            self.val = val
            self.possible_val.remove(val)

class Sudoku_board:
    def __init__(self):
        self.board = [[Sudoku_box() for x in range(9)] for x in range(9)] 
        self.rows = [{1, 2, 3, 4, 5, 6, 7, 8, 9} for x in range(9)]
        self.cols = [{1, 2, 3, 4, 5, 6, 7, 8, 9} for x in range(9)]
        self.boxes = [{1, 2, 3, 4, 5, 6, 7, 8, 9} for x in range(9)]

    def copy_board(self):
        return copy.deepcopy(self)

    def check_box(self, val, x, y):
        box = self.get_box_number(x, y)
        if val in self.boxes[box]:
            return True
        return False

    def get_box_number(self, x, y):
        if x <= 2:
            if y <= 2:
                return 0
            elif y <= 5:
                return 1
            elif y <= 8:
                return 2
        elif x <= 5:
            if y <= 2:
                return 3
            elif y <= 5:
                return 4
            elif y <= 8:
                return 5
        else:
            if y <= 2:
                return 6
            elif y <= 5:
                return 7
            elif y <= 8:
                return 8

    def set_val(self, val, x, y):
        if val in self.rows[x] and val in self.cols[y]:
            self.board[x][y].set_val(val)
            self.rows[x].remove(val)
            self.cols[y].remove(val)
            box_num = self.get_box_number(x, y)
            self.boxes[box_num].remove(val) 
            return 0
        else:
            return 1

    def __str__(self):
        print_horizontal = True
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end = " ")
                if i % 3 == 0 and i != 0 and print_horizontal:
                    print("--------------------------")
                    print_horizontal = False
                if i % 3 != 0:
                    print_horizontal = True
                if j != 8:
                    print(self.board[i][j].val, end = " ")
                else:
                    print(self.board[i][j].val)
        return ""

def update_possible_values(board):
    # # print('inside update')
    # print(board)
    updates_made = 0
    boxes_left = 0
    for i in range(9):
        for j in range(9):
            box = board.board[i][j]
            to_remove = []
            for x in box.possible_val:
                if not (x in board.rows[i] and x in board.cols[j] and board.check_box(x, i, j)):
                    to_remove.append(x)
            updates_made += len(to_remove)
            for x in to_remove:
                box.possible_val.remove(x)
            if len(box.possible_val) == 1 and box.val == 0:
                val = box.possible_val.pop()
                box.possible_val.add(val)   
                board.set_val(val, i, j)
            #conflict
            elif len(box.possible_val) == 0 and box.val == 0:
                return -1, -1
            elif box.val == 0:
                boxes_left += 1
    return updates_made, boxes_left

def sudoku_test_solvable(board):
    #returns whether the board is possibly solvable, and how many values are left to solve
    updates_made_temp = 1
    # solvable = True
    while updates_made_temp != 0:
        updates_made_temp, boxes_left = update_possible_values(board)
        if  updates_made_temp == -1:
            return False, 0
    return True, boxes_left

def sudoku_guess_solve(board):
    temp_board = board.copy_board()
    for i in range(9):
        for j in range(9):
            box = board.board[i][j]
            if box.val == 0:
                for x in box.possible_val:
                    temp_board.set_val(x, i, j)
                    solvable, boxes_left_temp = sudoku_test_solvable(temp_board)
                    if solvable and boxes_left_temp == 0:
                        return temp_board
                    elif solvable:
                        ret_board = sudoku_guess_solve(temp_board)
                        if ret_board == False:
                            temp_board = board.copy_board()
                        else:
                            return ret_board
                    else:
                        temp_board = board.copy_board()
    return False

def sudoku_solve(board):
    # print("attempt")
    updates_made, boxes_left = update_possible_values(board)
    while (updates_made != 0):
        updates_made,boxes_left = update_possible_values(board)
    if boxes_left != 0:
        #start guessing and checking for conflicts
        ret_board = sudoku_guess_solve(board)
        if ret_board != False:
            return ret_board
    # print(board)
    return board





# board = Sudoku_board()
# board.set_val(2, 0, 0)
# board.set_val(8, 0, 1)
# board.set_val(4, 0, 2)
# board.set_val(6, 0, 3)
# board.set_val(7, 0, 6)

# board.set_val(1, 1, 1)
# board.set_val(4, 1, 4)
# board.set_val(7, 1, 5)
# board.set_val(2, 1, 7)
# board.set_val(8, 1, 8)

# board.set_val(3, 2, 2)
# board.set_val(2, 2, 4)
# board.set_val(5, 2, 5)
# board.set_val(9, 2, 7)
# board.set_val(4, 2, 8)

# board.set_val(4, 3, 0)
# board.set_val(2, 3, 1)
# board.set_val(7, 3, 2)
# board.set_val(5, 3, 3)
# board.set_val(1, 3, 7)

# board.set_val(9, 4, 1)
# board.set_val(1, 4, 3)
# board.set_val(4, 4, 5)
# board.set_val(5, 4, 6)
# board.set_val(2, 4, 8)

# board.set_val(8, 5, 0)
# board.set_val(9, 5, 3)
# board.set_val(6, 5, 4)
# board.set_val(3, 5, 6)
# board.set_val(4, 5, 7)

# board.set_val(9, 6, 0)
# board.set_val(4, 6, 1)
# board.set_val(3, 6, 5)
# board.set_val(8, 6, 6)
# board.set_val(1, 6, 8)

# board.set_val(7, 7, 1)
# board.set_val(8, 7, 4)
# board.set_val(4, 7, 6)
# board.set_val(3, 7, 7)
# board.set_val(9, 7, 8)

# board.set_val(6, 8, 0)
# board.set_val(8, 8, 2)
# board.set_val(4, 8, 3)
# board.set_val(1, 8, 4)
# board.set_val(9, 8, 5)
# # print("original")
# # print(board)
# # print("solved")
# print(sudoku_solve(board))
# print(board.board[0][4].possible_val)
# print(board.rows[0])
class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.board = [[0 for x in range(9)] for x in range(9)] 
        self.parent = parent
        
        self.initUI()

    def display_err(self):
        return
        
    def sudoku_solve_get_input(self):
        board = Sudoku_board()
        # print(int(self.board[0][0].get()))
        # print(self.board[0][0].select_present())
        for i in range(9):
            for j in range(9):
                try:
                    err = board.set_val(int(self.board[i][j].get()), i, j)
                    # print(err)
                    # if err:
                    #   self.display_err()
                except ValueError:
                    self.display_err()
        board = sudoku_solve(board)
        # print(board)
        for i in range(9):
            for j in range(9):
                self.board[i][j].delete(0, END)
                val = str(board.board[i][j].val)
                if val == '0':
                    val = ''

                self.board[i][j].insert(0, val)

    def initUI(self):
      
        # self.parent.title("Sudoku Solver")
        # # self.style = Style()
        # # self.style.theme_use("default")

        # self.pack(fill=BOTH, expand=1)

        # quitButton = Button(self, text="Quit",
        #     command=self.quit)
        # quitButton.place(x=50, y=50)
        self.parent.title("Sudoku Solver")
        # self.style = Style()
        # self.style.theme_use("default")
        self.pack(fill=BOTH, expand=True)
        
        frame = Frame(self, relief=RAISED, borderwidth=1, height=4)
        frame.pack(fill=BOTH, expand=False)
        
        lbl1 = Label(frame, text="Sudoku Solver", width=10)
        lbl1.pack(side=TOP) 

        sudoku_frame = Frame(self, borderwidth=2, highlightthickness=0)
        sudoku_frame.pack(fill=BOTH, expand=False)

        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                # horizontal_line = Frame(sudoku_frame, borderwidth = 1)
                # horizontal_line.pack()    
                canvas = Canvas(sudoku_frame, height=8, width = 325, highlightthickness=0)
                canvas.create_line(0, 4, 325, 4)
                canvas.create_line(104, 0, 104, 8)
                canvas.create_line(212, 0, 212, 8)
                canvas.pack(side = TOP, padx = 2, pady=0)
            row = Frame(sudoku_frame, height = 0, width = 0, highlightthickness=0)
            row.pack(side = TOP,padx = 0, pady=0)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    # vertical_line = Frame(row, borderwidth = 1)
                    # vertical_line.pack()  
                    canvas = Canvas(row, height = 20, width = 8, highlightthickness=0)
                    canvas.create_line(4, 0, 4, 50)
                    canvas.pack(side=LEFT, padx =2, pady=0) 
                box = Entry(row, width = 4)
                box.pack(side=LEFT, padx=2, pady=0)
                self.board[i][j] = box


        # b1 = Entry(sudoku_frame, width=4)
        # b1.pack(side=LEFT, padx=10, pady=2)


  #       print_horizontal = True
        # for i in range(9):
        #   for j in range(9):
        #       if j % 3 == 0 and j != 0:
        #           print(" | ", end = " ")
        #       if i % 3 == 0 and i != 0 and print_horizontal:
        #           print("--------------------------")
        #           print_horizontal = False
        #       if i % 3 != 0:
        #           print_horizontal = True
        #       if j != 8:
        #           print(self.board[i][j].val, end = " ")
        #       else:
        #           print(self.board[i][j].val)



        
        quitButton = Button(self, text="Quit", command = self.quit)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        solveButton = Button(self, text="Solve", command = self.sudoku_solve_get_input)
        solveButton.pack(side=LEFT, padx=5)


def main():
  
    root = Tk()
    root.geometry("325x275")
    root.resizable(0,0)
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 




