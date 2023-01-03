# Minesweeper

# imported modules
import random
from enum import Enum
import time

# global variable declarations
start_time=time.time()
user_name=""



def time_convert(sec): # converts the time to hours minutes and seconds
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return ("Time elapsed: {0}h:{1}m:{2}s".format(int(hours),int(mins),int(sec)))



# Enums

POSITION_X=0
POSITION_Y=1

class CellType(Enum):
    EMPTY = 0
    NUMBER = 1
    BOMB = 2
    DUMMY = 3

class CellVisibility(Enum):
    VISIBLE=True
    HIDDEN=False

class CellFlagged(Enum):
    FLAG=True
    NO_FLAG=False


# Difficulty class containing name and values of the difficulty
class Difficulty:
    def __init__(self, name ,total_bombs, grid_size_x, grid_size_y):
        self.name=name
        self.total_bombs=total_bombs
        self.grid_size_x=grid_size_x
        self.grid_size_y=grid_size_y

    def get_name(self):
        return str(self.name)
        
    def get_bombs(self):
        return self.total_bombs

    def get_grid_size_x(self):
        return self.grid_size_x

    def get_grid_size_y(self):
        return self.grid_size_y

# list of difficulties that the player can select
difficulties=[
    Difficulty("beginner",10,9,9),
    Difficulty("intermediate",40,16,16),
    Difficulty("expert",99,36,16)
]


# Cell class used in the grid
class Cell:
    # sets the values for the cell
    def __init__(self, cell_type, visibility, adjacent_bomb_count, flag):
        self.cell_type=cell_type
        self.visibility=visibility
        self.adjacent_bomb_count = adjacent_bomb_count
        self.flag=flag

    # gets the type of cell
    def get_cell_type(self):
        return self.cell_type

    # returns a boolean value for whether the cell is visible
    def is_visible(self):
        return self.visibility == CellVisibility.VISIBLE
    
    # sets the cell to be visible
    def set_visible(self):
        self.visibility = CellVisibility.VISIBLE

    # sets the number that the cell should display based on the number of nearby bombs
    def set_bomb_count(self, bomb_count):
        self.adjacent_bomb_count = bomb_count
        self.cell_type = CellType.NUMBER

    # returns a boolean value for whether the cellhas a flag on it
    def is_flagged(self):
        return self.flag == CellFlagged.FLAG

    # adds a flag to the cell
    def add_flag(self):
        self.flag = CellFlagged.FLAG

    # removes the flag from the cell
    def remove_flag(self):
        self.flag = CellFlagged.NO_FLAG

    # if the cell has no flag it adds a flag if the cell already has a flag then it removes it
    def toggle_flag(self):
        if self.flag == CellFlagged.NO_FLAG:
            self.add_flag()
        else:
            self.remove_flag()


# Board class comprised of cells
class Board:
    # sets the values for the board
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        
        self.cells=[[0 for y in range(size_y)] for x in range(size_x)] # creates a list large enough to hold all the cell classes

    # creates the board with the correct size and fills it with empty cells
    def create_board(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                cell = Cell(CellType.EMPTY,CellVisibility.HIDDEN,0,CellFlagged.NO_FLAG)
                self.cells[x][y] = cell

    # get a cell from the cells list at specfic coordinates
    def get_cell(self, x, y):
        if x < 0 or x >= self.size_x or y < 0 or y >= self.size_y:# checking if the cell is outside the boundaries of the grid
            return Cell(CellType.DUMMY,CellVisibility.HIDDEN,0,CellFlagged.NO_FLAG)# and returning an empty cell if it is

        return self.cells[x][y]# otherwise return the cell in the grid
            
    # returns the index of the cell based on its position
    def get_index(self, position):
        return position[POSITION_X] + self.size_x * position[POSITION_Y]

    # returns the position of the cell in a list format based on where it's index is
    def get_position(self, index):
        x = index % self.size_x
        y = index // self.size_x
        return [x,y]

    # adds a specified number of bombs to the grid anywhere except for the player's starting position
    def add_bombs(self,total_bomb_count,player_start_x,player_start_y):
        current_bomb_count=0
        cell_index_list=[i for i in range(self.size_x * self.size_y)]

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):

                cell_position = [player_start_x + x_offset, player_start_y + y_offset]

                if cell_position[0] < 0 or cell_position[0] >= self.size_x or cell_position[1] <0 or cell_position[1] >= self.size_y: # check if the cell is within the boundaries of the grid
                    continue

                cell_index_list.remove(self.get_index(cell_position)) # remove the index from the list so the player can't start on a bomb

        while current_bomb_count < total_bomb_count:
            cell_position=random.randint(0,len(cell_index_list)-1)
            bomb_index=cell_index_list[cell_position]
            bomb_position=self.get_position(bomb_index)
 
            self.cells[bomb_position[POSITION_X]][bomb_position[POSITION_Y]] = Cell(CellType.BOMB, CellVisibility.HIDDEN, 0, CellFlagged.NO_FLAG)
            current_bomb_count+=1
            cell_index_list.remove(bomb_index)# remove the bomb index from the list so you can't get 2 bombs in the same position

    # find the number of bombs near the cell
    def number_of_bombs_near_cell(self,x,y):
        bomb_count=0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                if not(x_offset == 0 and y_offset == 0) and self.get_cell(x + x_offset, y + y_offset).get_cell_type() == CellType.BOMB:
                    bomb_count+=1
        return bomb_count

    # for each cell on the board set the number of nearby bombs
    def set_bomb_counts(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                bomb_count=self.number_of_bombs_near_cell(x,y)
                if self.get_cell(x,y).cell_type == CellType.EMPTY and bomb_count != 0:
                    cell = self.cells[x][y]
                    cell.set_bomb_count(bomb_count)

    # reveals cells around the player's input, recurses if the cell is empty
    def reveal_cells(self,x,y):
        centre_cell = self.get_cell(x, y)
        
        centre_cell.remove_flag()
        centre_cell.set_visible()

        if centre_cell.get_cell_type() == CellType.BOMB:
            centre_cell.set_visible()
            lose()

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                cell = self.get_cell(x + x_offset, y + y_offset)

                if cell.get_cell_type() == CellType.DUMMY or cell.is_visible():
                    continue

                if centre_cell.get_cell_type() == CellType.EMPTY:
                    cell.set_visible()
                    cell.remove_flag()
                    self.reveal_cells(x + x_offset, y + y_offset)

    # checks if all the bombs have been found and calls the win function
    def check_if_win(self):
        bomb_positions=[]
        unopened_cell_positions=[]
        for y in range(self.size_y):
            for x in range(self.size_x):
                cell = self.get_cell(x,y)

                if not(cell.is_visible()):
                    unopened_cell_positions.append([x,y])


                if cell.get_cell_type() == CellType.BOMB:
                    bomb_positions.append([x,y])

        if unopened_cell_positions == bomb_positions:
            win()

    # toggles the flag of a cell in a given position on the board  
    def toggle_flag(self,x,y):
        cell = self.get_cell(x, y)
        if not(cell.is_visible()):
            cell.toggle_flag()

    # sets a cell to visible on the board
    def set_cell_visible(self, coords):
        cell = self.cells[coords[POSITION_X]][coords[POSITION_Y]]
        cell.set_visible()

    #returns the number of bombs left
    def bombs_remaining(self):
        flags_placed=0
        total_bombs=difficulty1.get_bombs()
        for y in range(self.size_y):
            for x in range(self.size_x):
                cell = self.cells[x][y]
                if cell.is_flagged():
                    flags_placed+=1
        return total_bombs - flags_placed
    
    #flags a random  bomb on the board
    def hint(self):
        bomb_indexes=[]
        for y in range(self.size_y):
            for x in range(self.size_x):

                cell = self.cells[x][y]

                if cell.get_cell_type() == CellType.BOMB and not(cell.is_flagged()):
                    bomb_indexes.append(self.get_index([x,y]))

        if not(bomb_indexes== []):

            random_index=random.randint(0,len(bomb_indexes)-1)
            hint_index=bomb_indexes[random_index]
            hint_position=self.get_position(hint_index)
            hint_cell = self.cells[hint_position[0]][hint_position[1]]
            hint_cell.add_flag()

        else:
            print("all bombs are flagged!")


    # prints the whole board
    def print_board(self):

        # icons that are used to represent the objects in the game
        icons={
        0:"\033[38;5;0m"+".",
        1:"\033[38;5;4m"+"1",
        2:"\033[38;5;123m"+"2",
        3:"\033[38;5;82m"+"3",
        4:"\033[38;5;190m"+"4",
        5:"\033[38;5;215m"+"5",
        6:"\033[38;5;202m"+"6",
        7:"\033[38;5;200m"+"7",
        8:"\033[38;5;93m"+"8",
        9:"\033[38;5;2m"+"\u25fb",
        10:"\033[38;5;1m"+"x",
        11:"\033[38;5;196m"+"\u2691",
        12:"\033[38;5;34m"+"\u25a1"
        }

        print("")

        print(str(self.bombs_remaining()) + " " + icons.get(11), end = "\033[38;5;7m\n") # displays the number of flags left

        print(end="    ")

        print("")

        print(end="    ")
        for x in range(self.size_x):# prints the horizontal numbers on the board
            print(x % 10,end="  ")
        print("")

        for y in range(self.size_y):

            print("\033[38;5;7m"+str(y).zfill(2), end="  ")# prints the vertical numbers on the board

            for x in range(self.size_x):

                cell = self.get_cell(x,y)

                # give each an icon depending on its type and value
                if cell.is_flagged():
                    print(icons.get(11),end="  ")
                    continue
                if not cell.is_visible():
                    print(icons.get(12),end="  ")
                    continue
                if cell.get_cell_type() == CellType.BOMB:
                    print(icons.get(10),end="  ")
                elif cell.get_cell_type() == CellType.NUMBER:
                    print(icons.get(cell.adjacent_bomb_count),end="  ")
                else:
                    print(icons.get(0),end="  ")
            print(" ")
        print("\033[38;5;7m")

# writes the user name difficulty and time taken to leaderboard.txt
def write_to_leaderboard(user_name, difficulty, time_elapsed):
    file = open("leaderboard.txt", "a")

    file.write("Username:{0}, Difficulty:{1}, {2}".format(user_name, difficulty, time_elapsed) + "\n")

    file.close()

# function that is called when the player wins the game
def win():
        end_time=time.time()
        print(
            "=========YOU WIN !=========",end="\n"
            )
        time_elapsed=end_time-start_time
        display_time=time_convert(time_elapsed)
        print(display_time)

        write_to_leaderboard(user_name,difficulty1.get_name(),display_time)

# function that is called whent the player loses the game
def lose():
        end_time=time.time()
        print(
            "=========YOU LOSE !=========",end="\n"
            )
        time_lapsed=end_time-start_time
        time_convert(time_lapsed)

# gets the input from the user and performs an action based on the input with error handling
def get_user_input():
    while True:
        user_input=input("enter input:")
        try:
            if user_input == "hint":
                return user_input
            else: 
                coords=str(user_input).split()
                x=int(coords[0])
                y=int(coords[1])
                flag=str(coords[2])
                return [x,y,flag]
        except:
            print("Invalid input try (0 0 f for flag or 0 0 o for open cell or hint for hint)")

# sets the difficulty to the difficulty that was input at the start
def set_difficulty(input_difficulty):
    for difficulty in difficulties:
        if difficulty.get_name() == input_difficulty:
            return difficulty

# function that creates a list of diffficulty names
def difficulty_names():
    difficulty_names=[]
    for difficulty in difficulties:
        difficulty_names.append(difficulty.get_name())
    return difficulty_names
    
print(difficulty_names())

#gets user to input the difficulty with error handling
while True:
    input_difficulty = str(input("Enter difficulty:"))
    try:
        if input_difficulty in difficulty_names():
           difficulty1 = set_difficulty(input_difficulty)
           break
        else: 
            continue
    except:
        print("Invalid difficulty try: beginner, intermediate or expert")
        

print(str(difficulty1.get_bombs()) + " bombs")

user_name=input("enter name:")

board1 = Board(difficulty1.get_grid_size_x(),difficulty1.get_grid_size_y())

board1.create_board()

board1.print_board()

start_time=time.time()

coords=get_user_input()

board1.add_bombs(difficulty1.get_bombs(),coords[POSITION_X],coords[POSITION_Y])
board1.set_bomb_counts()

while True:
    if coords == "hint":
        board1.hint()
    elif coords[2] == "f":
        board1.toggle_flag(coords[POSITION_X],coords[POSITION_Y])
    else:
        board1.reveal_cells(coords[POSITION_X],coords[POSITION_Y])
        board1.check_if_win()

    board1.print_board()

    coords=get_user_input()