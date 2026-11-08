# Neotics kit for Open-RMF

This folder is Neotics' own work, added to our copy of [Open-RMF](https://github.com/open-rmf/rmf). It turns the waypoints and lanes of any Neotics scene into an Open-RMF traffic graph.

It is one part of the Neotics stack. Every fork in [neotics-io](https://github.com/neotics-io) reads the same two files:

- a **Neotics Scene** (`samples/depot.scene.json`): the room, the obstacles, the arm and the named places;
- a **Neotics Episode** (`samples/depot.episode.json`): a run recorded in MuJoCo, with time, joint positions and commands.

The depot is a sample made for these tools. It is not an entry or an answer for any [Neotics challenge](https://lab.neotics.io).

## Use it

Run from this folder:

```bash
python scene_to_nav_graph.py samples/depot.scene.json depot.nav.yaml
```

## How it's checked

Reads the exported graph with Open-RMF's own parser on ROS 2 Jazzy and confirms every waypoint and lane. This runs on GitHub in `.github/workflows/neotics.yml`, on every change to this folder.

## Licence

See [`LICENSE`](LICENSE). It covers this folder only.
