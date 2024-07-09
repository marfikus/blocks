
from typing import List
from angle import Angle
from coords import Coords
from two_coords_arrays import TwoCoordsArrays
from figure import Figure


class Map:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.figures: List[Figure] = []
        self.busy_cells_map: List[List[bool]] = self._init_busy_cells_map()
        
        
    def _init_busy_cells_map(self) -> List[List[bool]]:
        map = []
        for y in range(self.height):
            map.append([])
            for x in range(self.width):
                map[y].append(False)
        return map
    
    
    def show(self):
        add_space: str = " "
        
        print(f" {add_space}{('-' + add_space) * self.width}")
        
        for string in self.busy_cells_map:
            cells_str = ""
            for cell in string:
                # cells_str += f"o{add_space}" if cell else f" {add_space}"
                if cell:
                    cells_str += "o" + add_space
                else:
                    cells_str += " " + add_space
            print(f"|{add_space}{cells_str}|")
            
        print(f" {add_space}{('-' + add_space) * self.width}")
        
    
    def add_figure(self, f: Figure, x: int, y: int):
        if self._figure_is_exists_on_map(f):
            print("This figure is already exists on map!")
            return
            
        if not self._is_valid_figure_size(f):
            return
            
        if not self._is_valid_figure_position(f, x, y):
            return
            
        blocks_coords: List[Coords] = f.get_blocks_coords()
        rel_coords: List[Coords] = []
        
        for block_coords in blocks_coords:
            rel_x = block_coords.x + x
            rel_y = block_coords.y + y
            
            if self._cell_is_busy(rel_x, rel_y):
                print("Busy cell!")
                return
            else:
                rel_coords.append(Coords(rel_x, rel_y))
        
        self._set_busy_cells(rel_coords, True)
        self.figures.append(f)
        f.map_link = self
        f.x = x
        f.y = y
        
    
    def remove_figure(self, f: Figure):
        if not self._figure_is_exists_on_map(f):
            print("This figure is not exists on map!")
            return
            
        blocks_coords: List[Coords] = f.get_blocks_coords()
        
        for block_coords in blocks_coords:
            rel_x = block_coords.x + f.x
            rel_y = block_coords.y + f.y
            self.busy_cells_map[rel_y][rel_x] = False
            
        self.figures.remove(f)
        
        f.map_link = None
        f.x = 0
        f.y = 0
        
        
    # todo: можно добавить moveFigureLeft/Right/Up/Down(), где будет вызываться moveFigure()
    def move_figure(self, f: Figure, new_x: int, new_y: int):
        # Проверяем наличие фигуры на карте
        if not self._figure_is_exists_on_map(f):
            print("This figure is not exists on map!")
            return

        # Проверяем возможность новой позиции (не выходит ли за границы карты)
        if not self._is_valid_figure_position(f, new_x, new_y):
            return
            
        # Вычисляем массивы координат относительно текущей и новой позиции фигуры
        rel_coords_arrays: TwoCoordsArrays = self._get_rel_blocks_coords(
            TwoCoordsArrays(f.get_blocks_coords(), f.get_blocks_coords()),
            Coords(f.x, f.y),
            Coords(new_x, new_y)
        )
        
        # Проверяем возможность перемещения фигуры в новую позицию (свободны ли ячейки на карте)
        if not self._all_cells_is_empty(rel_coords_arrays):
            print("Busy cell!")
            return
            
        # Обновляем массив занятых ячеек
        self._set_busy_cells(rel_coords_arrays.first, False)
        self._set_busy_cells(rel_coords_arrays.second, True)
        
        # Обновляем позицию фигуры
        f.x = new_x
        f.y = new_y
        
        
    def rotate_figure(self, f: Figure, angle: Angle):
        # Проверяем наличие фигуры на карте
        if not self._figure_is_exists_on_map(f):
            print("This figure is not exists on map!")
            return
            
        # Создаём поворот фигуры (сама фигура не изменяется, пока не применим этот поворот, после проверок)
        f.make_rotation(angle)
        
        # Проверяем возможность новой позиции (не выходит ли за границы карты)
        if not self._is_valid_figure_position(f, True):
            return
            
        # Вычисляем массивы координат относительно текущей позиции фигуры
        rel_coords_arrays: TwoCoordsArrays = self._get_rel_blocks_coords(
            TwoCoordsArrays(
                f.get_blocks_coords(), 
                f.rotation.get_blocks_coords()
            ),
            Coords(f.x, f.y),
            Coords(f.x, f.y)
        )
        
        # Проверяем возможность поворота фигуры (свободны ли ячейки на карте)
        if not self._all_cells_is_empty(rel_coords_arrays):
            print("Busy cell!")
            return
            
        # Обновляем массив занятых ячеек
        self._set_busy_cells(rel_coords_arrays.first, False)
        self._set_busy_cells(rel_coords_arrays.second, True)
        
        # Применяем поворот фигуры
        f.apply_rotation()


    def _get_rel_blocks_coords(self, coords_arrays: TwoCoordsArrays, cur_pos: Coords, new_pos: Coords) -> TwoCoordsArrays:
        cur_blocks_coords: List[Coords] = coords_arrays.first
        new_blocks_coords: List[Coords] = coords_arrays.second
        
        cur_rel_blocks_coords: List[Coords] = []
        new_rel_blocks_coords: List[Coords] = []
        
        for i in range(len(cur_blocks_coords)):
            cur_rel_blocks_coords.append(Coords(
                cur_blocks_coords[i].x + cur_pos.x,
                cur_blocks_coords[i].y + cur_pos.y,
            ))
            new_rel_blocks_coords.append(Coords(
                new_blocks_coords[i].x + new_pos.x,
                new_blocks_coords[i].y + new_pos.y,
            ))
            
        return TwoCoordsArrays(cur_rel_blocks_coords, new_rel_blocks_coords)
        
        
    def _all_cells_is_empty(self, coords_arrays: TwoCoordsArrays) -> bool:
        cur_rel_blocks_coords: List[Coords] = coords_arrays.first
        new_rel_blocks_coords: List[Coords] = coords_arrays.second
        
        for i in range(len(new_rel_blocks_coords)):
            x: int = new_rel_blocks_coords[i].x
            y: int = new_rel_blocks_coords[i].y
            
            if self._cell_is_busy(x, y):
                is_busy_of_this_figure: bool = False
                
                for j in range(len(cur_rel_blocks_coords)):
                    if (cur_rel_blocks_coords[j].y == y) and (cur_rel_blocks_coords[j].x == x):
                        # если занята этой фигурой, то норм (она потом освободится)
                        is_busy_of_this_figure = True
                        break
                
                if not is_busy_of_this_figure:
                    return False
        
        return True

    
    def _cell_is_busy(self, x: int, y: int) -> bool:
        return self.busy_cells_map[y][x]


    def _set_busy_cells(self, rel_coords: List[Coords], state: bool):
        for rel_coord in rel_coords:
            x = rel_coord.x
            y = rel_coord.y
            self.busy_cells_map[y][x] = state


    def _figure_is_exists_on_map(self, f: Figure) -> bool:
        return f.map_link == self


    def _is_valid_figure_size(self, f: Figure) -> bool:
        if (f.width < 1) or (f.height < 1):
            print("Invalid figure size!")
            return False
            
        if (f.width > self.width) or (f.height > self.height):
            print("Figure size > map size!")
            return False
            
        return True


    def _is_valid_figure_position(self, f: Figure, x: int | None=None, y: int | None=None, rotation: bool=False) -> bool:
        if x is None: x = f.x
        if y is None: y = f.y
    
        figure_width: int
        figure_height: int
        if rotation:
            figure_width = f.rotation.width
            figure_height = f.rotation.height
        else:
            figure_width = f.width
            figure_height = f.height
            
        map_width = self.width
        map_height = self.height
        
        if (x < 0) or (y < 0):
            print("Invalid figure position!")
            return False
            
        if ((x + figure_width) > map_width) or ((y + figure_height) > map_height):
            print("Invalid figure position!")
            return False
        
        return True
