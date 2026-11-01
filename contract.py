from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    RECOUNT_ELECTION = "recount_election"


class Task(Enum):
    RECOUNT_RANKED_CHOICE = "recount-ranked-choice"


@dataclass
class Ballot(Output):
    rankings: Annotated[list[str], "Candidates in preference order; omitted candidates are unranked"]


@dataclass
class RecountInput(Output):
    candidates: Annotated[list[str], "Two to eight unique candidate ids"]
    ballots: Annotated[list[Ballot], "One to fifty ranked ballots"]


@dataclass
class RoundResult(Output):
    active: Annotated[list[str], "Active candidates in sorted order before elimination"]
    tallies: Annotated[list[int], "First-active-preference votes aligned with active"]
    exhausted: Annotated[int, "Ballots with no active ranked candidate"]
    eliminated: Annotated[str, "Eliminated candidate, or empty when this round elects the winner"]


@dataclass
class RecountOutput(Output):
    rounds: Annotated[list[RoundResult], "Complete instant-runoff audit trail"]
    winner: Annotated[str, "Candidate winning a strict majority or the last active candidate"]


TOOLS = {Tool.RECOUNT_ELECTION: (RecountInput, RecountOutput)}
TASKS = {Task.RECOUNT_RANKED_CHOICE: (RecountInput, RecountOutput)}
