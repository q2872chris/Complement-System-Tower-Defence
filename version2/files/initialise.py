from files.protein_information import get_data
from files.proteins import protein, tower
from files.data import window_data as win
from files.components import grid_square

def shop_grid():
    b = win.box_width
    x, y = win.game_width, win.grid_panel_height - b
    protein_data = get_data(True)
    data = sorted(protein_data.items(), key=lambda k: k[1]["shop"], reverse=True)
    grid = []
    pointer = 0
    for name, attrs in data:
        if attrs["shop"]:
            attrs["position"] = [x + b / 2, y + b / 2]
            grid.append(grid_square(x, y, type(name, (protein, tower), attrs)))
            if not pointer % 2:
                x += b
            else:
                x -= b
                y -= b
            pointer += 1
        else:
            type(name, (protein, tower), attrs)
    if pointer % 2:
        grid.append(grid_square(x, y, None))
    d1 = win.grid_panel_height - 2 * win.scroller_radius
    d2 = win.box_width * (pointer // 2) - win.grid_panel_height + win.box_width + win.border_width
    speed = d2 / d1     # calculate scroller speed based on grid height
    return grid, speed
