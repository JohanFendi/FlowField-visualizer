import pygame as pg
from flowfield import *
from agents import *


cell_width = 20
map_width = 60
map_height = 30
window_height = cell_width * map_height
window_width = cell_width * map_width
source_x = 7
source_y = 7

fps = 60
draw_mode = True


def user_wall_placement(flow_field, draw_mode):
    mouse_buttons = pg.mouse.get_pressed() 
    if mouse_buttons[0]:
        pos = pg.mouse.get_pos()
        x_cord, y_cord = pos[0] // cell_width, pos[1] // cell_width
        if (0 <= x_cord < map_width) and (0 <= y_cord < map_height):
            cell = flow_field.grid[y_cord][x_cord]
            if cell.type != Cell.source:
                cell.change_type(draw_mode)

def user_move_source(flow_field):
    keys = pg.key.get_pressed()
    if keys[pg.K_a] and flow_field.source.x_cord > 0:
        flow_field.update_source(flow_field.source.x_cord-1, flow_field.source.y_cord)

    if keys[pg.K_w] and flow_field.source.y_cord > 0:
        flow_field.update_source(flow_field.source.x_cord, flow_field.source.y_cord-1)

    if keys[pg.K_d] and flow_field.source.x_cord < flow_field.map_width - 1:
        flow_field.update_source(flow_field.source.x_cord+1, flow_field.source.y_cord)

    if keys[pg.K_s] and flow_field.source.y_cord < flow_field.map_height - 1:
        flow_field.update_source(flow_field.source.x_cord, flow_field.source.y_cord+1)

    print(flow_field.source.x_cord, flow_field.source.y_cord)


def main(clock, fps, flow_field, window, draw_mode):
    running = True

    a = Agent(18, 10)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    draw_mode = not draw_mode
                if event.key == pg.K_q:
                    running = False

  
        user_move_source(flow_field)
        user_wall_placement(flow_field, draw_mode)
        flow_field.generate_cost_field()
        flow_field.generate_vector_field()
        flow_field.draw(window)

        a.move(flow_field)
        a.draw(window, flow_field.cell_width)
        
        draw = "ON" if draw_mode else "OFF"
        erase = "OFF" if draw_mode else "ON"
        caption_strings =   ["Left click to draw", f"Draw: {draw}", 
                            f"Eraser: {erase}", "PRESS C to switch between draw and erase",
                            "PRESS Q to quit"  
                            ]

        pg.display.set_caption(" | ".join(caption_strings))
        pg.display.update()
        clock.tick(fps)


def print_vecs1(flow_field):
    for row in flow_field.grid:
        for cell in row:
            print(round(cell.y_vector,2), round(cell.x_vector,2), end = "  ")
        print()


if __name__ == "__main__":  
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((window_width, window_height))
    flow_field = Flow_field(map_width, map_height, cell_width, source_x, source_y)
    main(clock, fps, flow_field, window, draw_mode)
   



 