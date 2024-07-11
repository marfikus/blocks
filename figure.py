
from typing import Any, List
from angle import Angle
from block import Block
from coords import Coords
from rotation import Rotation
# from map import Map


class Figure:
    def __init__(self, title: str=""):
        self.title = title
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.blocks: List[Block] = []
        self.figure_map: List[List[Block | None]] = []
        self.rotation: Rotation = Rotation()
        self.map_link: Any = None


    def __str__(self):
        return (f"Figure '{self.title}': " 
                  f"x:{self.x}, "
                  f"y:{self.y}, "
                  f"width:{self.width}, "
                  f"height:{self.height}"
                # f"figure map:\n\t{self.show_map()}"
        )


    def add_block(self, new_block: Block, x: int, y: int):
        for block in self.blocks:
            if block.x == x and block.y == y:
                print(f"{self.title}: busy cell!")
                return
            
        new_block.x = x
        new_block.y = y
        self.blocks.append(new_block)
        self._update_figure_size()
        self._update_figure_map()
        # self.figure_map[x][y] = new_block


    def _update_figure_size(self):
        max_x: int = 0
        max_y: int = 0

        for block in self.blocks:
            if block.x > max_x: max_x = block.x
            if block.y > max_y: max_y = block.y

        self.width = max_x + 1
        self.height = max_y + 1


    def _update_figure_map(self):
        new_figure_map: List[List[Block | None]] = self._create_map(self.height, self.width)
                
        for block in self.blocks:
            new_figure_map[block.y][block.x] = block

        self.figure_map = new_figure_map

    
    def _create_map(self, h: int, w: int, value=None):
        map: List[List[Block | None]] = []

        for y in range(h):
            map.append([])
            for x in range(w):
                map[y].append(value)

        return map


    def show_map(self):
        print("----------------")
        for str in self.figure_map:
            for obj in str:
                if obj is None:
                    print(0, end=" ")
                else:
                    print(1, end=" ")
            print()
        print("----------------")


    def make_rotation(self, angle: Angle):
        self.rotation = Rotation()

        if angle == Angle.CLOCKWISE_90:
            self.rotation.figure_map = self._create_map(self.width, self.height) # меняем местами габариты
            self.rotation.width = self.height
            self.rotation.height = self.width

            # перекладываем ячейки
            for i in range(self.width): # i - по строкам новой карты и по столбцам старой
                k = self.height - 1 # j - по столбцам новой карты, k - по строкам старой
                for j in range(self.height):
                    self.rotation.figure_map[i][j] = self.figure_map[k][i]
                    k -= 1

        elif angle == Angle.COUNTERCLOCKWISE_90:
            self.rotation.figure_map = self._create_map(self.width, self.height) # меняем местами габариты
            self.rotation.width = self.height
            self.rotation.height = self.width

            # перекладываем ячейки
            k = self.width - 1 # k - по столбцам старой карты
            for i in range(self.width): # i - по строкам новой карты
                for j in range(self.height): # j - по столбцам новой карты и по строкам старой
                    self.rotation.figure_map[i][j] = self.figure_map[j][k]
                k -= 1

        elif angle == Angle.CLOCKWISE_180:
            self.rotation.figure_map = self._create_map(self.height, self.width) # в этом случае не меняем габариты
            self.rotation.width = self.width
            self.rotation.height = self.height

            # перекладываем ячейки
            n = self.height - 1 # n - по строкам старой карты
            for i in range(self.height): # i - по строкам новой карты
                k = self.width - 1 # j - по столбцам новой карты, k - по столбцам старой
                for j in range(self.width):
                    self.rotation.figure_map[i][j] = self.figure_map[n][k]
                    k -= 1
                n -= 1


        self.rotation.is_active = True

        # rotation.show_map()

        # match angle:
        #     case Angle.CLOCKWISE_90:
        #         print(1)
        #     case Angle.CLOCKWISE_180:
        #         print(2)


    def apply_rotation(self):
        if not self.rotation.is_active:
            print("No active rotation!")
            return
            
        self.width = self.rotation.width
        self.height = self.rotation.height
        self.figure_map = self.rotation.figure_map
        self._update_blocks_coords()
        self.rotation.is_active = False


    def _update_blocks_coords(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.figure_map[y][x] is not None:
                    # наверное так будет норм, поскольку в blocks и в figure_map находятся ссылки на одни и те же объекты
                    self.figure_map[y][x].x = x # type: ignore
                    self.figure_map[y][x].y = y # type: ignore


    def get_blocks_coords(self) -> List[Coords]:
        coords: List[Coords] = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.figure_map[y][x] != None:
                    coords.append(Coords(x, y))
        
        return coords
    
    
