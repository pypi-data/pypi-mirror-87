import dida
from dida import triggers


@dida.job(trigger=triggers.IntervalTrigger(seconds=10))
def example_job():
    pass


@dida.job
def example_job2(arg, arg2 = "Hello Dida"):
    pass
