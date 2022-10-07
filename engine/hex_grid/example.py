"""
Example of using hexutil.
A simple roguelike kernel written in PyQt5.
"""
import random
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
import hexutil

class Level(object):
    """Represents a level in the game.
    Currently there is only one.
    """

    def __init__(self, size):
        """Create level with a random walk"""
        tiles = {}

        # for i in range(size):
        #
        #     print(i)
        tile_list = []


        # i = 0
        # for width in range(size * 2):
        #     print("---------------------------------------------")
        #     print(f"i{i}")
        #     _width = None
        #
        #     if width / 2 < i:
        #         print(f"{width} > {width / 2} = ?")
        #         _width = - (width / 2)
        #         print(_width)
        #     elif width < size:
        #         _width = width / 2
        #         print(_width)
        #     i+=1
        #     # time.sleep(14000)
        #     # for heigh in range(size):
        #     #
        #     #     if (width + heigh) % 2 == 0:
        #     #
        #     #         tile = hexutil.Hex(width, heigh)
        #     #         tile_list.append(tile)
        #

        for _x in range(size * 2):

            if _x < size:
                # print(_x)
                # results[-_x] = {_x}
                res_x = -_x
            else:
                # results[int(_x - (x /2))] = {_x}
                res_x = int(_x - (size))

            for _y in range(size):

                if _y < size / 2:
                    # print(_x)
                    # results[-_x] = {_x}
                    res_y = -_y
                else:
                    # results[int(_x - (x /2))] = {_x}
                    res_y = int(_y - (size / 2))
                if (res_x + res_y) % 2 == 0:
                    tile = hexutil.Hex(int(res_x), int(res_y))
                    tile_list.append(tile)

        for tile in tile_list:
            tiles[tile] = '.'

        obstacle_amount = random.randint(1,7)

        for obstacle in range(obstacle_amount):
            obstacle_size = random.randint(1,10)

            for tile in hexutil.origin.random_walk(obstacle_size, tile_list):
                tiles[tile] = '~' # add water

        # for tile in hexutil.origin.random_walk(size):
        #     tiles[tile] = '.' # add floor tiles
        self.tiles = tiles
        self.seen_tiles = {}

    def get_tile(self, hexagon):
        return self.tiles.get(hexagon, '#')

    def get_seen_tile(self, hexagon):
        return self.seen_tiles.get(hexagon, ' ')

    def is_passable(self, hexagon):
        return self.get_tile(hexagon) not in '#~'

    def is_transparent(self, hexagon):
        return self.get_tile(hexagon) != '#'
 
    def update_fov(self, fov):
        for hexagon in fov:
            self.seen_tiles[hexagon] = self.get_tile(hexagon)


class GameWidget(QtWidgets.QWidget):
    """The Qt Widget which shows the game."""

    _tile_brushes = {
            '.' : QtGui.QBrush(QtGui.QImage('img/grass.jpg')),
            '~' : QtGui.QBrush(QtGui.QColor("brown")),
            '#' : QtGui.QBrush(QtGui.QColor("brown")),
            }

    selected_hexagon = None
    selected_path = frozenset()

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.setMouseTracking(True) # we want to receive mouseMoveEvents

        self.level = Level(35)
        self.player = hexutil.origin
        self.hexgrid = hexutil.HexGrid(24)

        # initialize GUI objects needed for painting
        self.font = QtGui.QFont("Helvetica", 20)
        self.font.setStyleHint(QtGui.QFont.SansSerif)
        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.select_brush = QtGui.QBrush(QtGui.QColor(127, 127, 255, 127))
        self.unseen_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 127))

        self.update_fov()

    def update_fov(self):
        self.fov = self.player.field_of_view(transparent=self.level.is_transparent, max_distance=100)
        self.level.update_fov(self.fov)

    def hexagon_of_pos(self, pos):
        """Compute the hexagon at the screen position."""
        size = self.size()
        xc = size.width()//2
        yc = size.height()//2
        return self.player + self.hexgrid.hex_at_coordinate(pos.x() - xc, pos.y() - yc)

    def mousePressEvent(self, event):
        hexagon = self.hexagon_of_pos(event.pos())
        path = self.player.find_path(hexagon, self.level.is_passable)
        if path and len(path) >= 2:
            self.player = path[1]
            self.update_fov()
            self.select_hexagon(event.pos())
            self.repaint()

    def mouseMoveEvent(self, event):
        self.select_hexagon(event.pos())

    def select_hexagon(self, pos):
        """Select hexagon and path to hexagon at position."""
        hexagon = self.hexagon_of_pos(pos)
        if hexagon != self.selected_hexagon:
            self.selected_hexagon = hexagon
            path = self.player.find_path(hexagon, self.level.is_passable)
            if path is None:
                self.selected_path = frozenset()
            else:
                self.selected_path = frozenset(path[1:])
            self.repaint()
 
    def paintEvent(self, event):
        # compute center of window
        size = self.size()
        xc = size.width()//2
        yc = size.height()//2
        # bounding box when we translate the origin to be at the center
        bbox = hexutil.Rectangle(-xc, -yc, size.width(), size.height())
        hexgrid = self.hexgrid
        painter = QtGui.QPainter()
        painter.begin(self)
        try:
            # paint background black
            painter.save()
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor())
            painter.drawRect(0, 0, size.width(), size.height())
            painter.restore()

            # set up drawing state
            painter.setPen(self.pen)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
            painter.setFont(self.font)
            painter.translate(xc, yc)
            # draw each hexagon which is in the window
            for hexagon in hexgrid.hexes_in_rectangle(bbox):
                polygon = QtGui.QPolygon([QtCore.QPoint(*corner) for corner in hexgrid.corners(hexagon)])
                hexagon2 = hexagon + self.player
                tile = self.level.get_seen_tile(hexagon2)
                if tile == ' ':
                    continue
                painter.setBrush(self._tile_brushes[tile])
                painter.drawPolygon(polygon)
                if hexagon2 not in self.fov:
                    painter.setBrush(self.unseen_brush)
                    painter.drawPolygon(polygon)
                if hexagon2 in self.selected_path:
                    painter.setBrush(self.select_brush)
                    painter.drawPolygon(polygon)
                if hexagon2 == self.player:
                    rect = hexgrid.bounding_box(hexagon)
                    rect = QtCore.QRectF(*rect) # convert to Qt RectF
                    painter.drawText(rect, QtCore.Qt.AlignCenter, '@')
        finally:
            painter.end()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GameWidget()
    window.show()
    app.exec_()

main()
