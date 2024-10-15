import pygame as pg

source = "source"


#Gets mouseclicks and either draws walls ord erases walls
def user_wall_placement(flow_field, draw_mode):
    mouse_buttons = pg.mouse.get_pressed() 
    if mouse_buttons[0]:
        pos = pg.mouse.get_pos()
        x_pos, y_pos = pos[0] // flow_field.cell_width, pos[1] // flow_field.cell_width
        if (0 <= x_pos < flow_field.map_width) and (0 <= y_pos < flow_field.map_height):
            cell = flow_field.grid[y_pos][x_pos]
            if cell.type != source:
                cell.change_type(draw_mode)


#User moves source with ASWD
def user_move_source(flow_field):
    keys = pg.key.get_pressed()
    if keys[pg.K_a] and flow_field.source.x_pos > 0:
        flow_field.update_source(flow_field.source.x_pos-1, flow_field.source.y_pos)

    if keys[pg.K_w] and flow_field.source.y_pos > 0:
        flow_field.update_source(flow_field.source.x_pos, flow_field.source.y_pos-1)

    if keys[pg.K_d] and flow_field.source.x_pos < flow_field.map_width - 1:
        flow_field.update_source(flow_field.source.x_pos+1, flow_field.source.y_pos)

    if keys[pg.K_s] and flow_field.source.y_pos < flow_field.map_height - 1:
        flow_field.update_source(flow_field.source.x_pos, flow_field.source.y_pos+1)


#Handels quiting and toggling on and of the draw mode
def event_handler(running, draw_mode):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                draw_mode = not draw_mode
            if event.key == pg.K_q:
                running = False
    
    return running, draw_mode