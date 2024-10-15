from flowfield import *
from agents import *
from userInput import * 

import pygame as pg

pg.init()


fps = 60

#Cell width in pixels
cell_width = 20

#Map dimensions in number of cells.
map_width = 60
map_height = 30

#Window dimmensions.
window_height = cell_width * map_height
window_width = cell_width * map_width

#Starting position of the source.
source_x = 7
source_y = 7


#Sets caption of pygame window.
def set_display_caption(draw_mode):
    draw = "ON" if draw_mode else "OFF"
    erase = "OFF" if draw_mode else "ON"
    caption_strings =   ["Left click to draw", f"Draw: {draw}", 
                        f"Eraser: {erase}", "PRESS C to switch between draw and erase",
                        "PRESS Q to quit"  
                        ]

    pg.display.set_caption(" | ".join(caption_strings))


#Main game loop
def main(clock, fps, flow_field, window):
    running = True
    draw_mode = True
    a = Agent(18, 10)
    while running:
        running, draw_mode = event_handler(running, draw_mode)
        user_move_source(flow_field)
        user_wall_placement(flow_field, draw_mode)
        flow_field.generate_integration_field()
        flow_field.generate_vector_field()
        flow_field.draw(window)

        a.move(flow_field)
        a.draw(window, flow_field.cell_width)
        
        set_display_caption(draw_mode)
        pg.display.update()
        clock.tick(fps)


#Function for printing vector values (debbuging tool)
def print_vecs1(flow_field):
    for row in flow_field.grid:
        for cell in row:
            print(round(cell.y_vector,2), round(cell.x_vector,2), end = "  ")
        print()


if __name__ == "__main__":  
    clock = pg.time.Clock()
    window = pg.display.set_mode((window_width, window_height))
    flow_field = Flow_field(map_width, map_height, cell_width, source_x, source_y)
    main(clock, fps, flow_field, window)
   



 