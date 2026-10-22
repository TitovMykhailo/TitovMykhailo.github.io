# Where the content comes from

Everything on the site was checked against Mykhailo's public repositories on 22 October 2026.

## Numbers

| Claim | How it was verified |
| --- | --- |
| KIZUNA v2: 167 automated tests passing | `pytest` on a clean clone of `TitovMykhailo/Kizuna-v2` — 167 passed |
| KIZUNA v2: 12-node Docker lab | `kizuna/README.md` and `docker/docker-compose.yml` (node-01 … node-12) |
| KIZUNA v2: ≈10.5k lines of Python | line count of `*.py` files outside `tests/` |
| KIZUNA v2: scenario map | node names, roles and positions from `kizuna/simulator/scenario.json` |
| KIZUNA v2: packet header | `struct "!4sBBIdHI"` in `kizuna/daemon/protocol/packet.py` |
| Task Tracker: 35 REST endpoints | count of `@Get/Post/Put/Delete/PatchMapping` in the backend |
| Task Tracker: 7 screens, 3 integration test suites | `README.md` |
| Appointment System: 29 REST endpoints, 7 service tests | mapping and `@Test` counts in the backend |
| Study Group: 34 REST endpoints, 8 tables | mapping count; table list in `README.md` |
| Job Hunter Agent: 5 sources, 0–10 score, ≥ 7 shortlist | `README.md` |
| Video Editing Automation: 12 scripts, 2 style profiles | `scripts/` folder and `README.md` |

## Screenshots

Task Tracker and Appointment System screenshots show the real React frontends from the public repositories,
run locally. The backends could not be started in the build environment, so API responses were filled with
demo data shaped like each project's own seed data (`DataSeeder.java`). The captions on the case-study pages say so.

## Not public / not verified

- Hybrid SEC-DED Decoder and ProstaPaper have no public source; their pages use clearly labelled illustrations.
- ProstaPaper was a team project at RAKATHON 2026 in Brno; individual contribution is not documented yet.
- No patient data appears anywhere on the site.
- 16-QAM Mapper is excluded at Mykhailo's request; it is not his project.
