from gilda_opts.schedule import Schedule


def test_schedule_1():
    dq = """{
    "system":{
      "name": "s1",
      "uid": 1,
      "blocks":[{"index":0, "duration":1},
              {"index":1, "duration":1},
              {"index":2, "duration":1},
              {"index":3, "duration":1},
              {"index":4, "duration":1}],
      "buses": [{"uid": 1,
                 "name": "home"},
                {"uid": 2,
                 "name": "casa"}],
     "demands": [{"name": "d1",
                   "loads": [1, 2, 3, 4]}]
    }}"""

    q1 = Schedule.from_json(dq)

    assert q1.system.name == "s1"
    assert q1.system.demands[0].loads[1] == 2
    assert q1.system.blocks[1].index == 1
