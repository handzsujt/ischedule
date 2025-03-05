import time
from threading import Event, Thread

import pytest

from src.ischedule import reset, run_loop, schedule, Scheduler


def task_1():
    print("Task 1")
    t1 = time.monotonic()
    while True:
        time.sleep(0.1)  # w/o sleep GIL attacks
        if time.monotonic() - t1 > 0.5:
            break
    print("Task 1 end", t1, time.monotonic())


def task_2():
    print("Task 2", time.monotonic())


def task_3():
    print("Task 3", time.monotonic())


def task_4():
    print("Task 4", time.monotonic())


def test_thread_1():
    schedule(task_1, interval=0.1)
    schedule(task_2, interval=0.2)
    stop_event = Event()
    Thread(target=lambda: [time.sleep(1), stop_event.set()]).start()
    run_loop(stop_event)


def test_thread_2():
    schedule(task_1, interval=0.1)
    schedule(task_2, interval=0.2)
    stop = Event()
    Thread(target=run_loop, kwargs={"stop_event": stop}, daemon=False).start()

    time.sleep(1)
    stop.set()


def test_multi_thread():
    sch1 = Scheduler()
    sch1.schedule(task_1, interval=0.1)
    sch1.schedule(task_2, interval=0.2)
    sch2 = Scheduler()
    sch2.schedule(task_3, interval=0.3)
    sch2.schedule(task_4, interval=0.5)
    stop1 = Event()
    stop2 = Event()
    Thread(target=sch1.run_loop, kwargs={"stop_event": stop1}, daemon=False).start()
    Thread(target=sch2.run_loop, kwargs={"stop_event": stop2}, daemon=False).start()

    time.sleep(3)
    stop1.set()
    stop2.set()


if __name__ == "__main__":
    test_multi_thread()


@pytest.fixture(autouse=True)
def reset_scheduler():
    print("reset")
    reset()
