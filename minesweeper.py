import random
from enum import Enum
#import numpy

POSITION_X=0
POSITION_Y=1

class CellType(Enum):
    EMPTY = 0
    NUMBER = 1
    BOMB = 2
    FLAG = 3

class CellVisibility(Enum):
    VISIBLE=True
    HIDDEN=False


class Cell:
    def __init__(self, cell_type, visibility, adjacent_bomb_count):
        # self.x=x
        # self.y=y
        self.cell_type=cell_type
        self.visibility=visibility
        self.adjacent_bomb_count = adjacent_bomb_count

    def get_cell_type(self):
        return self.cell_type

    def is_visible(self):
        return self.visibility == self.VISIBLE


class Grid:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        
        self.cells=[[0 for y in range(size_y)] for x in range(size_x)]


    def create_grid(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                cell = Cell(CellType.EMPTY,CellVisibility.HIDDEN,0)
                self.cells[x][y] = cell

    def get_cell(self, x, y):
        if x<0 or x >= self.size_x or y<0 or y>= self.size_y:
            return Cell(CellType.EMPTY,CellVisibility.HIDDEN,0)

        return self.cells[x][y]
            
    def get_index(self, position):
        return position[POSITION_X] + self.size_x * position[POSITION_Y]

    def get_position(self, index):
        x = index % self.size_x
        y = index // self.size_x
        return [x,y]

    def add_bombs(self,total_bomb_count,player_start_position):
        current_bomb_count=0
        cell_list=[i for i in range(self.size_x * self.size_y)]
        cell_list.remove(self.get_index(player_start_position))

        while current_bomb_count < total_bomb_count:
            cell_position=random.randint(0,len(cell_list)-1)
            bomb_index=cell_list[cell_position]
            bomb_position=self.get_position(bomb_index)
 
            self.cells[bomb_position[POSITION_X]][bomb_position[POSITION_Y]] = Cell(CellType.BOMB, CellVisibility.HIDDEN, 0)
            current_bomb_count+=1
            cell_list.remove(bomb_index)

    
    def number_of_bombs_near_cell(self,x,y):
        bomb_count=0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                if not(x_offset == 0 and y_offset == 0) and self.get_cell(x + x_offset, y + y_offset).get_cell_type() == CellType.BOMB:
                    bomb_count+=1
        return bomb_count

    def set_bomb_counts(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                bomb_count=self.number_of_bombs_near_cell(x,y)
                if self.get_cell(x,y).cell_type == CellType.EMPTY:
                    self.cells[x][y] = Cell(CellType.NUMBER, CellVisibility.VISIBLE, bomb_count)

    def reveal_cell(self,new_cell_position):
        index = 0
        for y in range(self.size_y):
            for x in range(self.size_x):
                index+=1
                cell_position = self.cells[index-1]
                if cell_position[0] == new_cell_position[0] and cell_position[1] == new_cell_position[1]:
                    cell_position[3]=False



    def display_grid(self):
        icons={
        0:"\033[38;5;0m"+".",
        1:"\033[38;5;4m"+"1", # numbers
        2:"\033[38;5;123m"+"2",
        3:"\033[38;5;2m"+"3",
        4:"\033[38;5;190m"+"4",
        5:"\033[38;5;215m"+"5",
        6:"\033[38;5;202m"+"6",
        7:"\033[38;5;200m"+"7",
        8:"\033[38;5;93m"+"8",
        9:"\033[38;5;2m"+"\u25fb",
        10:"\033[38;5;1m"+"x",
        11:"\033[38;5;15m"+"x",
        12:"\033[38;5;34m"+"\u25a1"
        }

        print(end="    ")
        for x in range(self.size_x):
            if x // 10 == 0:
                print(end="   ")
            else:
                print(x // 10,end="  ")
   
        print("")

        print(end="    ")
        for x in range(self.size_x):
            print(x % 10,end="  ")
        print("")

        for y in range(self.size_y):
            print("\033[38;5;7m"+str(y).zfill(2), end="  ")
            for x in range(self.size_x):
                cell = self.get_cell(x,y)
                if cell.get_cell_type() == CellType.BOMB:
                    print(icons.get(10),end="  ")
                elif cell.get_cell_type() == CellType.NUMBER:
                    print(icons.get(cell.adjacent_bomb_count),end="  ")
                else:
                    print(icons.get(0),end="  ")
            print(" ")
        print("\033[38;5;7m")



grid1 = Grid(12,12)

grid1.create_grid()



#grid1.reveal_cell([0,0])

grid1.add_bombs(2,[1,1])
grid1.set_bomb_counts()

grid1.display_grid()