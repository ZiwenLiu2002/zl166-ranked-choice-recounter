from contract import RoundResult


def result(valid, message):
    return {"valid": valid, "score": float(valid), "message": message, "details": {}}


def problem(value):
    if not 2 <= len(value.candidates) <= 8 or len(set(value.candidates)) != len(value.candidates):
        return "candidates must be two to eight unique ids"
    known = set(value.candidates)
    if not 1 <= len(value.ballots) <= 50:
        return "ballots must contain one to fifty entries"
    if any(len(set(b.rankings)) != len(b.rankings) or not set(b.rankings) <= known for b in value.ballots):
        return "a ballot repeats or names an unknown candidate"
    return None


def expected(value):
    active = set(value.candidates)
    rounds = []
    while True:
        ordered = sorted(active)
        counts = {name: 0 for name in ordered}
        exhausted = 0
        for ballot in value.ballots:
            available = [name for name in ballot.rankings if name in active]
            if available:
                counts[available[0]] += 1
            else:
                exhausted += 1
        continuing = len(value.ballots) - exhausted
        winners = [name for name in ordered if counts[name] * 2 > continuing]
        if winners or len(active) == 1:
            rounds.append(
                RoundResult(active=ordered, tallies=[counts[x] for x in ordered], exhausted=exhausted, eliminated="")
            )
            return rounds, winners[0] if winners else ordered[0]
        low = min(counts.values())
        eliminated = max(name for name in ordered if counts[name] == low)
        rounds.append(
            RoundResult(
                active=ordered, tallies=[counts[x] for x in ordered], exhausted=exhausted, eliminated=eliminated
            )
        )
        active.remove(eliminated)
