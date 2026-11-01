from contract import RecountOutput, RoundResult


def validate(value):
    if not 2 <= len(value.candidates) <= 8 or len(set(value.candidates)) != len(value.candidates):
        raise ValueError("candidates must contain two to eight unique ids")
    known = set(value.candidates)
    if not 1 <= len(value.ballots) <= 50:
        raise ValueError("ballots must contain one to fifty entries")
    for ballot in value.ballots:
        if len(set(ballot.rankings)) != len(ballot.rankings) or not set(ballot.rankings) <= known:
            raise ValueError("each ballot must rank known candidates at most once")


def recount_election(value, workspace):
    validate(value)
    active = set(value.candidates)
    rounds = []
    while True:
        ordered = sorted(active)
        counts = {name: 0 for name in ordered}
        exhausted = 0
        for ballot in value.ballots:
            choice = next((name for name in ballot.rankings if name in active), None)
            if choice is None:
                exhausted += 1
            else:
                counts[choice] += 1
        continuing = len(value.ballots) - exhausted
        winner = next((name for name in ordered if counts[name] * 2 > continuing), None)
        if winner is not None or len(active) == 1:
            winner = winner or ordered[0]
            rounds.append(
                RoundResult(active=ordered, tallies=[counts[x] for x in ordered], exhausted=exhausted, eliminated="")
            )
            return RecountOutput(rounds=rounds, winner=winner)
        fewest = min(counts.values())
        eliminated = max(name for name in ordered if counts[name] == fewest)
        rounds.append(
            RoundResult(
                active=ordered, tallies=[counts[x] for x in ordered], exhausted=exhausted, eliminated=eliminated
            )
        )
        active.remove(eliminated)
