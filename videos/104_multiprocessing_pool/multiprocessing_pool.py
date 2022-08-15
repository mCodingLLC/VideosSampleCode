from __future__ import annotations

import os.path
import time
from multiprocessing import Pool

import numpy as np
import scipy.io.wavfile


def gen_fake_data(filenames):
    print("generating fake data")
    try:
        os.mkdir("sounds")
    except FileExistsError:
        pass

    for filename in filenames:  # homework: convert this loop to pool too!
        if not os.path.exists(filename):
            print(f"creating {filename}")
            gen_wav_file(filename, frequency=440, duration=60.0 * 4)


def gen_wav_file(filename: str, frequency: float, duration: float):
    samplerate = 44100
    t = np.linspace(0., duration, int(duration * samplerate))
    data = np.sin(2. * np.pi * frequency * t) * 0.0
    scipy.io.wavfile.write(filename, samplerate, data.astype(np.float32))


def etl(filename: str) -> tuple[str, float]:
    # extract
    start_t = time.perf_counter()
    samplerate, data = scipy.io.wavfile.read(filename)

    # do some transform
    eps = .1
    data += np.random.normal(scale=eps, size=len(data))
    data = np.clip(data, -1.0, 1.0)

    # load (store new form)
    new_filename = filename.removesuffix(".wav") + "-transformed.wav"
    scipy.io.wavfile.write(new_filename, samplerate, data)
    end_t = time.perf_counter()

    return filename, end_t - start_t


def etl_demo():
    filenames = [f"sounds/example{n}.wav" for n in range(24)]
    gen_fake_data(filenames)
    start_t = time.perf_counter()

    print("starting etl")
    with Pool() as pool:
        results = pool.map(etl, filenames)

        for filename, duration in results:
            print(f"{filename} completed in {duration:.2f}s")

    end_t = time.perf_counter()
    total_duration = end_t - start_t
    print(f"etl took {total_duration:.2f}s total")


def run_normal(items, do_work):
    print("running normally on 1 cpu")
    start_t = time.perf_counter()
    results = list(map(do_work, items))
    end_t = time.perf_counter()
    wall_duration = end_t - start_t
    print(f"it took: {wall_duration:.2f}s")
    return results


def run_with_mp_map(items, do_work, processes=None, chunksize=None):
    print(f"running using multiprocessing with {processes=}, {chunksize=}")
    start_t = time.perf_counter()
    with Pool(processes=processes) as pool:
        results = pool.imap(do_work, items, chunksize=chunksize)
    end_t = time.perf_counter()
    wall_duration = end_t - start_t
    print(f"it took: {wall_duration:.2f}s")
    return results


def fib(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def n_fibs(n):
    if n < 2:
        return [i for i in range(n)]
    fibs = [0, 1]
    a, b = 0, 1
    for _ in range(n - 2):
        a, b = b, a + b
        fibs.append(b)
    return fibs


def compare_mp_map_to_normal():
    items = list(range(10000))
    do_work = fib
    run_with_mp_map(items, do_work)

    print()
    run_normal(items, do_work)


def main():
    etl_demo()
    # compare_mp_map_to_normal()


if __name__ == '__main__':
    main()
