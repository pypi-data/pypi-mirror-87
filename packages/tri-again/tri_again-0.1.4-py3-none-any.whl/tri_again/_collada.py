from collada import Collada
from collada.geometry import Geometry
from collada.material import Effect, Material
from collada.scene import GeometryNode, MaterialNode, Node, Scene
from collada.source import FloatSource, InputList
import numpy as np
from polliwog import Polyline
from toolz import groupby
import vg
from ._color import normalize_color
from ._scene_internal import (
    Line as InternalLine,
    Mesh as InternalMesh,
    Point as InternalPoint,
)


def create_material(collada, name, color=(1, 1, 1)):
    effect = Effect(
        f"{name}_effect",
        [],
        "lambert",
        diffuse=color,
        specular=(0, 0, 0),
        double_sided=True,
    )
    material = Material(name, name, effect)
    collada.effects.append(effect)
    collada.materials.append(material)
    return MaterialNode(name, material, inputs=[])


def geometry_node_from_mesh(collada, mesh, name):
    vertex_source_name = f"{name}_verts"
    geometry = Geometry(
        collada,
        name or "geometry0",
        str(mesh),
        [FloatSource(vertex_source_name, mesh.v.ravel(), ("X", "Y", "Z"))],
    )
    input_list = InputList()
    input_list.addInput(0, "VERTEX", f"#{vertex_source_name}")

    material_name = f"{name}_material"
    triset = geometry.createTriangleSet(mesh.f.ravel(), input_list, material_name)

    geometry.primitives.append(triset)
    collada.geometries.append(geometry)

    return GeometryNode(geometry, [create_material(collada, name=material_name)])


def geometry_node_from_segments(collada, vertices, edges, color, name, description):
    vg.shape.check(locals(), "vertices", (-1, 3))
    vg.shape.check(locals(), "edges", (-1, 2))

    vertex_source_name = f"{name}_verts"
    vertex_source = FloatSource(vertex_source_name, vertices, ("X", "Y", "Z"))
    geometry = Geometry(collada, name, description, [vertex_source])
    input_list = InputList()
    input_list.addInput(0, "VERTEX", f"#{vertex_source_name}")

    material_name = f"{name}_material"
    lineset = geometry.createLineSet(edges.ravel(), input_list, material_name)

    geometry.primitives.append(lineset)
    collada.geometries.append(geometry)

    return GeometryNode(
        geometry, [create_material(collada, name=material_name, color=color)]
    )


def geometry_node_from_polyline(collada, polyline, color, name):
    if not isinstance(polyline, Polyline):
        raise ValueError("Expected a Polyline")
    return geometry_node_from_segments(
        collada=collada,
        vertices=polyline.v,
        edges=polyline.e,
        color=color,
        name=name,
        description=str(polyline),
    )


def geometry_node_from_points(collada, points, radius, color, name):
    vg.shape.check(locals(), "points", (-1, 3))

    offset = radius * np.eye(3)
    segments = np.repeat(points, 6, axis=0).reshape(-1, 3, 2, 3)
    segments[:, :, 0] = segments[:, :, 0] + offset
    segments[:, :, 1] = segments[:, :, 1] - offset

    vertices = segments.reshape(-1, 3)
    edges = np.arange(len(vertices)).reshape(-1, 2)

    return geometry_node_from_segments(
        collada=collada,
        vertices=vertices,
        edges=edges,
        color=color,
        name=name,
        description=f"{len(points)} points",
    )


def collada_from_scene(scene, name="triagain"):
    collada = Collada()

    geometry_nodes = (
        [
            geometry_node_from_mesh(
                collada=collada,
                mesh=child.mesh,
                name=f"mesh_geometry_{i}",
            )
            for i, child in enumerate(
                child for child in scene.children if isinstance(child, InternalMesh)
            )
        ]
        + [
            geometry_node_from_polyline(
                collada,
                child.polyline,
                name=f"polyline_geometry_{i}",
                color=normalize_color(child.color),
            )
            for i, child in enumerate(
                child for child in scene.children if isinstance(child, InternalLine)
            )
        ]
        + [
            geometry_node_from_points(
                collada,
                points=np.array([point.point for point in points]),
                radius=scene.point_radius,
                color=normalize_color(color),
                name=f"point_geometry_{i}",
            )
            for i, (color, points) in enumerate(
                groupby(
                    lambda point: point.color,
                    [
                        child
                        for child in scene.children
                        if isinstance(child, InternalPoint)
                    ],
                ).items()
            )
        ]
    )

    scene = Scene(name, [Node("root", children=geometry_nodes)])
    collada.scenes.append(scene)
    collada.scene = scene
    return collada
