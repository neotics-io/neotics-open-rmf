import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))

from neotics_scene import Scene  # noqa: E402
from scene_to_nav_graph import LEVEL, to_nav_graph  # noqa: E402


@pytest.fixture
def level():
    return to_nav_graph(Scene.load(KIT / "samples" / "depot.scene.json"))["levels"][LEVEL]


def test_every_waypoint_is_a_named_vertex(level):
    assert [v[2]["name"] for v in level["vertices"]] == ["dock", "aisle_west", "center", "aisle_east", "charger", "pickup", "dropoff"]


def test_lanes_run_both_ways(level):
    pairs = {(a, b) for a, b, _ in level["lanes"]}
    assert len(level["lanes"]) == 12 and all((b, a) in pairs for a, b in pairs)


def test_every_place_can_be_reached_from_the_dock(level):
    reach, frontier = {0}, [0]
    while frontier:
        here = frontier.pop()
        for a, b, _ in level["lanes"]:
            if a == here and b not in reach:
                reach.add(b)
                frontier.append(b)
    assert len(reach) == len(level["vertices"])


def test_charger_and_parking_are_marked(level):
    by_name = {v[2]["name"]: v[2] for v in level["vertices"]}
    assert by_name["charger"]["is_charger"] and by_name["dock"]["is_parking_spot"] and not by_name["center"]["is_charger"]
