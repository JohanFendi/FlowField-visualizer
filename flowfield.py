import pygame as pg
from collections import deque



class Cell:
    path = "path"
    wall = "wall"
    source = "source"
    def __init__(self, width, x_pos, y_pos, color, acceleration_x = 0, acceleration_y = 0 , dist_to_source = 0):
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.type = Cell.path
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.dist_to_source = dist_to_source


    def draw(self, window):
        start_x = self.x_pos * self.width
        start_y = self.y_pos * self.width
        try:
            pg.draw.rect(window, self.color, (start_y, start_x, self.width, self.width))
        except ValueError:
            print(self.color)
    

    def change_type(self, draw_walls_mode):
        if draw_walls_mode: 
            self.type = Cell.wall
            self.color = (0,0,0)
        else:
            self.type = Cell.path


class Flow_field:
    def __init__(self, map_width, map_height, cell_width, source_x, source_y):
        self.map_width = map_width
        self.map_height = map_height
        self.cell_width = cell_width
        self.source_x = source_x 
        self.source_y = source_y 
        self.grid = self.create_grid()
        self.grid[source_y][source_x].type = Cell.source

    def create_grid(self):
        grid = [[] for _ in range(self.map_height)]

        for y_cord in range(self.map_height):
            for x_cord in range(self.map_width):
                cell = Cell(self.cell_width, y_cord, x_cord, (255,255,255))
                grid[y_cord].append(cell)
        
        return grid 

    def draw(self, window):
        for row in self.grid:
            for cell in row:
                cell.draw(window)
    

    def compute_distances(self):
        queue = deque()
        visited = set()
        queue.append([0, self.source_y, self.source_x])
        visited.add((self.source_y, self.source_x))

        while len(queue) > 0:
            dist, y_cord, x_cord = queue.popleft()
            cell = self.grid[y_cord][x_cord]
            cell.dist_to_source = dist

            for neighbour in self.get_neighbours(dist, y_cord, x_cord, visited):
                queue.append(neighbour)
        
        self.get_cell_colours(visited)


    def get_neighbours(self, dist, y_cord, x_cord, visited):
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
                    cell.color = (0,0,255)
                    continue


                k = (self.map_height + self.map_height) * 1.5
                redness = max(0, (-255/k) * cell.dist_to_source + 255)
                blueness = min(255, 255/k * cell.dist_to_source )
                cell.color = (redness, 100, blueness)

                
    

        
