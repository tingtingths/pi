#!/usr/bin/python3
import time, sys, threading
import multiprocessing as mp

class Worker(threading.Thread):
#class Worker(mp.Process):
    def __init__(self, rank, step, thread_split, result):
        threading.Thread.__init__(self)
        #mp.Process.__init__(self)
        self.base_num = int(rank * thread_split)
        self.end_num = int(self.base_num + thread_split)
        self.step = step
        self.result = result

    def run(self):
        for i in range(self.base_num, self.end_num):
            x = (i + 0.5) * self.step
            self.result.value = self.result.value + 4 / (1 + x * x)

if __name__ == "__main__":
    if sys.argv[1]:
        s = sys.argv[1]
        if s == "maxsize":
            split = sys.maxsize
        else:
            split = int(sys.argv[1])
    num_thread = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    step = 1.0 / split
    thread_split = split / num_thread
    _threads = []

    print("split: {0}, step: {1}".format(split, step))

    for i in range(0, num_thread):
        _threads.append((Worker(i, step, thread_split, mp.Value("d", 0.0))))

    start = time.time()
    [t.start() for t in _threads]
    [t.join() for t in _threads]
    end = time.time()

    sum = 0
    for t in _threads:
        sum += t.result.value

    print("pi: {0}, time: {1}".format(step*sum, end - start))
