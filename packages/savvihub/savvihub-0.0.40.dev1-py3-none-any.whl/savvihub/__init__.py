from savvihub.common.context import Context


def log(step, row=None):
    """
    step: a step for each iteration (required)
    row: a dictionary to log
    """
    context = Context(experiment_required=True)
    context.experiment.log(row=row, step=step)
