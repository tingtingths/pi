#!/usr/bin/python3
import multiprocessing as mp
import time, sys

def calc(step, base, end):
    ret = 0
    for i in range(base, end):
            x = (i + 0.5) * step
            ret = ret + 4 / (1 + x * x)
    q.put(ret)

if __name__ == "__main__":
    if sys.argv[1]:
        s = sys.argv[1]
        if s == "maxsize":
            split = sys.maxsize
        else:
            split = int(sys.argv[1])

    num_thread = int(sys.argv[2]) if len(sys.argv) > 2 else mp.cpu_count()
    step = 1.0 / split
    thread_split = split / num_thread
    _threads = []

    print("split: {0}, step: {1}".format(split, step))

    q = mp.Queue()

    start = time.time()
    for i in range(0, num_thread):
        base = int(i * thread_split)
        end = int(base + thread_split)
        _threads.append(mp.Process(target=calc, args=(step, base, end,)))
        _threads[i].start()
        print(str(i) + " start")

    for i in range(0, num_thread):
        _threads[i].join()
    end = time.time()

    sum = 0
    for i in range(0, num_thread):
        sum += q.get()

    print("pi: {0}, time: {1}".format(step*sum, end - start))
