from contract import Task, Tool

from .checks import expected, problem, result


def verify_input(tool, value):
    Tool(tool)
    issue = problem(value)
    return result(issue is None, issue or "input is valid")


def verify_output(tool, input_value, output_value, workspace):
    Tool(tool)
    rounds, winner = expected(input_value)
    valid = output_value.rounds == rounds and output_value.winner == winner
    return result(valid, "recount is exact" if valid else "rounds or winner differ from the deterministic recount")


def verify_task(task, arguments, output, reference, workspace):
    Task(task)
    return verify_output("recount_election", arguments, output, workspace)
