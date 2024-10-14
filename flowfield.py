import pygame as pg
from collections import deque
import math


class Cell:
    path = "path"
    wall = "wall"
    source = "source"
    wall_cost = 10000
    def __init__(self, width, y_cord, x_cord):
        self.width = width
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.x_vector = 0
        self.y_vector = 0
        self.vector_length = int(self.width / 2)
        self.cost = 0
        self.color = (255,255,255)
        self.type = Cell.path


    def draw(self, window):
        start_x = self.x_cord * self.width
        start_y = self.y_cord * self.width
        pg.draw.rect(window, self.color, (start_x, start_y, self.width, self.width))
        
    
    def change_type(self, draw_walls_mode):
        if draw_walls_mode: 
            self.type = Cell.wall
            self.color = (0,0,0)
            self.cost = Cell.wall_cost
        else:
            self.type = Cell.path


    def draw_vector(self, window):
        center_x = (self.x_cord + 0.5) * self.width 
        center_y = (self.y_cord + 0.5) * self.width
        vector_tip_x = center_x + self.x_vector * self.vector_length
        vector_tip_y = center_y + self.y_vector * self.vector_length
        vector_angle = math.atan2(self.y_vector, self.x_vector)

        vector_left_tip_x = center_x + (math.cos(vector_angle - 0.5)  * self.vector_length *0.75)
        vector_left_tip_y = center_y + (math.sin(vector_angle - 0.5)  * self.vector_length *0.75)
        vector_right_tip_x = center_x + (math.cos(vector_angle + 0.5)  * self.vector_length *0.75)
        vector_right_tip_y = center_y + (math.sin(vector_angle + 0.5)  * self.vector_length *0.75)

        pg.draw.line(window, (0,0,0), (center_x, center_y), (vector_tip_x, vector_tip_y), 1)
        pg.draw.line(window, (0,0,0), (vector_tip_x, vector_tip_y), (vector_left_tip_x, vector_left_tip_y), 1)
        pg.draw.line(window, (0,0,0), (vector_tip_x, vector_tip_y), (vector_right_tip_x, vector_right_tip_y), 1)


class Flow_field:
    normalized_vec = 1 / math.sqrt(2)
    def __init__(self, map_width, map_height, cell_width, source_x, source_y):
        self.map_width = map_width
        self.map_height = map_height
        self.cell_width = cell_width
        self.grid = self.create_grid()
        self.source = self.grid[source_y][source_x]
        self.grid[source_y][source_x].type = Cell.source

    
    def update_source(self, new_source_x, new_source_y):
        self.source.type = Cell.path
        self.source = self.grid[new_source_y][new_source_x]
        self.source.type = Cell.source


    def create_grid(self):
        grid = [[] for _ in range(self.map_height)]

        for y_cord in range(self.map_height):
            for x_cord in range(self.map_width):
                cell = Cell(self.cell_width, y_cord, x_cord)
                grid[y_cord].append(cell)
        
        return grid 

    def draw(self, window):
        for row in self.grid:
            for cell in row:
                cell.draw(window)
                if cell != self.source:
                    cell.draw_vector(window)
    

    def generate_cost_field(self):
        queue = deque()
        visited = set()
        queue.append([0, self.source.y_cord, self.source.x_cord])
        visited.add((self.source.y_cord, self.source.x_cord))

        while len(queue) > 0:
            dist, y_cord, x_cord = queue.popleft()
            cell = self.grid[y_cord][x_cord]
            cell.cost = dist

            for neighbour in self.get_neighs_bfs(dist, y_cord, x_cord, visited):
                queue.append(neighbour)
        
        self.get_cell_colours(visited)
    

    def get_neighs_bfs(self, dist, y_cord, x_cord, visited):
        neighbours = []
        if y_cord > 0 and (y_cord-1, x_cord) not in visited and self.grid[y_cord-1][x_cord].type == Cell.path:
            neighbours.append([dist+1, y_cord-1, x_cord])
            visited.add((y_cord-1, x_cord))

        if x_cord > 0 and (y_cord, x_cord-1) not in visited and self.grid[y_cord][x_cord-1].type == Cell.path:
            neighbours.append([dist+1, y_cord, x_cord-1])
            visited.add((y_cord, x_cord-1))

        if y_cord < self.map_height - 1 and (y_cord+1, x_cord) not in visited and self.grid[y_cord+1][x_cord].type == Cell.path:
            neighbours.append([dist+1, y_cord+1, x_cord])
            visited.add((y_cord+1, x_cord))

        if x_cord < self.map_width - 1  and (y_cord, x_cord+1) not in visited and self.grid[y_cord][x_cord+1].type == Cell.path:
            neighbours.append([dist+1, y_cord, x_cord+1])
            visited.add((y_cord, x_cord+1))

        return neighbours

    

    def generate_vector_field(self):
        self.apply_kernel(self.min_neighbour_kernel)
        #self.apply_kernel(self.avg_neighbour_kernel)  #One needs to make a copy of the min_neigh_vector field first, then one can change 


    def apply_kernel(self, kernel):
        len_row = len(self.grid[0])

        for y_cord in range(len(self.grid)):
            for x_cord in range(len_row):
                cell = self.grid[y_cord][x_cord]
                if cell.type == Cell.wall or cell == self.source:
                    cell = self.grid[y_cord][x_cord]
                    cell.x_vector = 0
                    cell.y_vector = 0
                    continue

                kernel(y_cord, x_cord)
    

    def min_neighbour_kernel(self, y_cord, x_cord):
        min_neighbour = None
        min_cost = float('inf')
        
        for y_cord2 in range(y_cord-1, y_cord+2):
            for x_cord2 in range(x_cord-1, x_cord+2):
                if (not (0 <= y_cord2 < self.map_height) or not (0 <= x_cord2 < self.map_width) or 
                    (y_cord2 == y_cord and x_cord == x_cord2)):
                    continue
                    
                neigh_cell = self.grid[y_cord2][x_cord2]
                if neigh_cell.cost < min_cost:
                    min_neighbour = neigh_cell
                    min_cost = neigh_cell.cost
        

        x_vector = min_neighbour.x_cord - x_cord
        y_vector = min_neighbour.y_cord - y_cord
        if abs(x_vector) == 1 and abs(y_vector) == 1:
            x_vector = Flow_field.normalized_vec * x_vector
            y_vector = Flow_field.normalized_vec * y_vector


        cell = self.grid[y_cord][x_cord]
        cell.x_vector = x_vector
        cell.y_vector = y_vector

        assert -1 <= abs(x_vector) <= 1 and -1 <= abs(y_vector) <= 1, f"VECTORERROR"
    
    def avg_neighbour_kernel(self, y_cord, x_cord):

        cell = self.grid[y_cord][x_cord]
        y_vector = 0
        x_vector = 0
        for y_cord2 in range(y_cord-1, y_cord+2):
            for x_cord2 in range(x_cord-1, x_cord+2):
                if (not (0 <= y_cord2 < self.map_height) or not (0 <= x_cord2 < self.map_width)): #or 
                    #(y_cord2 == y_cord and x_cord == x_cord2)):
                    continue

                cell = self.grid[y_cord2][x_cord2]
                x_vector += cell.x_vector
                y_vector += cell.y_vector
        
        x_vector /= 8
        y_vector /= 8
        cell.x_vector = x_vector
        cell.y_vector = y_vector

        assert -1 <= abs(x_vector) <= 1 and -1 <= abs(y_vector) <= 1, f"VECTORERROR"


    def get_cell_colours(self, visited):
        for y_cord in range(self.map_height):
            for x_cord in range(self.map_width):
                cell = self.grid[y_cord][x_cord]
                
                if cell.type == Cell.source:
                    cell.color = (255, 255, 0)
                    continue
                
                if cell.type == Cell.wall:
                    continue

                if (y_cord, x_cord) not in visited:
                    cell.color = (0,0,155)
                    continue


                k = (self.map_height + self.map_height) * 1.5
                redness = max(0, (-255/k) * cell.cost + 255)
                blueness = min(155, 155/k * cell.cost)
                cell.color = (redness, 0, blueness)

                
    

        
