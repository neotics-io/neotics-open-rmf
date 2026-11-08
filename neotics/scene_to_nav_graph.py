"""Turn a Neotics Scene's waypoints and lanes into an Open-RMF traffic graph.

    python scene_to_nav_graph.py samples/depot.scene.json depot.nav.yaml

Lanes run both ways. A waypoint named "charger" is marked as a charger, and "dock" as a parking spot.
"""
import sys

import yaml

from neotics_scene import Scene

LEVEL = "L1"


def to_nav_graph(scene: Scene) -> dict:
    names = list(scene.waypoints)
    vertices = []
    for name in names:
        x, y = scene.waypoints[name]
        vertices.append([x, y, {
            "name": name,
            "is_charger": name == "charger",
            "is_parking_spot": name == "dock",
            "is_holding_point": name in ("dock", "charger"),
        }])
    lanes = []
    for a, b in scene.lanes:
        i, j = names.index(a), names.index(b)
        lanes += [[i, j, {"speed_limit": 0.0}], [j, i, {"speed_limit": 0.0}]]
    return {"building_name": scene.name, "levels": {LEVEL: {"vertices": vertices, "lanes": lanes}}}


if __name__ == "__main__":
    with open(sys.argv[2], "w", encoding="utf-8") as out:
        yaml.safe_dump(to_nav_graph(Scene.load(sys.argv[1])), out, sort_keys=False, default_flow_style=None)
