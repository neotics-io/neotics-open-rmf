"""Full check inside ROS 2: Open-RMF's own parser reads the exported graph."""
import sys
import tempfile
from pathlib import Path

import rmf_adapter.geometry as geometry
import rmf_adapter.graph as graph
import rmf_adapter.vehicletraits as traits
import yaml

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))

from neotics_scene import Scene  # noqa: E402
from scene_to_nav_graph import to_nav_graph  # noqa: E402


def main() -> int:
    scene = Scene.load(KIT / "samples" / "depot.scene.json")
    path = Path(tempfile.mkdtemp()) / "depot.nav.yaml"
    path.write_text(yaml.safe_dump(to_nav_graph(scene), sort_keys=False), encoding="utf-8")

    vehicle = traits.VehicleTraits(
        linear=traits.Limits(0.7, 0.5),
        angular=traits.Limits(1.0, 1.0),
        profile=traits.Profile(geometry.make_final_convex_circle(0.25), geometry.make_final_convex_circle(0.3)),
    )
    parsed = graph.parse_graph(str(path), vehicle)

    assert parsed.num_waypoints == len(scene.waypoints), parsed.num_waypoints
    assert parsed.num_lanes == 2 * len(scene.lanes), parsed.num_lanes
    for name, (x, y) in scene.waypoints.items():
        waypoint = parsed.find_waypoint(name)
        assert waypoint is not None, name
        assert abs(waypoint.location[0] - x) < 1e-6 and abs(waypoint.location[1] - y) < 1e-6, name
    print(f"Open-RMF parsed {parsed.num_waypoints} waypoints and {parsed.num_lanes} lanes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
