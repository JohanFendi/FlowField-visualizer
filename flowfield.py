import pygame as pg
from collections import deque
import math

# Cell types
path = "path"
wall = "wall"
source = "source"

# Color constants
source_color = (255, 255, 0)
unreachable_cell_color = (50, 50, 50)
vector_color = (0, 255, 0)
wall_color = (0,0,0)
wall_cost = 10000  # High cost for walls to make them "unreachable"

#Intensity of heatmap colors (0-255)
heatmap_redness = 150
heatmap_blueness = 150

# Arrow drawing constants for vector field visualization
arrow_tip_ratio = 0.75  # Ratio for the length of arrow tips
arrow_tip_angle = 0.3   # Angle (in radians) for the arrow tips

# Normalized vector for diagonal directions to keep consistent vector lengths
normalized_vec = 1 / math.sqrt(2)


class Cell:
    def __init__(self, width, y_pos, x_pos):
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vector = 0
        self.y_vector = 0
        self.vector_length = int(self.width / 2)
        self.cost = 0
        self.color = (255,255,255)
        self.type = path


    #Draw the cell as a rectangle in the window
    def draw(self, window):
        start_x = self.x_pos * self.width
        start_y = self.y_pos * self.width
        pg.draw.rect(window, self.color, (start_x, start_y, self.width, self.width))
        

    #Change the cell type between wall and path based on 
    #whether the drawing walls functionallity is on or of
    def change_type(self, draw_walls_mode):
        if draw_walls_mode: 
            self.type = wall
            self.color = wall_color
            self.cost = wall_cost
        else:
            self.type = path


    #Draw the vector/arrow inside the cell
    def draw_vector(self, window):
        center_x = (self.x_pos + 0.5) * self.width 
        center_y = (self.y_pos + 0.5) * self.width
        vector_angle = math.atan2(self.y_vector, self.x_vector)

        # Calculate the points for the arrow tips
        vector_tip_x = center_x + self.x_vector * self.vector_length
        vector_tip_y = center_y + self.y_vector * self.vector_length
        vector_left_tip_x = center_x + (math.cos(vector_angle - arrow_tip_angle)  * self.vector_length * arrow_tip_ratio)
        vector_left_tip_y = center_y + (math.sin(vector_angle - arrow_tip_angle)  * self.vector_length * arrow_tip_ratio)
        vector_right_tip_x = center_x + (math.cos(vector_angle + arrow_tip_angle)  * self.vector_length * arrow_tip_ratio)
        vector_right_tip_y = center_y + (math.sin(vector_angle + arrow_tip_angle)  * self.vector_length * arrow_tip_ratio)

        # Draw the vector line and the arrow tips
        pg.draw.line(window, vector_color, (center_x, center_y), (vector_tip_x, vector_tip_y), 1)
        pg.draw.line(window, vector_color, (vector_tip_x, vector_tip_y), (vector_left_tip_x, vector_left_tip_y), 1)
        pg.draw.line(window, vector_color, (vector_tip_x, vector_tip_y), (vector_right_tip_x, vector_right_tip_y), 1)


class Flow_field:
    def __init__(self, map_width, map_height, cell_width, source_x, source_y):
        self.map_width = map_width
        self.map_height = map_height
        self.cell_width = cell_width
        self.grid = self.create_grid()
        self.source = self.grid[source_y][source_x]
        self.grid[source_y][source_x].type = source

    
    #Updates source when it's position is changed by the user
    def update_source(self, new_source_x, new_source_y):
        self.source.type = path
        self.source = self.grid[new_source_y][new_source_x]
        self.source.type = source


    #Creates a 2D array containing rows of cells
    def create_grid(self):
        grid = [[] for _ in range(self.map_height)]

        for y_pos in range(self.map_height):
            for x_pos in range(self.map_width):
                cell = Cell(self.cell_width, y_pos, x_pos)
                grid[y_pos].append(cell)
        
        return grid 


    #Draws every call, and draws vectors for path cells
    def draw(self, window):
        for row in self.grid:
            for cell in row:
                cell.draw(window)
                if cell.type == path:
                    cell.draw_vector(window)
    

    #Bfs algorithm to get the distance to a given cell from the source
    def generate_integration_field(self):
        queue = deque()
        visited = set()
        queue.append([0, self.source.y_pos, self.source.x_pos])
        visited.add((self.source.y_pos, self.source.x_pos))

        while len(queue) > 0:
            dist, y_pos, x_pos = queue.popleft()
            cell = self.grid[y_pos][x_pos]
            cell.cost = dist

            for neighbour in self.get_neighs_bfs(dist, y_pos, x_pos, visited):
                queue.append(neighbour)
        
        self.get_cell_colours(visited)
    

    #Gets all horisontal and vertical neighbours, but not diagonal. 
    #Used in the integration field generation
    def get_neighs_bfs(self, dist, y_pos, x_pos, visited):
        neighbours = []
        if y_pos > 0 and (y_pos-1, x_pos) not in visited and self.grid[y_pos-1][x_pos].type == path:
            neighbours.append([dist+1, y_pos-1, x_pos])
            visited.add((y_pos-1, x_pos))

        if x_pos > 0 and (y_pos, x_pos-1) not in visited and self.grid[y_pos][x_pos-1].type == path:
            neighbours.append([dist+1, y_pos, x_pos-1])
            visited.add((y_pos, x_pos-1))

        if y_pos < self.map_height - 1 and (y_pos+1, x_pos) not in visited and self.grid[y_pos+1][x_pos].type == path:
            neighbours.append([dist+1, y_pos+1, x_pos])
            visited.add((y_pos+1, x_pos))

        if x_pos < self.map_width - 1  and (y_pos, x_pos+1) not in visited and self.grid[y_pos][x_pos+1].type == path:
            neighbours.append([dist+1, y_pos, x_pos+1])
            visited.add((y_pos, x_pos+1))

        return neighbours

    
    #Applies a given kernel to generate the vectorfield.
    def generate_vector_field(self):
        self.apply_kernel(self.min_neighbour_kernel)


    #Higher order function for applying kernels.
    def apply_kernel(self, kernel):
        len_row = len(self.grid[0])

        for y_pos in range(len(self.grid)):
            for x_pos in range(len_row):
                cell = self.grid[y_pos][x_pos]
                if cell.type == wall or cell == self.source:
                    cell = self.grid[y_pos][x_pos]
                    cell.x_vector = 0
                    cell.y_vector = 0
                    continue

                kernel(y_pos, x_pos)
    

    #Makes every cells vector point towards it's neighbour with the
    #minimum path cost. 
    def min_neighbour_kernel(self, y_pos, x_pos):
        min_neighbour = None
        min_cost = float('inf')
        
        for y_pos2 in range(y_pos-1, y_pos+2):
            for x_pos2 in range(x_pos-1, x_pos+2):
                if (not (0 <= y_pos2 < self.map_height) or not (0 <= x_pos2 < self.map_width) or 
                    (y_pos2 == y_pos and x_pos == x_pos2)):
                    continue
                    
                neigh_cell = self.grid[y_pos2][x_pos2]
                if neigh_cell.cost < min_cost:
                    min_neighbour = neigh_cell
                    min_cost = neigh_cell.cost
        
        x_vector = min_neighbour.x_pos - x_pos
        y_vector = min_neighbour.y_pos - y_pos
        if abs(x_vector) == 1 and abs(y_vector) == 1:
            x_vector = normalized_vec * x_vector
            y_vector = normalized_vec * y_vector

        cell = self.grid[y_pos][x_pos]
        cell.x_vector = x_vector
        cell.y_vector = y_vector

        assert -1 <= abs(x_vector) <= 1 and -1 <= abs(y_vector) <= 1, f"VECTORERROR"
    

    #Assign colors based on the cost of cells 
    def get_cell_colours(self, visited):
        for y_pos in range(self.map_height):
            for x_pos in range(self.map_width):
                cell = self.grid[y_pos][x_pos]
                
                if cell.type == source:
                    cell.color = source_color
                    continue
                
                if cell.type == wall:
                    continue

                if (y_pos, x_pos) not in visited:
                    cell.color = unreachable_cell_color
                    continue

                #All the non path cells have now been filtered out
                #The blueTone and redTone are calculated using linear functions
                
                k = (self.map_height + self.map_height) * 1.5 
                redTone = max(0, (-heatmap_redness/k) * cell.cost + heatmap_redness) #Decreasing function
                blueTone = min(heatmap_blueness, heatmap_blueness/k * cell.cost) #Increasing function
                cell.color = (redTone, 0, blueTone)


    def avg_neighbour_kernel(self, y_pos, x_pos):
        cell = self.grid[y_pos][x_pos]
        y_vector = 0
        x_vector = 0
        for y_pos2 in range(y_pos-1, y_pos+2):
            for x_pos2 in range(x_pos-1, x_pos+2):
                if (not (0 <= y_pos2 < self.map_height) or not (0 <= x_pos2 < self.map_width)):
                    continue

                cell = self.grid[y_pos2][x_pos2]
                x_vector += cell.x_vector
                y_vector += cell.y_vector
        
        x_vector /= 8
        y_vector /= 8
        cell.x_vector = x_vector
        cell.y_vector = y_vector

        assert -1 <= abs(x_vector) <= 1 and -1 <= abs(y_vector) <= 1, f"VECTORERROR"          
    

        
