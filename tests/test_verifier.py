from slimconfig import build_output

import verifier
from contract import RecountInput, RecountOutput


def verdict(given, made):
    return verifier.verify_task(
        "recount-ranked-choice", build_output(given, RecountInput), build_output(made, RecountOutput), None, "."
    )


def test_recount_and_tie_break():
    given = {
        "candidates": ["a", "b", "c"],
        "ballots": [{"rankings": ["a", "b"]}, {"rankings": ["b", "a"]}, {"rankings": ["c", "a"]}],
    }
    made = {
        "rounds": [
            {"active": ["a", "b", "c"], "tallies": [1, 1, 1], "exhausted": 0, "eliminated": "c"},
            {"active": ["a", "b"], "tallies": [2, 1], "exhausted": 0, "eliminated": ""},
        ],
        "winner": "a",
    }
    assert verdict(given, made)["valid"] is True
    assert verdict(given, made | {"winner": "b"})["valid"] is False
    wrong = made | {"rounds": [made["rounds"][0] | {"eliminated": "a"}, made["rounds"][1]]}
    assert verdict(given, wrong)["valid"] is False


def test_exhausted_ballots_and_bad_input():
    good = build_output({"candidates": ["a", "b"], "ballots": [{"rankings": []}]}, RecountInput)
    assert verifier.verify_input("recount_election", good)["valid"] is True
    bad = build_output({"candidates": ["a", "a"], "ballots": [{"rankings": ["a"]}]}, RecountInput)
    assert verifier.verify_input("recount_election", bad)["valid"] is False
