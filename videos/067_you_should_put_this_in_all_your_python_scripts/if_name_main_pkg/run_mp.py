import multiprocessing as mp


def run_mp(f, args):
    print(__name__)
    import time
    time.sleep(10)
    with mp.Pool() as p:
        results = p.map(f, args)
        print(results)

def worker_fn(f, args):
    results = f(*args)
    print(results)