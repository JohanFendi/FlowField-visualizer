import pygame as pg

#Agent constants
agent_velocity = 0.1
agent_color = (0,255,0)
agent_radius = 5


class Agent:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vector = 0
        self.y_vector = 0
        self.velocity = agent_velocity
        self.color = agent_color
        self.radius = agent_radius


    #Sets the vector of the agent to the vector of the current cell.
    def update_vectors(self, flow_field):
        assert 0 <= self.x_pos <= flow_field.map_width, f"INDEXERROR: CURRENT X_POS : {self.x_pos} MAP_WIDTH : {flow_field.map_width}"
        assert 0 <= self.y_pos <= flow_field.map_height, f"INDEXERROR: CURRENT Y_POS : {self.y_pos} MAP_HEIGHT : {flow_field.map_height}"
        self.x_vector = flow_field.grid[int(self.y_pos)][int(self.x_pos)].x_vector
        self.y_vector = flow_field.grid[int(self.y_pos)][int(self.x_pos)].y_vector


    # Updates the agent's position by applying its velocity in the direction of its vector.
    def move(self, flow_field):
        self.update_vectors(flow_field)
        self.x_pos += self.x_vector * self.velocity
        self.y_pos += self.y_vector * self.velocity
       
       
    #Draws the agent as a circle. 
    def draw(self, window, cell_width):
        x_cord = self.x_pos * cell_width
        y_cord = self.y_pos * cell_width
        pg.draw.circle(window, self.color, (x_cord, y_cord), self.radius)
 