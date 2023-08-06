from ._color import normalize_color


class Object:
    pass


class Mesh(Object):
    def __init__(self, mesh, name=None):
        self.mesh = mesh
        self.name = name


class Line(Object):
    def __init__(self, polyline, color):
        # Validate.
        normalize_color(color)

        self.polyline = polyline
        self.color = color


class Point(Object):
    def __init__(self, point, color, name=None):
        # Validate.
        normalize_color(color)

        self.point = point
        self.name = name
        self.color = color
