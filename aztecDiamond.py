from tile import Tile
from tuple_addition import tuple_add as tAdd
from tkinter import Canvas, Frame, BOTH
from random import random

class AztecDiamond(Frame):

    def __init__(self, x, y):
        super().__init__()
        self.n = 1
        self.tiles = []
        self.dimensions = (x, y)
        self.color_neutral = "orange"
        self.triag_color = "black"
        self.direction_colors = ["red", "green", "yellow", "blue"]
        self.direction_colored = False
        self.black = True
        self.initialize_draw()
        self.init_tiles()
        self.place()
    
    def init_tiles(self):
        i = random()
        if i < 0.5:
            self.tiles.append(Tile((0, 0), (0, -1), (1, 0)))
            self.tiles.append(Tile((-1, 0), (-1, -1), (-1, 0)))
        else:
            self.tiles.append(Tile((0, 0), (-1, 0), (0, 1)))
            self.tiles.append(Tile((0, -1), (-1, -1), (0, -1)))
    
    def grow(self):
        shift_dict = {} # dict that maps tile sources to shift directions to determine if two tiles shifted over each other
        free_tiles = [] # list that tracks all tiles that are free to fill

        self.n = self.n + 1
        n = self.n

        # register newgrown tiles
        for i in range(n):
            free_tiles.append((i, n-i-1))
            free_tiles.append((-i-1, i-n))
            free_tiles.append((i, -n+i))
            free_tiles.append((i-n, i))
        # register all tiles that will be shifting away as free (after the shift), and store the direction the shift will happen
        for tile in self.tiles:
            shift_dict[tile.coord_black] = tile.direction
            shift_dict[tile.coord_white] = tile.direction
            free_tiles.append(tile.coord_black)
            free_tiles.append(tile.coord_white)
        # performs the tile-shift and check for tiles that shifted over one another
        tiles_to_remove = []
        for tile in self.tiles:
            (c1, c2) = tile.shift()
            a = (0,0)
            b = (0,0)
            try:
                a = shift_dict[tile.coord_black]
                b = shift_dict[tile.coord_white]
            except:
                pass
            if (tAdd(a, tile.direction) == (0,0)) | (tAdd(b, tile.direction) == (0,0)):
                tiles_to_remove.append(tile)
            else:
                if c1 in free_tiles:
                    free_tiles.remove(c1)
                if c2 in free_tiles:
                    free_tiles.remove(c2)
        for tile in tiles_to_remove:
            self.tiles.remove(tile)
        while True:    
        # finds corners that correspond to squares that will have to be filled
            corners = {}
            for field in free_tiles:
                x = field[0]
                y = field[1]
                if not((x,y-1) in free_tiles):
                    if not((x-1,y) in free_tiles):
                        corners[(x,y)] = (x+1,y+1)
                    if not((x+1,y) in free_tiles):
                        corners[(x,y)] = (x-1,y+1)
                elif not((x,y+1) in free_tiles):
                    if not((x-1,y) in free_tiles):
                        corners[(x,y)] = (x+1,y-1)
                    if not((x+1,y) in free_tiles):
                        corners[(x,y)] = (x-1,y-1)
            # fills found squares with new tiles
            worked_on = []
            for corner in corners:
                i = random()
                (x, y) = corner
                (m, n) = corners[corner]
                if (x,y) in worked_on:
                    continue
                if i < 0.5:
                    if x < m:
                        direction_x = (-1, 0)
                        direction_m = (1, 0)
                    else:
                        direction_x = (1, 0)
                        direction_m = (-1, 0)
                    self.tiles.append(Tile((x, y), (x, n), direction_x))
                    self.tiles.append(Tile((m, y), (m, n), direction_m))
                else:
                    if y < n:
                        direction_y = (0, -1)
                        direction_n = (0, 1)
                    else:
                        direction_y = (0, 1)
                        direction_n = (0, -1)
                    self.tiles.append(Tile((x, y), (m, y), (direction_y)))
                    self.tiles.append(Tile((x, n), (m, n), (direction_n)))
                worked_on.append((x,y))
                worked_on.append((x,n))
                worked_on.append((m,y))
                worked_on.append((m,n))
            for coord in worked_on:
                free_tiles.remove(coord)
            if len(free_tiles) == 0:
                break

    def grow_and_draw(self):
        self.grow()
        self.place()

    def initialize_draw(self):
        self.initialize_draw_constants()
        self.master.title("Aztec Diamond")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def initialize_draw_constants(self):
        (x, y) = self.dimensions
        self.alpha = 0.9
        self.available_size = round(min(x, y)*self.alpha)
        self.corner = ((x-self.available_size)/2, (y-self.available_size)/2)

    def place(self):
        self.canvas.delete("all")

        (x, y) = self.corner
        dim = self.available_size
        n = self.n
        stepping = dim/(2*n)

        if self.black:
            self.draw_line_frame(0.12, x, y, dim, n, stepping)
        self.draw_tiles(0.14, x, y, dim, stepping)

        self.canvas.pack(fill=BOTH, expand=1)
    
    def draw_line_frame(self, thickness, x, y, dim, n, stepping):
        self.canvas.create_line(
            x+dim/2,
            y,
            x+dim/2,
            y+dim,
            width=thickness*stepping
            )
        self.canvas.create_line(
            x,
            y+dim/2,
            x+dim,
            y+dim/2,
            width=thickness*stepping
            )
        for i in range(n):
            self.canvas.create_rectangle(
                x+stepping*i,
                y+stepping*(n-i-1),
                x+stepping*(2*n-i),
                y+stepping*(n+i+1),
                width=thickness*stepping
                )

    def draw_tiles(self, spacing, x, y, dim, stepping):
        offset = stepping*spacing/2
        edge = stepping*(1-spacing)
        x_center = x+dim/2
        y_center = y+dim/2

        colors = {
            "white":    "#fff",
            "black":    "#000",
            "red":      "#f00",
            "green":    "#0f0",
            "blue":     "#00f",
            "yellow":   "#ff0",
            "cyan":     "#0ff",
            "magenta":  "#f0f",
            "orange":   "#f50"
            }
        if self.direction_colored:
            (up, down, left, right) = self.direction_colors
        else:
            (up, down, left, right) = [self.color_neutral] * 4
        triag_color = colors[self.triag_color]

        for tile in self.tiles:
            black = tile.coord_black
            white = tile.coord_white
            
            b_corner_x = (x_center + black[0]*stepping) + offset
            b_corner_y = (y_center + black[1]*stepping) + offset
            w_corner_x = (x_center + white[0]*stepping) + offset
            w_corner_y = (y_center + white[1]*stepping) + offset
            fill_corner_x = (x_center + (black[0] + white[0])/2 * stepping) + offset
            fill_corner_y = (y_center + (black[1] + white[1])/2 * stepping) + offset

            triag_radius = 0.35*edge
            triag_center_x = fill_corner_x + edge/2
            triag_center_y = fill_corner_y + edge/2
            triag_offset_height = 0.5*triag_radius
            triag_offset_width = 1.732050580/2*triag_radius

            x_peak = triag_center_x
            y_peak = triag_center_y
            x_left = triag_center_x
            y_left = triag_center_y
            x_right = triag_center_x
            y_right = triag_center_y
            direction = tile.direction
            if direction == (1, 0):
                x_peak += triag_radius
                x_left -= triag_offset_height
                x_right -= triag_offset_height
                y_left -= triag_offset_width
                y_right += triag_offset_width
                color = right
            elif direction == (0, 1):
                x_left += triag_offset_width
                x_right -= triag_offset_width
                y_peak += triag_radius
                y_left -= triag_offset_height
                y_right -= triag_offset_height
                color = down
            elif direction == (-1, 0):
                x_peak -= triag_radius
                x_left += triag_offset_height
                x_right += triag_offset_height
                y_left -= triag_offset_width
                y_right += triag_offset_width
                color = left
            elif direction == (0, -1):
                x_left += triag_offset_width
                x_right -= triag_offset_width
                y_peak -= triag_radius
                y_left += triag_offset_height
                y_right += triag_offset_height
                color = up

            self.canvas.create_rectangle(
                b_corner_x,
                b_corner_y,
                b_corner_x + edge,
                b_corner_y + edge,
                outline=colors[color],
                fill=colors[color]
                )
            self.canvas.create_rectangle(
                w_corner_x,
                w_corner_y,
                w_corner_x + edge,
                w_corner_y + edge,
                outline=colors[color],
                fill=colors[color]
                )
            self.canvas.create_rectangle(
                fill_corner_x,
                fill_corner_y,
                fill_corner_x + edge,
                fill_corner_y + edge,
                outline=colors[color],
                fill=colors[color]
                )
            if self.black:
                self.canvas.create_polygon(
                    x_peak,
                    y_peak,
                    x_left,
                    y_left,
                    x_right,
                    y_right,
                    outline=triag_color,
                    fill=triag_color
                )