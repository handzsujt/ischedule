from src.ischedule import run_loop, schedule, Scheduler

sch = Scheduler()


@schedule(interval=0.1)
def task():
    print("Performing a task")


def test():
    run_loop(return_after=1)


@sch.schedule(interval=0.1)
def task_cl():
    print("Performing a task")


def test_cl():
    sch.run_loop(return_after=1)
