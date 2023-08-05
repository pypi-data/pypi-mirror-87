"""Trivial drawing aids (box, line, ellipse)."""

import ast

from gaphas.item import NW, Element
from gaphas.item import Line as _Line
from gaphas.util import path_ellipse

from gaphor.core.modeling import Presentation
from gaphor.diagram.shapes import stroke


class Line(Presentation, _Line):
    def __init__(self, id=None, model=None):
        super().__init__(id, model)
        self.fuzziness = 2
        self._handles[0].connectable = False
        self._handles[-1].connectable = False

    def save(self, save_func):
        save_func("matrix", tuple(self.matrix))
        for prop in ("orthogonal", "horizontal"):
            save_func(prop, getattr(self, prop))
        points = [tuple(map(float, h.pos)) for h in self.handles()]
        save_func("points", points)

    def load(self, name, value):
        if name == "horizontal":
            self.horizontal = ast.literal_eval(value)
        elif name == "matrix":
            self.matrix = ast.literal_eval(value)
        elif name == "orthogonal":
            self._load_orthogonal = ast.literal_eval(value)
        elif name == "points":
            points = ast.literal_eval(value)
            for _ in range(len(points) - 2):
                h = self._create_handle((0, 0))
                self._handles.insert(1, h)
            for i, p in enumerate(points):
                self.handles()[i].pos = p
            self._update_ports()

    def postload(self):
        if hasattr(self, "_load_orthogonal"):
            self.orthogonal = self._load_orthogonal
            del self._load_orthogonal

    def draw(self, context):
        cr = context.cairo
        style = context.style
        self.line_width = style["line-width"]
        if style["color"]:
            cr.set_source_rgba(*style["color"])
        super().draw(context)


class Box(Presentation, Element):
    """A Box has 4 handles (for a start)::

    NW +---+ NE SW +---+ SE
    """

    def __init__(self, id=None, model=None):
        super().__init__(id, model)

    def save(self, save_func):
        save_func("matrix", tuple(self.matrix))
        save_func("width", self.width)
        save_func("height", self.height)

    def load(self, name, value):
        if name == "matrix":
            self.matrix = ast.literal_eval(value)
        elif name == "width":
            self.width = ast.literal_eval(value)
        elif name == "height":
            self.height = ast.literal_eval(value)

    def postload(self):
        pass

    def draw(self, context):
        cr = context.cairo
        nw = self._handles[NW]
        cr.rectangle(nw.pos.x, nw.pos.y, self.width, self.height)
        stroke(context)


class Ellipse(Presentation, Element):
    """"""

    def __init__(self, id=None, model=None):
        super().__init__(id, model)

    def save(self, save_func):
        save_func("matrix", tuple(self.matrix))
        save_func("width", self.width)
        save_func("height", self.height)

    def load(self, name, value):
        if name == "matrix":
            self.matrix = ast.literal_eval(value)
        elif name == "width":
            self.width = ast.literal_eval(value)
        elif name == "height":
            self.height = ast.literal_eval(value)

    def postload(self):
        pass

    def draw(self, context):
        cr = context.cairo

        rx = self.width / 2.0
        ry = self.height / 2.0

        cr.move_to(self.width, ry)
        path_ellipse(cr, rx, ry, self.width, self.height)
        stroke(context)
