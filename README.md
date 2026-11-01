# Ranked Choice Recounter

Produces a deterministic instant-runoff audit trail from ranked ballots.

## Tools

`recount_election` counts every round; `recount-ranked-choice` returns all tallies, exhausted ballots, eliminations, and the winner. Lowest-tally ties eliminate the lexicographically greatest candidate id.

## Layout

The typed contract is in `contract.py`, execution code in `src/plugin/`, deterministic recount checks in `verifier/`, and adversarial cases in `tests/`.

## Develop and run

Run `uv sync --extra dev`, `uv run pytest`, and `uv run ruff check .`.
