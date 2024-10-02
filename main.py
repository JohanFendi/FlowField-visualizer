import pygame as pg
from flowfield import *



cell_width  = 20
map_width = 60
map_height = 30
window_height = cell_width * map_height
window_width = cell_width * map_width
source_x = 10
source_y = 10
fps = 60

draw_mode = True

def main(clock, fps, flow_field, window, draw_mode):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    draw_mode = not draw_mode
                if event.key == pg.K_q:
                    running = False


        mouse_buttons = pg.mouse.get_pressed()
        if mouse_buttons[0]:
            try:
                pos = pg.mouse.get_pos()
                x_cord, y_cord = pos[0] // cell_width, pos[1] // cell_width
                cell = flow_field.grid[y_cord][x_cord]
                if cell.type != Cell.source:
                    cell.change_type(draw_mode)
            except IndexError:
                print(f'INDEXERROR: Y = {y_cord} X = {x_cord}')


        flow_field.compute_distances()
        flow_field.draw(window)
        clock.tick(fps)
                
        draw_state = "ON" if draw_mode else "OFF"
        erase_state = "OFF" if draw_mode else "ON"


        caption_strings =   ["Left click to draw", f"Draw: {draw_state}", 
                            f"Eraser: {erase_state}", "PRESS C to switch between draw and erase",
                            "PRESS Q to quit"  
                            ]

        pg.display.set_caption(" | ".join(caption_strings))
        pg.display.update()


if __name__ == "__main__":  
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((window_width, window_height))
    flow_field = Flow_field(map_width, map_height, cell_width, source_x, source_y)
    flow_field.compute_distances()
    main(clock, fps, flow_field, window, draw_mode)