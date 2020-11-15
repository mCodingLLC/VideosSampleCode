import random
import time
from graphlib import TopologicalSorter
from multiprocessing import Queue, Process


def do_work(node):
    print('compiling', node)
    time.sleep(random.random())
    print('done compiling', node)


def worker(task_queue, done_queue):
    for node in iter(task_queue.get, 'STOP'):
        do_work(node)
        done_queue.put(node)





def compiler_example():
    NUMBER_OF_PROCESSES = 2

    task_queue = Queue()
    done_queue = Queue()

    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    graph = {
        'myprog': ['extlib1', 'fmtlib', 'urllib', 'mylib'],
        'mylib': ['fmtlib', 'stdlib'],
    }

    do_all_tasks(graph, task_queue, done_queue)

    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


def do_all_tasks(graph, task_queue, done_queue):
    topological_sorter = TopologicalSorter(graph)
    topological_sorter.prepare()
    while topological_sorter.is_active():
        for node in topological_sorter.get_ready():
            task_queue.put(node)
        node = done_queue.get()
        topological_sorter.done(node)


if __name__ == '__main__':
    dependencies = {
        'scipy': {'numpy'},
        'pandas': {'numpy', 'scipy', 'requests'},
        'requests': {'urllib3'},
    }

    from graphlib import TopologicalSorter
    ts = TopologicalSorter(dependencies)
    print(list(ts.static_order()))















