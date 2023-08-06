from ._scene_internal import Line, Mesh, Point


class Scene:
    """
    Simple scenegraph for quickly debugging 3D meshes, polylines, and points.

    Args:
        point_radius (float): The desired radius of the markers that are
            rendered for points. The default is `1.0`.
    """

    def __init__(self, point_radius=1.0):
        self.point_radius = point_radius
        self.children = []

    def add_meshes(self, *meshes):
        """
        Add one or more meshes to the scene.

        Args:
            meshes (list): One or more instances of `lacecore.Mesh`.

        Return:
            Self for chaining.

        See also:
            https://lacecore.readthedocs.io/en/latest/
        """
        for mesh in meshes:
            self.children.append(Mesh(mesh=mesh))
        return self

    def add_lines(self, *polylines, color="red"):
        """
        Add one or more polylines to the scene.

        Args:
            polylines (list): One or more instances of `polliwog.Polyline`.
            color (object): A CSS named color or an tuple of RGB values,
                scaled from 0 to 1.

        Return:
            Self for chaining.

        See also:
            https://polliwog.readthedocs.io/en/latest/
        """
        for polyline in polylines:
            self.children.append(Line(polyline=polyline, color=color))
        return self

    def add_points(self, *points, name=None, color="red"):
        """
        Add one or more points to the scene.

        Args:
            points (list): One or more `(3,)` NumPy arrays or a `kx3` array.
            name (str): The name of a point to add. Do not use this when providing
                more than one point.
            color (object): A CSS named color or an tuple of RGB values,
                scaled from 0 to 1.

        Return:
            Self for chaining.
        """
        if len(points) > 0 and name is not None:
            raise ValueError(
                "When more than one point is provided, expected `name` to be None"
            )
        for point in points:
            self.children.append(Point(point, name=name, color=color))
        return self

    def write(self, filename):
        """
        Write a COLLADA file for this scene.

        Args:
            filename (str): The filename to write (e.g. `debug.dae`).
        """
        import os
        from ._collada import collada_from_scene

        _, extension = os.path.splitext(filename)
        if extension != ".dae":
            raise ValueError("Expected filename to end with .dae")

        dae = collada_from_scene(self)
        dae.write(filename)
