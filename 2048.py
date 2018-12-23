import random

board_state1 = [[0,2,4,0],[8,12,12,8],[12,8,16,16],[32,32,16,16]] # sample board state
board_state2 = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
#board index ranges from 0 - 15

def start_game_state()->list:
    """reset the game"""
    board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    return(board)

def print_game_state(board:list)->None:
    """in takes a board state and prints it out"""
    for i in range(0,4):
        print (board[i])
#print_game_state(board_state1)    

def index_to_coordinate(board_index: int) ->list:
    """convert board index into a list of row, then column"""
    row = int(board_index/4)
    column = board_index%4
    return([row, column])
assert index_to_coordinate(0) == [0,0]
assert index_to_coordinate(15) == [3,3]

def check_space(board:list)->"list of int":
    """put in the entire existing board list,
output a list of board position that is empty"""
    board_index = 0
    board_space = []
    for i in range(0,16):
        board_coor = index_to_coordinate(i)
        if board[board_coor[0]][board_coor[1]] == 0:
            board_space.append(i)
    return(board_space)
#print(check_space(board_state1))

def add_two(board:list)->list:
    """put in a board and return one with 2 added in it"""
    space_left = check_space(board) #create a list of board index left spaced
    board_index = random.randint(0,len(space_left)-1) #randomly choose a number from the list
#    print (board_index)
    coordinate_to_add = index_to_coordinate(space_left[board_index])
    board[coordinate_to_add[0]][coordinate_to_add[1]] += 2
    return(board)
#print (add_two(board_state1))

"""Let's think about how this game will work
First it will create a new game state
Then it will explain how to control
or the game just starts, as the game itself prompt the player to input
This repeats until the program can no longer run the add_two command"""
# w:up s:down d:right a:left
#execute_sum calls on execute_list_command, which calls on execute_list
#and delete zero
def execute_list(board:list,row_first:int,column_dif:int, row_dif:int) ->list:
    """return a list of pre_calculated(but managed) board for execute_list_command"""
    new_board = []
    for i in range(0,4):   #4 rows, 4 loop
        #each loop a row 
        board_index = row_first
        extend_row = []
        for x in range(0,4):
            board_coor =index_to_coordinate(board_index)
            extend_row.append(board[board_coor[0]][board_coor[1]])
            board_index += column_dif
        new_board.append(extend_row)
        row_first += row_dif
    return(new_board)
#print (up_list(board_state2,0,4,1)) #up
#print (up_list(board_state2,3,-1,4)) #right
#print (up_list(board_state2,12,-4,1)) #down
#print (up_list(board_state2,0,1,4)) #left

def execute_list_command(board:list, command:str):
    """combine command with execute list for execute sum"""
    if command == "w":
        row_first = 0
        column_dif = 4
        row_dif = 1
    elif command == "a":
        row_first = 0
        column_dif = 1
        row_dif = 4
    elif command == "s":
        row_first = 12
        column_dif = -4
        row_dif = 1
    elif command == "d":
        row_first = 3
        column_dif = -1
        row_dif = 4
    return(execute_list(board,row_first,column_dif, row_dif))
#print (execute_list_command(board_state2,"d"))

def delete_zero(sum_board:list)->list:
    """delete all zero on the board to enable sum function"""
    for i in [0,1,2,3]:# no changes here, there must be 4 rows
        while 0 in sum_board[i]:
            sum_board[i].remove(0)
    return(sum_board)

def column_sum(row:list)-> list:
    """sum up  a row that should have no zero """
    for i in range(0,4):
        if i < (len(row)-1):
            if row[i] == row[i+1]:
                row[i] *= 2
                del(row[i+1])
        else:
            if len(row) !=4: 
                row.append(0)
    return(row) # directly return value if there are nothing to sum up
assert column_sum([2,2]) == [4,0,0,0]
assert column_sum([]) == [0,0,0,0]
assert column_sum([2])==[2,0,0,0]
assert column_sum([2,4,4,8]) ==[2,8,8,0] #column check should be 1,2
assert column_sum([4,4,8,8]) == [8,16,0,0]
assert column_sum([2,4,2,4]) == [2,4,2,4]

def execute_sum(board:list, command: str)->list:
    """process the command by the player and return the board state"""
    #have the command as a parameter, or have it included in this code?
    sum_list = execute_list_command(board,command)
    sum_list = delete_zero(sum_list)
    for i in range(0,4):
        board[i] = column_sum(sum_list[i])
    if command == "s":
        board = execute_list_command(board,"d")
        board = execute_list_command(board,"w")
    else:
        board = execute_list_command(board, command)
    return(board)   
            
def main_game():
    """main game!"""
    correct_input = ["w","a","s","d"]
    board = start_game_state()
    board = add_two(board)
    lost = False
    while lost == False:
        print_game_state(board)
        command = input("w:up a:left s:down d:right  ")
        while command not in correct_input:
            command = input("w:up a:left s:down d:right  ")
        board = execute_sum(board,command)
        board = add_two(board)
main_game()

