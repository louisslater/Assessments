import random
from enum import Enum
#import numpy

class Cell:
    def __init__(self, x, y, cell_type, visibility):
        self.x=x
        self.y=y
        self.cell_type=cell_type
        self.visibility=visibility

    def get_cell_type(self):
        return self.cell_type

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


class Grid:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        
        self.cells=[[0 for x in range(size_x)] for y in range(size_y)]


    def create_grid(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                cell = Cell(x,y,CellType.EMPTY,CellVisibility.VISIBLE)
                self.cells[x][y] = cell

    def get_cell(self, x, y):
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
 
            self.cells[bomb_position[POSITION_X]][bomb_position[POSITION_Y]] = Cell(bomb_position[POSITION_X] ,bomb_position[POSITION_Y], CellType.BOMB, CellVisibility.HIDDEN)
            current_bomb_count+=1
            cell_list.remove(bomb_index)

    
        

    def add_one_to_cell(self, cell_position):
        if cell_position[2] < 9:
                cell_position[2] +=1
                return cell_position

    def number_of_bombs_near_cell(self):
        index = 0
        for row in range(self.size_y):
            for column in range(self.size_x):
                index+=1
                cell_position = self.cells[index-1]
                if cell_position[2] == 10:

                    #vertical cells
                    #down
                    if cell_position[1] < self.size_y-1:
                        adjacent_cell_position=self.cells[index-1+self.size_x]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)
                    #up
                    if cell_position[1] > 0:
                        adjacent_cell_position=self.cells[index-1-self.size_x]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)

                    #horizontal cells
                    #left
                    if cell_position[0] > 0:
                        adjacent_cell_position=self.cells[index-2]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)
                    #right
                    if cell_position[0] < self.size_x-1:
                        adjacent_cell_position=self.cells[index]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)

                    #diagonal cells
                    #down-right
                    if cell_position[1] < self.size_y-1 and cell_position[0] < self.size_x-1:
                        adjacent_cell_position=self.cells[index+self.size_x]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)

                    #down-left
                    if cell_position[1] < self.size_y-1 and cell_position[0] > 0:
                        adjacent_cell_position=self.cells[index-2+self.size_x]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)

                    #up-right
                    if cell_position[1] > 0 and cell_position[0] < self.size_x-1:
                        adjacent_cell_position=self.cells[index-self.size_x]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)
                    #up-left
                    if cell_position[1] > 0 and cell_position[0] > 0:
                        adjacent_cell_position=self.cells[index-2-self.size_x]
                        adjacent_cell_position=self.add_one_to_cell(adjacent_cell_position)

    def reveal_cell(self,new_cell_position):
        index = 0
        for row in range(self.size_y):
            for column in range(self.size_x):
                index+=1
                cell_position = self.cells[index-1]
                if cell_position[0] == new_cell_position[0] and cell_position[1] == new_cell_position[1]:
                    cell_position[3]=False



    def display_grid(self):
        icons={
        0:" ",
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

        for y in range(self.size_y):
            for x in range(self.size_x):
                cell = self.get_cell(x,y)
                if cell.get_cell_type() == CellType.BOMB:
                    print(icons.get(10),end="  ")
                else:
                    print(icons.get(1),end="  ")
            print(" ")
        print("\033[38;5;7m")



grid1 = Grid(3,3)

grid1.create_grid()

#grid1.reveal_cell([0,0])

grid1.add_bombs(3,[0,0])

#grid1.number_of_bombs_near_cell()

grid1.display_grid()