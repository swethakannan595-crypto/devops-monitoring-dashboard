import multiprocessing
import time


def cpu_stress():
    while True:
        x = 999999 * 999999
        x = x ** 2


if __name__ == "__main__":

    cores = multiprocessing.cpu_count()

    print(f"Starting CPU load on {cores} cores")

    processes = []

    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping CPU test")

        for p in processes:
            p.terminate()