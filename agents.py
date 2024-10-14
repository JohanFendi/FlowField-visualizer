import pygame as pg

VELOCITY = 0.1
AGENT_COLOR = (0,255,0)
AGENT_RADIUS = 5

class Agent:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vector = 0
        self.y_vector = 0
        self.velocity = VELOCITY
        self.color = AGENT_COLOR
        self.radius = AGENT_RADIUS

    def update_vectors(self, flow_field):
        assert 0 <= self.x_pos <= flow_field.map_width, f"INDEXERROR: CURRENT X_POS : {self.x_pos} MAP_WIDTH : {flow_field.map_width}"
        assert 0 <= self.y_pos <= flow_field.map_height, f"INDEXERROR: CURRENT Y_POS : {self.y_pos} MAP_HEIGHT : {flow_field.map_height}"
        self.x_vector = flow_field.grid[int(self.y_pos)][int(self.x_pos)].x_vector
        self.y_vector = flow_field.grid[int(self.y_pos)][int(self.x_pos)].y_vector

    def move(self, flow_field):
        self.update_vectors(flow_field)
        self.x_pos += self.x_vector * self.velocity
        self.y_pos += self.y_vector * self.velocity
       
    def draw(self, window, cell_width):
        x_cord = self.x_pos * cell_width
        y_cord = self.y_pos * cell_width
        pg.draw.circle(window, self.color, (x_cord, y_cord), self.radius)
 