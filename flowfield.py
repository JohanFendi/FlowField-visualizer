import pygame as pg
from collections import deque



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


class Flow_field:
    normalized_vec = 0.707
    def __init__(self, map_width, map_height, cell_width, source_x, source_y):
        self.map_width = map_width
        self.map_height = map_height
        self.cell_width = cell_width
        self.grid = self.create_grid()
        self.source = self.grid[source_y][source_x]
        self.grid[source_y][source_x].type = Cell.source


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
    

    def compute_vector_field(self):
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

                diff_x = neigh_cell.x_cord - x_cord
                diff_y = neigh_cell.y_cord - y_cord
                assert -1 <= diff_x <= 1 and -1 <= diff_y <= 1, f"NEIGH_CELL_ERROR" 
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


    def get_cell_colours(self, visited):
        for y_cord in range(self.map_height):
            for x_cord in range(self.map_width):
                cell = self.grid[y_cord][x_cord]
                
                if cell.type == Cell.source:
                    cell.color = (255,0,255)
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

                
    

        
